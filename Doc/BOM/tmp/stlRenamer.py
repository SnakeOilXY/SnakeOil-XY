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
    extra_cad_parts = []
    for extra_cad_file in settings.EXTRA_CAD_FILES:
        this_cad_parts = CAD.get_cad_parts_from_file(extra_cad_file, True)
        extra_cad_parts += this_cad_parts
    # Generate color-results-*.txt files
    filename_results = actions.generate_filename_color_reports(
        cad_parts=cad_parts + extra_cad_parts, 
        use_cache=settings.USE_CACHE,
        stl_paths=settings.STL_PATHS,
        snakeoil_project_path=settings.SNAKEOIL_PROJECT_PATH,
        stl_exclude_dirs=settings.STL_EXCLUDE_DIRS,
        stl_exclude_strings=settings.STL_EXCLUDE_STRINGS
        )
    actions.add_part_colors_to_stl_file_names(filename_results)
