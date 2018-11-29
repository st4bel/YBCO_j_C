import numpy as np
import csv

def readfile(filename):
    x=[]
    y=[]

    lol=list(csv.reader(open(filename,"rt"), delimiter="\t"))
    for row in lol:
        if len(row) == 1:
            header = row[0]
        elif len(row) > 1:
            x.append(float(row[0]))
            y.append(float(row[1]))
    return [x,y]


filename = "S088_U(I)_B7_6mA.txt"
content = readfile(filename)
np.savetxt("data.txt",content, delimiter=",")
