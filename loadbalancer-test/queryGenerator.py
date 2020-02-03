import sys
import csv

pathResult= open("pathResult", "w")
with open(sys.argv[1], "r") as fileName:
    reader = csv.reader(fileName)
    infos = [(row[4],row[7]) for row in reader if len(row) >=8][1:]
    for fsize,duration in infos:
        pathResult.write("/wait/?fsize="+str(float(fsize) / 1024)+"&duration="+str(float(duration)*1000000)+"&time=1000\n")




