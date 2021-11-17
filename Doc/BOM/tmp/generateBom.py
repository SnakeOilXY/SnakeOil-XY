"""
Run with FreeCAD's bundled interpreter.

Example:
    "C:/Program Files/FreeCAD 0.19/bin/python.exe" generate-bom.py
"""

from pathlib import Path
import re
import FreeCAD
import json
import FreeCADGui as Gui

# Gui.setupWithoutGUI()

# This is cross-platform now as long as the script is in the project directory
# target_file = Path(__file__).parent.joinpath('CAD/v1-180-assembly.FCStd')
# for appImage
target_file = '/home/chip/Data/Code/SnakeOil-XY/CAD/v1-180-assembly.FCStd'
# Regex pattern to match all fasteners
fastener_pattern = re.compile('.*-(Screw|Washer|HeatSet|Nut)')
bom = {'fasteners': {}, 'other': {}, 'detail': {}}
fasteners_bom = bom['fasteners']
other_bom = bom['other']
detail_bom = bom['detail']
type_dictionary = {}  # for debugging purposes


def add_detailBom(fastenerName, otherName, parentPartName):
    if parentPartName not in detail_bom.keys():
        detail_bom[parentPartName] = {'fasteners': {}, 'other': {}}
    targetDetailBom = detail_bom[parentPartName]

    if fastenerName != None:
        if fastenerName in targetDetailBom['fasteners'].keys():
            targetDetailBom['fasteners'][fastenerName] += 1
        else:
            targetDetailBom['fasteners'][fastenerName] = 1
    if otherName != None:
        if otherName in targetDetailBom['other'].keys():
            targetDetailBom['other'][otherName] += 1
        else:
            targetDetailBom['other'][otherName] = 1


def add_fastener_to_bom(part, parentPartName):

    fastener = part.Label
    # Prepare fastener string to be added to BOM
    # ISO type with descriptive name
    if hasattr(part, 'type'):
        if part.type == "ISO4762":
            fastener = f"Socket head {fastener}"
        if part.type == "ISO7380-1":
            fastener = f"Button head {fastener}"
        if part.type == "ISO4026":
            fastener = f"Grub {fastener}"
        if part.type == "ISO4032":
            fastener = f"Hex {fastener}"
        if part.type == "ISO7092":
            fastener = f"Small size {fastener}"
        if part.type == "ISO7093-1":
            fastener = f"Big size {fastener}"
        if part.type == "ISO7089":
            fastener = f"Standard size {fastener}"
        if part.type == "ISO7090":
            fastener = f"Standard size {fastener}"
    # Remove numbers at end if they exist (e.g. 'M3-Washer004' becomes 'M3-Washer')
    while fastener[-1].isnumeric():
        fastener = fastener[:-1]

    if fastener in fasteners_bom.keys():
        fasteners_bom[fastener] += 1
    else:
        fasteners_bom[fastener] = 1

    # add fastener to detail bom
    add_detailBom(fastener, None, parentPartName)


def add_other_part_to_bom(part, parentPartName):
    part_name = part.Label

    while part_name[-1].isnumeric() or part_name[-1] == '-':
        part_name = part_name[:-1]
    if part_name in other_bom.keys():
        other_bom[part_name] += 1
    else:
        other_bom[part_name] = 1
    # add fastener to detail bom
    add_detailBom(None, part_name, parentPartName)


def get_bom_from_freecad_document(assembly: FreeCAD.Document):
    print("# Getting parts of", assembly.Label)
    parts = []
    # Get parts from this document
    parts += [x for x in assembly.Objects if x.TypeId.startswith('Part::')]
    for part in parts:
        # print("\tFound part", part.Label)
        # [debugging] Add type to dictionary so we can see which parts we want to add or filter out
        type_dictionary[part.Label] = part.TypeId
        # If fastener matches, add it to BOM
        if fastener_pattern.match(part.Label):
            add_fastener_to_bom(part, assembly.Label)
        else:
            add_other_part_to_bom(part, assembly.Label)
    # Recurse through each linked file
    for linked_file in assembly.findObjects("App::Link"):
        print("# Getting fasteners from", linked_file.Name)
        get_bom_from_freecad_document(linked_file.LinkedObject.Document)


def addCustomfFastener(fastenerName, count):
    if fastenerName in fasteners_bom.keys():
        fasteners_bom[fastenerName] += count
    else:
        fasteners_bom[fastenerName] = count


print(f"# Getting fasteners from {target_file}")
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
# 3030 M3 t-nut (50 for rails, 10 for other add-onds)
addCustomfFastener("3030 M3-T-nut", 60)
# 3030 M5 t-nut for z motor mount and others
addCustomfFastener("3030 M5-T-nut", 10)


# Pretty print BOM dictionary
# print(json.dumps(bom, indent=4))

# sort fasteners_bom
sortedFastenersDict = {}
for i in sorted(fasteners_bom):
    sortedFastenersDict[i] = fasteners_bom[i]
fasteners_bom = sortedFastenersDict

with open('bom-fasteners.json', 'w') as file:
    file.write(json.dumps(fasteners_bom, indent=4))

with open('bom-detail.json', 'w') as file:
    file.write(json.dumps(detail_bom, indent=4))

print("# completed!")
