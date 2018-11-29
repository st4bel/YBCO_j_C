import csv
import matplotlib.pyplot as plt
import numpy as np

#x=[]
#y=[]

#lol=list(csv.reader(open("S088_U(I)_B7_6mA.txt","rt"), delimiter="\t"))
#for row in lol:
#    if len(row) > 1:
#        x.append(float(row[0]))
#        y.append(float(row[1]))


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
    return {"header":header,"x":x,"y":y}

def getOffset(csv):
    offset_from_average = np.mean(csv["y"])
    zeros = []
    for i in range(0,len(csv["x"])):
        if csv["x"][i]==0:
            zeros.append(csv["y"][i])
    offset_from_zero = np.mean(zeros)
    return {"average":offset_from_average,"zeros":offset_from_zero}

def correctOffset(csv,offset):
    for i in range(0,len(csv["y"])):
        csv["y"][i]-=offset
    return csv



filename = "S088_U(I)_B7_6mA.txt"
content = readfile(filename)
print(getOffset(content))
content = correctOffset(offset=getOffset(content)["zeros"], csv=content)


plt.plot(content["x"],content["y"],label="U(I)")
plt.xlabel('x')
plt.ylabel('y')
plt.title(filename)
plt.legend()
#plt.savefig("test.png")
plt.show()
