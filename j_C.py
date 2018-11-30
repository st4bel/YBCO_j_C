import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
#x=[]
#y=[]

#lol=list(csv.reader(open("S088_U(I)_B7_6mA.txt","rt"), delimiter="\t"))
#for row in lol:
#    if len(row) > 1:
#        x.append(float(row[0]))
#        y.append(float(row[1]))


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

def j_C_lin_pol(x,V_0,V_1,I_c):
    #V_0: Offset, V_1: lin Anteil, V_c: Spannung bei der I_c bestimmt wird (10µV), I_c: kritische Stromdichte, n: poly. Grad
    return V_0 + (V_1 * x) + 10*np.power((x / I_c ),11)




filename = "S088_U(I)_B7_6mA.txt"
xdata, ydata = readfile(filename)
#print(getOffset(content))
#content = correctOffset(offset=getOffset(content)["zeros"], csv=content)

popt, pcov = curve_fit(j_C_lin_pol, xdata, ydata)#, bounds=([-.1,-1,.004],[0,1,.006]))
print(popt)

xrange = np.linspace(np.amin(xdata),np.amax(xdata),100)

plt.plot(xrange,j_C_lin_pol(xrange,*popt),"--g",label="fit: V_0=%5.3f, V_1=%5.3f, I_c=%5.3f" % tuple(popt))


p11 = np.poly1d(np.polyfit(xdata, ydata,11))
plt.plot(xdata,p11(xdata),"-r",label="n=11")

plt.plot(xdata,ydata, ".b", label="U(I)")
plt.plot(xrange,[popt[0]+10]*100,"--b")
plt.plot([popt[2]]*2,[np.amin(ydata),np.amax(ydata)], "--b")

#plt.plot(content["x"],j_C_lin_pol(content["x"],*popt), "-r", label = "fit: V_0=%5.3f, V_1=%5.3f, V_c=%5.3f, I_c=%5.3f, n=%5.3f" % tuple(popt))
plt.xlabel('I in mA')
plt.ylabel('U in uV')
plt.title(filename)
plt.legend()
plt.grid(which="both",axis="both")
#plt.savefig("test.png")
plt.show()
