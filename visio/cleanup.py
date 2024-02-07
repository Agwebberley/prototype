import json
import os

class StarUML:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def load_data(self):
        with open(self.file_path) as f:
            self.data = json.load(f)

    def print_out(self):
        for element in self.data['ownedElements']:
            if element['_type'] == 'ERDDataModel':
                if 'ownedElements' in element:
                    for sub_element in element['ownedElements']:
                        if sub_element['_type'] == 'ERDEntity':
                            print('Table:', sub_element['name'])
                            print('Columns:')
                            if 'columns' in sub_element:
                                for attribute in sub_element['columns']:
                                    print(' -', attribute['name'], ':', attribute['type'])
                                    if 'tags' in attribute:
                                        print('    Tags:')
                                        for tag in attribute['tags']:
                                            print('     -', tag['name'], ':', tag['value'])

                            print('Relationships:')
                            if 'ownedElements' in sub_element:
                                for relationship in sub_element['ownedElements']:
                                    if relationship['_type'] == 'ERDRelationship':
                                        print(' -', relationship['name'], end='; ')
                                        connected_table_id = relationship['end2']['reference']['$ref']
                                        print('connected Table:', connected_table_id)
                                        for connected_element in element['ownedElements']:
                                            if connected_element['_type'] == 'ERDEntity' and connected_element['_id'] == connected_table_id:
                                                print(sub_element['name'], '-', connected_element['name'], end='; ')
                                                if 'cardinality' in relationship['end1']:
                                                    cardinality = relationship['end1']['cardinality']
                                                else:
                                                    cardinality = '1'
                                                if 'cardinality' in relationship['end2']:
                                                    cardinality += '-' + relationship['end2']['cardinality']
                                                else:
                                                    cardinality += '-1'
                                                print('Cardinality:', cardinality)

    def generate_django_models(self):
        type_mapping = {
            'CHAR': 'CharField',
            'INTEGER': 'IntegerField',
            'FLOAT': 'FloatField',
            'BOOLEAN': 'BooleanField',
            'DATE': 'DateField',
            'DATETIME': 'DateTimeField',
            'TEXT': 'TextField',
        }
        
        imported_tables = self.get_relationships_imports()
        print(imported_tables)
        for element in self.data['ownedElements']:
            if element['_type'] == 'ERDDataModel':
                if 'ownedElements' in element:
                    for sub_element in element['ownedElements']:
                        if sub_element['_type'] == 'ERDEntity':
                            model_name = sub_element['name']
                            app_name, table_name = model_name.split('.')
                            app_folder = os.path.join('your_project_folder', app_name)
                            os.makedirs(app_folder, exist_ok=True)
                            with open(os.path.join(app_folder, 'models.py'), 'w') as f:
                                f.write(f"from django.db import models\n")
                                if app_name in imported_tables:
                                    for connected_app_name in imported_tables[app_name]:
                                        f.write(f"from {connected_app_name}.models import ")
                                        for connected_table_name in imported_tables[app_name][connected_app_name]:
                                            f.write(f"{connected_table_name}, ")
                                        f.write("\n")
                                f.write(f"\n")
                                f.write(f"class {table_name}(models.Model):\n")
                                self.write_attributes(sub_element, f, type_mapping)
                                self.write_relationships(sub_element, element, f, app_name)
                                f.write(f"\n")

    def write_attributes(self, sub_element, file, type_mapping):
        if 'columns' in sub_element:
            for attribute in sub_element['columns']:
                attribute_name = attribute['name']
                attribute_type = attribute['type']
                django_attribute_type = type_mapping.get(attribute_type, 'CharField')
                file.write(f"    {attribute_name} = models.{django_attribute_type}()\n")

    def write_relationships(self, sub_element, element, file, app_name):
        if 'ownedElements' in sub_element:
            for relationship in sub_element['ownedElements']:
                if relationship['_type'] == 'ERDRelationship':
                    connected_table_id = relationship['end2']['reference']['$ref']
                    for connected_element in element['ownedElements']:
                        if connected_element['_type'] == 'ERDEntity' and connected_element['_id'] == connected_table_id:
                            connected_table_name = connected_element['name']
                            connected_app_name, connected_table_name = connected_table_name.split('.')
                            file.write(f"    {connected_table_name} = models.ForeignKey('{connected_app_name}.{connected_table_name}', on_delete=models.CASCADE)\n")
        
    def write_relationship_imports(self, sub_element, app_name, existing_code, file):
        imported_tables = set()
        # If There are relationships in a table, we need to import the related tables if there are not in the same file
        # If anconnected table is in the same file, we don't need to import it again
        # The import statement is added to the top of the file
        if 'ownedElements' in sub_element:
            for relationship in sub_element['ownedElements']:
                if relationship['_type'] == 'ERDRelationship':
                    connected_table_id = relationship['end2']['reference']['$ref']
                    for connected_element in sub_element['ownedElements']:
                        if connected_element['_type'] == 'ERDEntity' and connected_element['_id'] == connected_table_id:
                            connected_table_name = connected_element['name']
                            connected_app_name, connected_table_name = connected_table_name.split('.')
                            if connected_app_name != app_name:
                                if connected_app_name not in imported_tables:
                                    import_statement = f"from {connected_app_name}.models import {connected_table_name}\n"
                                    if import_statement not in existing_code:
                                        file.write(f"from {connected_app_name}.models import {connected_table_name}\n" + existing_code)
                                    imported_tables.add(connected_app_name)
                            else:
                                imported_tables.add(connected_app_name)
                            break
    
    def get_relationships_imports(self):
        # Return a dicionary with the app name as the key and the set of imported tables as the value
        imported_tables = {}
        for element in self.data['ownedElements']:
            if element['_type'] == 'ERDDataModel':
                if 'ownedElements' in element:
                    for sub_element in element['ownedElements']:
                        if sub_element['_type'] == 'ERDEntity':
                            if 'ownedElements' in sub_element:
                                for relationship in sub_element['ownedElements']:
                                    if relationship['_type'] == 'ERDRelationship':
                                        connected_table_id = relationship['end2']['reference']['$ref']
                                        for connected_element in element['ownedElements']:
                                            if connected_element['_type'] == 'ERDEntity' and connected_element['_id'] == connected_table_id:
                                                connected_table_name = connected_element['name']
                                                table_name = sub_element['name']
                                                connected_app_name, connected_table_name = connected_table_name.split('.')
                                                app_name, table_name = table_name.split('.')
                                                # Dictionary structure:
                                                # {app_name: {connected_app_name: [table1, table2, ...]}}
                                                if app_name not in imported_tables:
                                                    imported_tables[app_name] = {}
                                                if connected_app_name not in imported_tables[app_name]:
                                                    imported_tables[app_name][connected_app_name] = set()
                                                imported_tables[app_name][connected_app_name].add(connected_table_name)
        return imported_tables
        
    

if __name__ == '__main__':
    file_path = r'prototype\Database.mdj'
    visio_cleanup = StarUML(file_path)
    visio_cleanup.load_data()
    #visio_cleanup.print_out()
    visio_cleanup.generate_django_models()
