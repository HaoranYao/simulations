import csv
import os
import sys
import shutil
import random

def genSizeFile(name, size):
    filePath = name
    i = 0
    with open(filePath, "w", encoding="utf8") as file:
        while i < size:
            file.write(str(random.randint(0,9)))
            i = i + 1
        file.close()
    # print(os.path.getsize(filePath))

print("Writing files from list %s " % sys.argv[1])

with open(sys.argv[1], "r") as fileName:
    reader = csv.reader(fileName)
    fileSize = [row[4] for row in reader][1:]
    fileSize = list(map(int, fileSize))

    # print(fileSize)
if os.path.exists(r"./fileResult"):
    shutil.rmtree("./fileResult")

os.mkdir(r'./fileResult')

os.chdir(r'./fileResult')

for j in fileSize:
    genSizeFile(str(j), j)
