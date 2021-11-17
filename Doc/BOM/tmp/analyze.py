
import json

bom = {}

with open('bom-fasteners.json', 'r') as sourceFile:
    bom = json.load(sourceFile)

print(json.dumps(bom, indent=4))

with open('result.md', 'w') as resultFile:
    resultFile.write("| Item | Quantity | Description |\n")
    resultFile.write("|---|---|---|\n")
    for item in bom.keys():
        resultFile.write("|" + item + "|" + str(bom[item])+"|  |\n")
