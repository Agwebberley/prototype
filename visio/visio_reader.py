from vsdx import VisioFile
import sys

DBG = False

# open a visio file
def visio_open(filename):
  if DBG: print("Opening Visio file",filename)
  # Return a file handle to the Visio file
  return VisioFile(filename)

# Get the indicated page
def visio_get_page(visio_file,page_index):
  if DBG: print("Returning diagram page",page_index)
  # Return the requested page
  page = visio_file.pages[page_index]
  if DBG: print("Page:",page)
  return page

def visio_get_all_shapes(page):
  if DBG: print("Returning all shapes on page")
  # Find all shapes on this page
  all_shapes = page.child_shapes
  shape_list = []
  # Return the list of shapes
  if DBG: print("Shapes:")
  for shape in all_shapes:
    if shape.shape_type == 'Shape':
      if DBG: print(" ... ",shape.shape_type,shape.shape_name,shape.text)
      shape_list.append(shape)
    elif shape.shape_type == 'Group':
      sublist = visio_get_all_subshapes(shape)
      shape_list.extend(sublist)
    else:
      print("Unknown Shape Type:",str.strip(shape.shape_type))
  return shape_list

def visio_get_all_subshapes(group):
  if DBG: print("Returning all subshapes in shape",group.shape_type,group.shape_name,group.text)
  # Find all subshapes in this shape
  child_shape_list = group.child_shapes
  shape_list = []
  if DBG: print("Child Shapes:")
  for shape in child_shape_list:
    if shape.shape_type == 'Shape':
      if DBG: print(" ... ",shape.shape_type,shape.shape_name,shape.text)
      shape_list.append(shape)
    elif shape.shape_type == 'Group':
      sublist = visio_get_all_subshapes(shape)
      shape_list.extend(sublist)
    else:
      print("Unknown Shape Type:",str.strip(shape.shape_type))
  return shape_list

# Get the indicated shape
def visio_get_shape_by_name(page,name):
  if DBG: print("Returning shape with name =",name)
  # Return the requested shape
  shape = page.find_shape_by_text(name)
  if DBG: print("Shape =",shape)
  return shape

# Get all the connections to and from a shape
def visio_get_shape_connections(shape):
  if DBG: print("Getting connections to",shape.shape_type,shape.shape_name,shape.text)
  # Return the connection list
  connections = shape.connected_shapes
  if DBG:
    print("Connections:")
    for con in connections:
      print(" ... ",con.shape_type,con.shape_name,con.text)
  return connections

# Visit all the shapes connected to the current shape
def visit_shape_connections(shape, visited_list):
  if DBG: print("Visiting connections from", shape.shape_type,shape.shape_name,shape.text)
  # See if this shape has been visited before
  if shape.shape_name in visited_list:
    if DBG: print("Shape", shape.shape_type,shape.shape_name,shape.text, "has already been visited")
    return

  # Put this shape on the visited list
  visited_list.append(shape.shape_name)
  if DBG: print("Putting",shape.shape_type,shape.shape_name,shape.text,"on visited list")

  # Find all connections away from this object
  connections = visio_get_shape_connections(shape)
  for con in connections:
    if con.shape_name not in visited_list:
      visited_list.append(con.shape_name)
      if DBG: print("Putting",shape.shape_type,shape.shape_name,shape.text,"on visited list")

      # Connection not on list - visit all of it's connecteds
      connecteds = visio_get_shape_connections(con)
      for each in connecteds:
        visit_shape_connections(each, visited_list)

    else:
      # Connection has already been visited
      if DBG: print("Connection", shape.shape_type,shape.shape_name,shape.text, "has already been visited")

  # All connected shapes visited
  if DBG: print("End of connections to shape",shape.shape_type,shape.shape_name,shape.text)

  # See if shape has a parent
  if shape.shape_name != None:
    if DBG: print("Looking for connections to shape parent:",
                  shape.parent.shape_type,shape.parent.shape_name,shape.parent.text)
    visit_shape_connections(shape.parent, visited_list)
  return

if __name__ == "__main__":
  DBG = True
  which = 2
  if which == 0:
    filename = 'TestFile.vsdx'
    #start_name = 'Start'
  elif which == 1:
    filename = 'DrawioWorkflowDiagram.vsdx'
    #start_name = 'Start'
  elif which == 2:
    filename = './visio/Drawing1.vsdm'
  else:
    filename = 'DrawioTestDiagram.vsdx'
    #start_name = 'Customers'

  # Open Visio file
  visfl = visio_open(filename)

  # Get page 0
  page0 = visio_get_page(visfl,0)

  # Find all the shapes and make sure one of them is called "Start"
  all_shapes = visio_get_all_shapes(page0)
  #start_shape = None
  #for shape in all_shapes:
  #  if str.strip(shape.text) == start_name:
  #    start_shape = shape
  #    break
  #
  # Verify "Start" shape located
  #if start_shape == None:
  #  print("ERROR: Workflow diagram does not contain a 'Start' shape")
  #  sys.exit(1)
  #
  # Begin at the "Start" shape
  #start_shape = visio_get_shape_by_name(page0,start_name)
  #
  # Traverse all connections beneath the "Start" shape
  #visited_list = []
  #visit_shape_connections(start_shape,visited_list)

  # Show connections to all objects
  print("\nShowing all shape connections:")
  for shape in all_shapes:
    visio_get_shape_connections(shape)

  # End of program