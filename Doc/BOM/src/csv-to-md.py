INPUT_FILE = "bolt-bom.csv"

data = []

logFile = open(INPUT_FILE, 'r')
data = logFile.readlines()

for line in data:
    lineSeg = line.replace("\n","").split(",")
    print("|",lineSeg[0],"|",lineSeg[1],"|",lineSeg[2], "|")