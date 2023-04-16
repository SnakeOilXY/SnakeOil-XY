"""
Run with FreeCAD's bundled interpreter, or as a FreeCAD macro

Settings can be found in ./lib/settings.py
"""
import os
if os.name == 'nt':
    FREECADPATH = os.getenv('FREECADPATH', 'C:/Program Files/FreeCAD 0.20/bin')
else:
    FREECADPATH = os.getenv('FREECADPATH', '/usr/lib/freecad-python3/lib/')
import sys
sys.path.append(FREECADPATH)
import logging
from lib import CAD, settings, actions

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
LOGGER = logging.getLogger()

if __name__ == '__main__':
    # Get assembly object from filepath
    cad_parts = CAD.get_cad_parts_from_file(settings.CAD_FILE, settings.USE_CACHE)
    # Generate bom-*.json files
    actions.generate_bom(cad_parts)
