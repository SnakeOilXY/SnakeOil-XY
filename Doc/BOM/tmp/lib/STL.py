"""
Run with FreeCAD's bundled interpreter, or as a FreeCAD macro
"""
import logging
import os
import re
if os.name == 'nt':
    FREECADPATH = os.getenv('FREECADPATH', 'C:/Program Files/FreeCAD 0.20/bin')
else:
    FREECADPATH = os.getenv('FREECADPATH', '/usr/lib/freecad-python3/lib/')
import sys
sys.path.append(FREECADPATH)
from pathlib import Path
import sys
from typing import Dict, List, Union
from lib import CAD
from difflib import SequenceMatcher

logging.basicConfig(
    # filename='generateBom.log', filemode='w', 
    format='%(levelname)s: %(message)s', level=logging.INFO
    )
LOGGER = logging.getLogger()

BASE_PATH = Path(os.path.dirname(__file__)).parent

def filter_stl_files(stl_files: List[Path], exclude_dirs: List[Path] = [], exclude_strings: List[str] = []):
    filtered_stl_files = []
    for file in stl_files:
        keep = True
        for excluded_fp in exclude_dirs:
            if str(file).startswith(str(excluded_fp)):
                keep = False
        for excluded_str in exclude_strings:
            if excluded_str.lower() in str(file).lower():
                keep = False
        # Ignore if filename already has a part color
        if re.match(CAD.part_color_pattern, file.name):
            keep = False
        if keep == True:
            filtered_stl_files.append(file)
    return filtered_stl_files

def get_stl_files(snakeoil_project_path: Path, target_stl_path: Path, 
                  exclude_dirs: List[Path] = [], exclude_strings: List[str] = []) -> List[Path]:
    stl_files = [x.relative_to(snakeoil_project_path) for x in snakeoil_project_path.glob(f"{target_stl_path}/**/*.stl")]
    stl_files = filter_stl_files(stl_files, exclude_dirs, exclude_strings)
    LOGGER.info(f"# Found {len(stl_files)} stl files")
    return stl_files

def write_file_color_reports(filename_results: Dict[str, Union[List[Path], List[str]]]):
    for category, results in filename_results.items():
        with open(BASE_PATH / f'color-results-{category}.txt', 'w') as file:
            if not results:
                continue
            if issubclass(type(results[0]), Path):
                formatted_results: List[str] = [x.as_posix() for x in results]  # type: ignore
            elif type(results[0]) is str:
                formatted_results = [str(x) for x in results]
            else:
                raise TypeError(f"Results must be str or Path, found {type(results[0])}")
            sorted_results = sorted(formatted_results)
            file.write('\n'.join(sorted_results))