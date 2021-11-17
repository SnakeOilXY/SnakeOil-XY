"""
Run with FreeCAD's bundled interpreter, or as a FreeCAD macro
"""
from pathlib import Path
import re
import FreeCAD
import json
import os
import FreeCADGui as Gui
from dataclasses import dataclass, field
from enum import Enum

# Open GUI if running from console, otherwise we know we are running from a macro
if hasattr(Gui, 'showMainWindow'):
    Gui.showMainWindow()
else:
    print("Running as macro")

# Use SNAKEOIL_PROJECT_PATH environment variable if exists, else default to @Chip's directory
SNAKEOIL_PROJECT_PATH = os.getenv('SNAKEOIL_PROJECT_PATH', '/home/chip/Data/Code/SnakeOil-XY/')
target_file = Path(SNAKEOIL_PROJECT_PATH).joinpath('CAD/v1-180-assembly.FCStd')
bom_out_dir = Path(SNAKEOIL_PROJECT_PATH).joinpath('Doc/BOM/tmp')
# Regex pattern to match all fasteners
fastener_pattern = re.compile('.*-(Screw|Washer|HeatSet|Nut)')
# If a shape color in this list, the object will be treated as a printed part
printed_parts_colors = [
    (0.3333333432674408, 1.0, 1.0, 0.0),  # Teal
    (0.6666666865348816, 0.6666666865348816, 1.0, 0.0),  # Blue
]

# Quick references to BOM part types.  Also provides type hinting in the BomPart dataclass
PRINTED = "printed"
FASTENER = "fastener"
OTHER = "other"
BomItemType = Enum('BomItemType', [PRINTED, FASTENER, OTHER])


def get_new_bom():
    """Use this factory to get a new empty BOM dict"""
    _bom = {}
    for partType in BomItemType:
        _bom[partType.name] = {}
    return _bom


# Create new BOM dictionaries
bom = get_new_bom()
detail_bom = get_new_bom()
# Quick references
fasteners_bom = bom[FASTENER]
printed_bom = bom[PRINTED]
other_bom = bom[OTHER]


@dataclass
class BomItem:
    part: FreeCAD.Part  # Reference to FreeCAD part object
    type: BomItemType  # What type of BOM entry (printed, fastener, other)
    name: str = field(init=False)  # We'll get the name from the part.label in the __post_init__ function

    def __post_init__(self):
        self.name = self.part.Label
        # Remove numbers at end if they exist (e.g. 'M3-Washer004' becomes 'M3-Washer')
        while self.name[-1].isnumeric():
            self.name = self.name[:-1]
        # Add descriptive fastener names
        if self.type == FASTENER:
            if hasattr(self.part, 'type'):
                if self.part.type == "ISO4762":
                    self.name = f"Socket head {self.name}"
                if self.part.type == "ISO7380-1":
                    self.name = f"Button head {self.name}"
                if self.part.type == "ISO4026":
                    self.name = f"Grub {self.name}"
                if self.part.type == "ISO4032":
                    self.name = f"Hex {self.name}"
                if self.part.type == "ISO7092":
                    self.name = f"Small size {self.name}"
                if self.part.type == "ISO7093-1":
                    self.name = f"Big size {self.name}"
                if self.part.type == "ISO7089":
                    self.name = f"Standard size {self.name}"
                if self.part.type == "ISO7090":
                    self.name = f"Standard size {self.name}"


def _add_to_main_bom(bomItem: BomItem):
    targetBom = bom[bomItem.type]
    if bomItem.name in targetBom.keys():
        targetBom[bomItem.name] += 1
    else:
        targetBom[bomItem.name] = 1


def _add_to_detailed_bom(bomItem: BomItem):
    parentPartName = bomItem.part.Document.Label
    if parentPartName not in detail_bom.keys():
        detail_bom[parentPartName] = get_new_bom()
    targetDetailBom = detail_bom[parentPartName][bomItem.type]
    if bomItem.name in targetDetailBom.keys():
        targetDetailBom[bomItem.name] += 1
    else:
        targetDetailBom[bomItem.name] = 1


def add_to_bom(part: FreeCAD.Part):
    # Sort parts by type
    if fastener_pattern.match(part.Label):
        bomItem = BomItem(part, FASTENER)
    elif part.ViewObject.ShapeColor in printed_parts_colors:
        bomItem = BomItem(part, PRINTED)
    else:
        bomItem = BomItem(part, OTHER)
    _add_to_main_bom(bomItem)
    _add_to_detailed_bom(bomItem)


def get_bom_from_freecad_document(assembly: FreeCAD.Document):
    print("# Getting parts of", assembly.Label)
    for part in [x for x in assembly.Objects if x.TypeId.startswith('Part::')]:
        add_to_bom(part)
    # Recurse through each linked file
    for linked_file in assembly.findObjects("App::Link"):
        print("# Getting fasteners from", linked_file.Name)
        get_bom_from_freecad_document(linked_file.LinkedObject.Document)


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
    print(f"# Writing to {target_file_name}")
    # Sort dictionary alphabetically by key
    with open(filePath, 'w') as bom_file:
        bom_file.write(json.dumps(sortedDict, indent=2))


print(f"# Getting BOM from {target_file}")
# Get assembly object from filepath
cad_assembly = FreeCAD.open(str(target_file))
get_bom_from_freecad_document(cad_assembly)

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

# Write to files
write_bom_to_file('bom-all.json', bom)
write_bom_to_file('bom-fasteners.json', fasteners_bom)
write_bom_to_file('bom-printed-parts.json', printed_bom)
write_bom_to_file('bom-detail.json', detail_bom)
write_bom_to_file('bom-other.json', other_bom)

print("# completed!")
