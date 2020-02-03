import sys
import csv

with open(sys.argv[1], "r") as fileName:
    reader = csv.reader(fileName)
    fileSize = [row[4] for row in reader][1:]
    fileSize = list(map(int, fileSize))
    with open("pathResult", "w") as pathResult:
        for item in fileSize:
            pathResult.write("fileResult/" + str(item) + "\n")




