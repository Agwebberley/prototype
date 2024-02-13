import json
import os
import sqlite3
import ast

class StarUML:
    """
    TODO: Add a validation function to check if the models already match the database design
    TODO: Allow any functions within models.py files to persist

    """
    def __init__(self, file_path, folder_path='your_project_folder'):
        self.file_path = file_path
        self.data = None
        self.folder_path = folder_path
        cfv = ClassFunctionVisitor()
        self.cfv = cfv


    def load_data(self):
        with open(self.file_path) as f:
            self.data = json.load(f)
    
    def get_app_names(self):
        # Get a list of all of the app names
        app_names = []
        for element in self.data['ownedElements']:
            if element['_type'] == 'ERDDataModel':
                if 'ownedElements' in element:
                    for sub_element in element['ownedElements']:
                        if sub_element['_type'] == 'ERDEntity':
                            app_name = sub_element['name'].split('.')[0]
                            if app_name not in app_names:
                                app_names.append(app_name)
        return app_names
    
    def get_file_paths(self):
        # Get a list of all of the file paths
        file_paths = []
        for app_name in self.get_app_names():
            file_paths.append(os.path.join(self.folder_path, app_name, 'models.py'))
        return file_paths



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
        empty_classes = self.get_empty_classes()
        
        imported_tables = self.get_relationships_imports()
        print(imported_tables)
        file_contents = {}
        for element in self.data['ownedElements']:
            if element['_type'] == 'ERDDataModel':
                if 'ownedElements' in element:
                    for sub_element in element['ownedElements']:
                        if sub_element['_type'] == 'ERDEntity':
                            model_name = sub_element['name']
                            app_name, table_name = model_name.split('.')
                            app_folder = os.path.join(self.folder_path, app_name)
                            os.makedirs(app_folder, exist_ok=True)
                            if app_folder not in file_contents:
                                file_contents[app_folder] = ''
                                file_contents[app_folder] += f"from django.db import models\n"
                                if app_name in imported_tables:
                                    for connected_app_name in imported_tables[app_name]:
                                        file_contents[app_folder] += f"from {connected_app_name}.models import "
                                        for connected_table_name in imported_tables[app_name][connected_app_name]:
                                            file_contents[app_folder] += f"{connected_table_name}, "
                                        # Remove the last comma and space
                                        file_contents[app_folder] = file_contents[app_folder][:-2]
                                        file_contents[app_folder] += "\n"
                            file_contents[app_folder] += "\n"
                            file_contents[app_folder] += f"class {table_name}(models.Model):\n"
                            file_contents[app_folder] += self.get_attributes(sub_element, type_mapping)
                            file_contents[app_folder] += self.get_relationships(sub_element, element, app_name)
                            file_contents[app_folder] += "\n"
                            if app_name in empty_classes and table_name in empty_classes[app_name]:
                                file_contents[app_folder] += "    pass\n"

        for app_folder, content in file_contents.items():
            with open(os.path.join(app_folder, 'models.py'), 'w') as f:
                f.write(content)

    def get_attributes(self, sub_element, type_mapping):
        attributes = ""
        if 'columns' in sub_element:
            for attribute in sub_element['columns']:
                attribute_name = attribute['name']
                attribute_type = attribute['type']
                django_attribute_type = type_mapping.get(attribute_type, 'CharField')
                attributes += f"    {attribute_name} = models.{django_attribute_type}()\n"
        return attributes

    def get_relationships(self, sub_element, element, app_name):
        relationships = ""
        if 'ownedElements' in sub_element:
            for relationship in sub_element['ownedElements']:
                if relationship['_type'] == 'ERDRelationship':
                    connected_table_id = relationship['end2']['reference']['$ref']
                    for connected_element in element['ownedElements']:
                        if connected_element['_type'] == 'ERDEntity' and connected_element['_id'] == connected_table_id:
                            connected_table_name = connected_element['name']
                            connected_app_name, connected_table_name = connected_table_name.split('.')
                            relationships += f"    {connected_table_name} = models.ForeignKey('{connected_app_name}.{connected_table_name}', on_delete=models.CASCADE)\n"
        return relationships
        

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
    
    def get_empty_classes(self):
        # Return a dictionary with the app name as the key and the set of empty classes as the value
        empty_classes = {}
        for element in self.data['ownedElements']:
            if element['_type'] == 'ERDDataModel':
                if 'ownedElements' in element:
                    for sub_element in element['ownedElements']:
                        if sub_element['_type'] == 'ERDEntity':
                            if 'columns' not in sub_element:
                                app_name, table_name = sub_element['name'].split('.')
                                if app_name not in empty_classes:
                                    empty_classes[app_name] = set()
                                empty_classes[app_name].add(table_name)

        
        return empty_classes

class ClassFunctionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.classes = {}

    def visit_ClassDef(self, node):
        # Initialize an empty list for each class to hold its functions
        self.classes[node.name] = []
        # Visit each node within the class definition to find function definitions
        self.generic_visit(node)
    def visit_FunctionDef(self, node):
        # Assuming the parent node is a ClassDef, add the function name to the class's list
        if isinstance(node.parent, ast.ClassDef):
            self.classes[node.parent.name].append(node.name)
    def generic_visit(self, node):
        # Before visiting children, set the parent attribute
        for child in ast.iter_child_nodes(node):
            child.parent = node
        super().generic_visit(node)
    
    def get_parent(self, node):
        # Since there is no built-in way to get the parent node, we can use this method
        # We have to traverse the tree from the root to the current node to find the parent
        for parent in ast.walk(self.tree):
            for child in ast.iter_child_nodes(parent):
                if child == node:
                    return parent
    def parse_python_file_with_ast(self, file_path):
        with open(file_path, 'r') as file:
            content = file.read()
            # Parse the content into an AST
            self.tree = ast.parse(content)
            # Visit the AST to fill the classes dictionary
            self.visit(self.tree)
        return self.classes
    def send_to_database(self, file_path):
        # Parse the file and get the classes and functions
        classes = self.parse_python_file_with_ast(file_path)
        # Using AST, find the actual code for each function
        with open(file_path, 'r') as file:
            content = file.read()
            tree = ast.parse(content)
            for class_name, functions in classes.items():
                for function_name in functions:
                    for node in ast.walk(tree):
                        parent = self.get_parent(node)
                        if parent is not None:
                            if isinstance(node, ast.FunctionDef) and node.name == function_name and parent.name == class_name:
                                code = ast.unparse(node)
                                save_to_database(class_name, function_name, code)
                    

def save_to_database(class_name, function_name, code):
    # Connect to the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create a table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS functions
                      (class_name TEXT, function_name TEXT, code TEXT)''')

    # Insert the data into the table
    cursor.execute("DELETE FROM functions")
    cursor.execute("INSERT INTO functions VALUES (?, ?, ?)", (class_name, function_name, code))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def print_from_database():
    # Connect to the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Select all the data from the table
    cursor.execute("SELECT * FROM functions")

    # Print the data
    for row in cursor.fetchall():
        print(row)

    # Close the connection
    conn.close()

if __name__ == '__main__':
    file_path = r'prototype\Database.mdj'
    visio_cleanup = StarUML(file_path)
    visio_cleanup.load_data()
    #visio_cleanup.print_out()
    visio_cleanup.generate_django_models()
    cfv = ClassFunctionVisitor()
    print(cfv.parse_python_file_with_ast(r'Orders\\models.py'))
    cfv.send_to_database(r'Orders\\models.py')
    print_from_database()
