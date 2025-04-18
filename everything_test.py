import os
from classes.external.everything import Everything, Request

import struct
print(struct.calcsize("P") * 8)

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# Join with the DLL filename to get the full path
dll_path = os.path.join(script_dir, "Everything64.dll")
# Initialize Everything with the full path to the DLL
everything = Everything(dll_path)
# sets the search options
everything.set_search('everything')
everything.set_request_flags(Request.FullPathAndFileName|Request.DateModified|Request.Size)
# starts the search
if not everything.query():
    raise Exception(everything.get_last_error())
# prints all results
for item in everything:
    print(
        item.get_filename(),
        f'Size: {item.get_size()} Bytes',
        f'Modified date: {item.get_date_modified()}',
        '', sep='\n'
    )
