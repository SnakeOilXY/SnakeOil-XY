"""
Run with FreeCAD's bundled interpreter, or as a FreeCAD macro
"""
import os
from typing import Dict, List, Union
if os.name == 'nt':
    FREECADPATH = os.getenv('FREECADPATH', 'C:/Program Files/FreeCAD 0.20/bin')
else:
    FREECADPATH = os.getenv('FREECADPATH', '/usr/lib/freecad-python3/lib/')
import sys
sys.path.append(FREECADPATH)
from pathlib import Path
import sys
import FreeCAD as App  # type: ignore
import FreeCADGui as Gui  # type: ignore
import logging
from lib import BOM, STL, CAD

logging.basicConfig(
    format='%(levelname)s: %(message)s', level=logging.INFO
    )
LOGGER = logging.getLogger()

BASE_PATH = Path(os.path.dirname(__file__))
SNAKEOIL_PROJECT_PATH = BASE_PATH.parent.parent.parent
CAD_FILE = SNAKEOIL_PROJECT_PATH / 'CAD/v1-180-assembly.FCStd'
# Use EXTRA_CAD_FILES to find colors of parts not in the main assembly
EXTRA_CAD_FILES = [
    SNAKEOIL_PROJECT_PATH / 'WIP/component-assembly/toolhead-carrier-sherpa-1515-assembly.FCStd',
    SNAKEOIL_PROJECT_PATH / 'WIP/component-assembly/top-lid-assembly.FCStd',
    SNAKEOIL_PROJECT_PATH / 'WIP/component-assembly/sherpa-mini-assembly.FCStd',
    SNAKEOIL_PROJECT_PATH / 'WIP/component-assembly/bottom-panel-250-assembly.FCStd',
    SNAKEOIL_PROJECT_PATH / 'WIP/component-assembly/4PR-assembly.FCStd',
    SNAKEOIL_PROJECT_PATH / 'WIP/E-axis/sherpa-mini.FCStd',
]
STL_PATHS = [
    SNAKEOIL_PROJECT_PATH / 'BETA3_Standard_Release_STL' / 'STLs',
    SNAKEOIL_PROJECT_PATH / 'BETA3_4PR_Release_STL' / 'STLs',
    # SNAKEOIL_PROJECT_PATH / 'BETA3_Standard_Release_STL' / 'STLs',
]
# Convert to relative paths
STL_PATHS = [x.relative_to(SNAKEOIL_PROJECT_PATH) for x in STL_PATHS]
# Ignore STL files in these directories
STL_EXCLUDE_DIRS = [
    (SNAKEOIL_PROJECT_PATH / "BETA3_Standard_Release_STL/STLs/Add-on"),
    (SNAKEOIL_PROJECT_PATH / "BETA3_Standard_Release_STL/STLs/Tools"),
    (SNAKEOIL_PROJECT_PATH / "BETA3_Standard_Release_STL/STLs/Panels/Bottom-panel/alt"),
    (SNAKEOIL_PROJECT_PATH / "BETA3_Standard_Release_STL/STLs/Z-axis/alt"),
]
# Convert to relative paths
STL_EXCLUDE_DIRS = [x.relative_to(SNAKEOIL_PROJECT_PATH) for x in STL_EXCLUDE_DIRS]
STL_EXCLUDE_STRINGS = [
    "OPTIONAL"
]

def generate_bom(cad_parts):
    """Builds bom from CAD objects and writes bom-*.json files"""
    BOM.get_bom_from_freecad_document(cad_parts)
    # Add custom fasteners (not in CAD)
    BOM.add_fasteners()
    # Write all BOM files
    BOM.write_bom_files()

def generate_filename_color_reports(cad_parts, use_cache):
    """Builds filename color reports and writes to color-results-*.txt"""
    # List all CAD objects by main and accent colors
    if not use_cache:
        with open(CAD.MD5_COLOR_CACHE_FILE, 'w') as file:
            file.write('{}')
            file.flush()
            os.fsync(file)
    stl_files = []
    for stl_path in STL_PATHS:
        stl_files += STL.get_stl_files(SNAKEOIL_PROJECT_PATH, stl_path, STL_EXCLUDE_DIRS, STL_EXCLUDE_STRINGS)
    filename_results = CAD.get_filename_color_results(stl_files, cad_parts)
    STL.write_file_color_reports(filename_results)
    return filename_results

def add_part_colors_to_stl_file_names(filename_results: Dict[str, Union[List[Path], List[str]]]):
    for color, prepend_str in CAD.COLOR_PREPEND_KEYS.items():
        for fp in filename_results[color]:
            if issubclass(type(fp), Path):
                filename = fp.name  # type: ignore
                # Strip any existing colors from filenames
                if True in [x for x in CAD.COLOR_PREPEND_KEYS.values() if filename.startswith(x)]:
                    filename = filename[2:]
                new_name = fp.with_name(f"{prepend_str}{filename}")  # type: ignore
                os.rename(fp, new_name)
            else:
                raise Exception(f"file name result is not a valid Path type: {fp}")


if __name__ == '__main__':
    # Get assembly object from filepath
    CACHE = True
    cad_parts = CAD.get_cad_parts_from_file(CAD_FILE, CACHE)
    extra_cad_parts = []
    for extra_cad_file in EXTRA_CAD_FILES:
        this_cad_parts = CAD.get_cad_parts_from_file(extra_cad_file, True)
        extra_cad_parts += this_cad_parts
    # Generate bom-*.json files
    generate_bom(cad_parts)
    # Generate color-results-*.txt files
    filename_results = generate_filename_color_reports(cad_parts + extra_cad_parts, False)
    add_part_colors_to_stl_file_names(filename_results)
