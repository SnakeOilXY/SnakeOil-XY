

result = []


def appendIfNotExist(data):
    for item in result:
        if item["name"] == data["name"]:
            item["count"] = item["count"] + data["count"]
            return True
    result.append(data)
    return False

def replaceName(inp):
    nameDict = [
        {
            "src":"ISO4762",
            "dest":"Socket head"
        },
        {
            "src":"ISO7380-1",
            "dest":"Button head"
        },
        {
            "src":"ISO4026",
            "dest":"Grub"
        },
        {
            "src":"ISO4032",
            "dest":"Hex"
        },
        {
            "src":"ISO7092",
            "dest":"Small size"
        },
        {
            "src":"ISO7093-1",
            "dest":"Big size"
        },
        {
            "src":"ISO7089",
            "dest":"Standard size"
        },
        {
            "src":"ISO7090",
            "dest":"Standard size"
        },
    ]

    for target in nameDict:
        inp = inp.replace(target["src"],target["dest"])

    return inp


with open("bolt.csv") as sourceFile:
    lines = sourceFile.readlines()

    multiplier = 1
    for line in lines:
        if line[0] == "#":
            multiplier = float(line.split(",")[1])
        elif line != ",\n" and line != "\n" and line != "" and line != "Type,Qty\n":
            segments = line.replace("\n", "").split(",")
            print(segments)
            tmpData = {
                "name": segments[0],
                "count": float(segments[1]) * multiplier
            }
            appendIfNotExist(tmpData)

# count m6 screw -> m6 T nut
m6TnutCount = 0
for item in result:
    if "Screw M6" in item["name"]:
        m6TnutCount = m6TnutCount + item["count"]
appendIfNotExist({"name": "M6 T-nut","count": m6TnutCount})

with open('result.md', 'w') as resultFile:
    resultFile.write("| Item | Quantity | Description |\n")
    resultFile.write("|---|---|---|\n")
    for item in result:
        resultFile.write("|" + replaceName(item["name"]) + "|" + str(item["count"])+"|  |\n")
