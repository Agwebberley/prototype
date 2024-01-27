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
                                        other_table_id = relationship['end2']['reference']['$ref']
                                        for other_element in element['ownedElements']:
                                            if other_element['_type'] == 'ERDEntity' and other_element['_id'] == other_table_id:
                                                print(sub_element['name'], '-', other_element['name'], end='; ')
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

        for element in self.data['ownedElements']:
            if element['_type'] == 'ERDDataModel':
                if 'ownedElements' in element:
                    for sub_element in element['ownedElements']:
                        if sub_element['_type'] == 'ERDEntity':
                            model_name = sub_element['name']
                            app_name, table_name = model_name.split('.')
                            app_folder = os.path.join('your_project_folder', app_name)
                            os.makedirs(app_folder, exist_ok=True)
                            with open(os.path.join(app_folder, 'models.py'), 'a') as f:
                                f.write(f"from django.db import models\n")
                                self.write_relationship_imports(element, f)
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
                    other_table_id = relationship['end2']['reference']['$ref']
                    for other_element in element['ownedElements']:
                        if other_element['_type'] == 'ERDEntity' and other_element['_id'] == other_table_id:
                            other_table_name = other_element['name']
                            other_app_name, other_table_name = other_table_name.split('.')
                            file.write(f"    {other_table_name} = models.ForeignKey('{other_app_name}.{other_table_name}', on_delete=models.CASCADE)\n")
        
    def write_relationship_imports(self, element, file):
        imported_tables = set()
        for sub_element in element['ownedElements']:
            if sub_element['_type'] == 'ERDEntity':
                for relationship in sub_element['ownedElements']:
                    if relationship['_type'] == 'ERDRelationship':
                        other_table_id = relationship['end2']['reference']['$ref']
                        for other_element in element['ownedElements']:
                            if other_element['_type'] == 'ERDEntity' and other_element['_id'] == other_table_id:
                                other_table_name = other_element['name']
                                other_app_name, other_table_name = other_table_name.split('.')
                                import_statement = f"from {other_app_name}.models import {other_table_name}\n"
                                if other_table_name not in imported_tables:
                                    file.write(import_statement)
                                    imported_tables.add(other_table_name)

if __name__ == '__main__':
    file_path = r'prototype\Database.mdj'
    visio_cleanup = StarUML(file_path)
    visio_cleanup.load_data()
    visio_cleanup.print_out()
    visio_cleanup.generate_django_models()
