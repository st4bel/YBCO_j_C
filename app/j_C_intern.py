import csv
import matplotlib.pyplot as plt
import numpy as np

def readfile(filename):
    x=np.array([])
    y=np.array([])

    lol=list(csv.reader(open(filename,"rt"), delimiter="\t"))
    for row in lol:
        if len(row) == 1:
            header = row[0]
        elif len(row) > 1:
            x=np.append(x,[float(row[0])*1000])
            y=np.append(y,[float(row[1])*1000])
    return x,y

def plot
