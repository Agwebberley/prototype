import json

# Load the UML JSON file
with open(r'prototype\Database.mdj') as f:
    data = json.load(f)
# Iterate over the UML Models

for element in data['ownedElements']:
        if element['_type'] == 'ERDDataModel':
        # Iterate over the UML Classes
            if 'ownedElements' in element:
                for sub_element in element['ownedElements']:
                    if sub_element['_type'] == 'ERDEntity':
                        print('Table:', sub_element['name'])
                        print('Columns:')
                        if 'columns' in sub_element:
                            for attribute in sub_element['columns']:
                                print(' -', attribute['name'], ':', attribute['type'])
                        print('Relationships:')
                        if 'ownedElements' in sub_element:
                            for relationship in sub_element['ownedElements']:
                                if relationship['_type'] == 'ERDRelationship':
                                    print(' -', relationship['name'], end='; ')
                                    # Print the other table involved in the relationship
                                    other_table_id = relationship['end2']['reference']['$ref']
                                    for other_element in element['ownedElements']:
                                        if other_element['_type'] == 'ERDEntity' and other_element['_id'] == other_table_id:
                                            print(sub_element['name'], '-', other_element['name'], end='; ')
                                            # Print the cardinality
                                            if 'cardinality' in relationship['end1']:
                                                cardinality = relationship['end1']['cardinality']
                                            else:
                                                cardinality = '1'
                                            if 'cardinality' in relationship['end2']:
                                                cardinality += '-' + relationship['end2']['cardinality']
                                            else:
                                                cardinality += '-1'
                                            print('Cardinality:', cardinality)
