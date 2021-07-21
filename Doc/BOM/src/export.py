import datetime


fileList = ["bom-header.md", "bom-frame.md",
            "bom-fasterner.md", "bom-motion.md", "bom-electronic.md","bom-panel.md", "bom-other.md"]

lines = []
for targetFile in fileList:
    print("read file :", targetFile)
    with open(targetFile, 'r') as tmpFile:
        tmpData = tmpFile.readlines()
        lines.extend(tmpData)

with open("../README.md", 'w') as outputFile:
    outputFile.write("".join(lines).replace(
        "{#@lastUpdated}", datetime.datetime.now().astimezone().replace(microsecond=0).isoformat(), -1))
    print("Done!")
