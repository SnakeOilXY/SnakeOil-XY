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

def generate_bom(cad_parts):
    """Builds bom from CAD objects and writes bom-*.json files"""
    BOM.get_bom_from_freecad_document(cad_parts)
    # Add custom fasteners (not in CAD)
    BOM.add_fasteners()
    # Write all BOM files
    BOM.write_bom_files()

def generate_filename_color_reports(
        cad_parts, use_cache, stl_paths, snakeoil_project_path, 
        stl_exclude_dirs, stl_exclude_strings
        ):
    """Builds filename color reports and writes to color-results-*.txt"""
    # List all CAD objects by main and accent colors
    if not use_cache:
        with open(CAD.MD5_COLOR_CACHE_FILE, 'w') as file:
            file.write('{}')
            file.flush()
            os.fsync(file)
    stl_files = []
    for stl_path in stl_paths:
        stl_files += STL.get_stl_files(snakeoil_project_path, stl_path, stl_exclude_dirs, stl_exclude_strings)
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