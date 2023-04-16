from enum import Enum
import json
import logging
import os
from pathlib import Path
from typing import List
# from lib.CAD import (BomItem, PRINTED_MAIN, PRINTED_ACCENT, FASTENER, OTHER)
from lib import CAD

logging.basicConfig(
    # filename='generateBom.log', filemode='w', 
    format='%(levelname)s: %(message)s', level=logging.INFO
    )
BASE_PATH = Path(os.path.dirname(__file__))
LOGGER = logging.getLogger()
bom_out_dir = Path(BASE_PATH).parent

def get_new_bom():
    """Use this factory to get a new empty BOM dict"""
    _bom = {}
    for partType in CAD.BOM_ITEM_TYPES:
        _bom[partType] = {}
    return _bom

# Create new BOM dictionaries
bom = get_new_bom()
detail_bom = get_new_bom()
# Quick references
fasteners_bom = bom[CAD.FASTENER]
printed_bom = bom[CAD.PRINTED_MAIN]
printed_accent_bom = bom[CAD.PRINTED_ACCENT]
other_bom = bom[CAD.OTHER]

def _add_to_main_bom(bomItem: CAD.BomItem):
    targetBom = bom[bomItem.bom_item_type]
    if bomItem.name in targetBom.keys():
        targetBom[bomItem.name] += 1
    else:
        targetBom[bomItem.name] = 1

def _add_to_detailed_bom(bomItem: CAD.BomItem):
    documentName = bomItem.document
    if documentName not in detail_bom.keys():
        detail_bom[documentName] = get_new_bom()
    targetDetailBom = detail_bom[documentName][bomItem.bom_item_type]
    if bomItem.name in targetDetailBom.keys():
        targetDetailBom[bomItem.name] += 1
    else:
        targetDetailBom[bomItem.name] = 1

def get_bom_from_freecad_document(bom_items: List[CAD.BomItem]):
    for bomItem in bom_items:
        _add_to_main_bom(bomItem)
        _add_to_detailed_bom(bomItem)

def addCustomfFastener(fastenerName, count):
    if fastenerName in fasteners_bom.keys():
        fasteners_bom[fastenerName] += count
    else:
        fasteners_bom[fastenerName] = count

def sort_dictionary_recursive(dictionary):
    sortedDict = {}
    for i in sorted(dictionary):
        val = dictionary[i]
        if type(val) is dict:
            val = sort_dictionary_recursive(val)
        sortedDict[i] = val
    return sortedDict

def write_bom_to_file(target_file_name, bomContent):
    # sort dict
    sortedDict = sort_dictionary_recursive(bomContent)
    filePath = bom_out_dir.joinpath(target_file_name)
    LOGGER.info(f"# Writing to {target_file_name}")
    # Sort dictionary alphabetically by key
    with open(filePath, 'w') as bom_file:
        bom_file.write(json.dumps(sortedDict, indent=2))

def add_fasteners():
    # add custom Fasteners that not in the assembly
    # spring washer for rails mount
    addCustomfFastener("Spring washer M3", 60)
    # bolts for 3030 extrusion rails mount
    addCustomfFastener("Socket head M3x10-Screw", 50)
    # bolts for 1515 extrusion rail mount
    addCustomfFastener("Socket head M3x8-Screw", 10)
    # T-nut for 1515 gantry and bed
    addCustomfFastener("Square M3-Nut", 30)
    # count 3030 M6 T-nut = M6 bolt
    m6NutCount = 0
    for fastenersName in fasteners_bom.keys():
        if "Screw" in fastenersName and "M6" in fastenersName:
            m6NutCount += fasteners_bom[fastenersName]
    addCustomfFastener("3030 M6-T-nut", m6NutCount)
    # 3030 M3 t-nut (50 for rails, 10 for other add-ons)
    addCustomfFastener("3030 M3-T-nut", 60)
    # 3030 M5 t-nut for z motor mount and others
    addCustomfFastener("3030 M5-T-nut", 10)

def write_bom_files():
    # Write to files
    write_bom_to_file('bom-all.json', bom)
    write_bom_to_file('bom-fasteners.json', fasteners_bom)
    write_bom_to_file('bom-printed-parts.json', {
        'printed (main color)': printed_bom, 
        'printed (accent color)': printed_accent_bom
        })
    write_bom_to_file('bom-detail.json', detail_bom)
    write_bom_to_file('bom-other.json', other_bom)

global parts_dict
parts_dict = None