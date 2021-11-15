from pathlib import Path
import os
import sys
import re
from pprint import pprint

if FreeCAD.ActiveDocument == None:
    print("Err : No active document")
else:
    for obj in FreeCAD.ActiveDocument.Objects:
        pprint(obj)
