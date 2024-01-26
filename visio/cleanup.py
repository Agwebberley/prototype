import os
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

def cleanup_xml_files(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith('.xml'):
                file_path = os.path.join(root, filename)
                print(f"Cleaning up file: {file_path}")
                cleanup_xml_file(file_path)

def cleanup_xml_file(file_path):
    global Count
    Count = 0
    # Parse the XML document
    tree = ET.parse(file_path)

    # Get the root element
    root = tree.getroot()

    # Function to recursively traverse the XML tree and remove 'Cell' elements with decimal values
    def remove_cells_with_decimal_value(element):
        
        for child in element:
            if child.tag == '{http://schemas.microsoft.com/office/visio/2012/main}Cell':
                v_value = child.get('V')
                f_value = child.get('F')
                if not f_value:
                    f_value = ''
                if '.' in v_value or 'THEMEVAL' in f_value:
                    Count =+ 1
                    element.remove(child)
                remove_cells_with_decimal_value(child)
            else:
                remove_cells_with_decimal_value(child)

    # Call the function to remove 'Cell' elements with decimal values
    remove_cells_with_decimal_value(root)

    # Write the modified XML back to the file
    tree.write(file_path)

    # Prettify the XML file
    xml_string = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
    with open(file_path, "w") as file:
        file.write(xml_string)
    print(f"Cleaned up file: {file_path}")
    print(f"Removed {Count} cells with decimal values")


import json

# Load the UML JSON file
with open(r'visio\Models\ERD.mdj') as f:
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
                                        print(sub_element['name'], '-', other_element['name'])

if __name__ == "__mmain__":
    # Prompt the user to enter the folder path
    folder_path = r"""C:\Users\agweb\OneDrive\Documents\GitHub\prototype\visio\Delivery"""
    # Call the cleanup_xml_files function with the folder path
    cleanup_xml_files(folder_path)
