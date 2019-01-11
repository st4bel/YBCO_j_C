import csv
import matplotlib.pyplot as plt
import numpy as np
from app import app
import os
from app.models import *

def filepath(filename):
    return os.path.join(app.config["UPLOAD_FOLDER"],filename)

def plotpath(filename, extension=".png"):
    return os.path.join(app.config["PLOT_FOLDER"],filename + extension)

def readfile(filepath, u_amp=1000):
    x=np.array([])
    y=np.array([])

    lol=list(csv.reader(open(filepath,"rt"), delimiter="\t"))
    for row in lol:
        if len(row) == 1:
            header = row[0]
        elif len(row) > 1:
            x=np.append(x,[float(row[0])*1000])
            y=np.append(y,[float(row[1])*u_amp])
    return x,y

def solve_for_y(pcoeff, y=0):
    pcopy = pcoeff.copy()
    pcopy[-1] -= y
    return np.roots(pcopy)

def solve_for_y_real(pcoeff,y):
    roots = np.array(solve_for_y(pcoeff, y))
    realroots = np.array([])
    for root in roots:
        if root.imag == 0:
            realroots = np.append(realroots, [root.real])
    return realroots

def filter_roots_by_range(roots,min,max):
    froots = np.array([])
    for root in roots:
        if min < root and root < max:
            froots = np.append(froots,[root])
    return froots

def ohmig_res(xdata,ydata):
    #getting outmost turning points of the tier 11 polynom
    p=np.poly1d(np.polyfit(xdata,ydata,11))
    d2p=p.deriv(2)
    roots=d2p.r
    cut=np.logical_and(xdata>=np.amin(roots),xdata<=np.amax(roots))
    xcut = xdata[cut]
    ycut = ydata[cut]

    #polyfit for n=1
    p1 = np.polyfit(xcut,ycut,1)

    return p1

def calculate_ohmig_res(xdata, ydata, j_C):
    permutation = xdata.argsort()
    xsorted = xdata[permutation]
    ysorted = ydata[permutation]
    #cutting x and y to -j_C/2 <= x <= j_C/2
    cut = np.logical_and(xdata>=-j_C/2,xdata<=j_C/2)
    xcut = xdata[cut]
    ycut = ydata[cut]

    #polyfit for n=1
    p1 = np.polyfit(xcut,ycut,1)
    return p1

def close_plot():
    plt.close()

def show_plot():
    plt.show()
    plt.close()

def plot_file(filename):
    file = Document.query.filter_by(filename=filename).first()
    xdata, ydata = readfile(filepath = filepath(filename), u_amp = file.amplification)
    plt.plot(xdata,ydata,".b",label="U(I), amplification = "+str(file.amplification))
    plt.xlabel("I in mA")
    plt.ylabel("U in uV")
    plt.legend()
    plt.grid(which="both",axis="both")
    plt.savefig(plotpath(filename,"_plot.png"))

def plot_j_C(filename):
    file = Document.query.filter_by(filename=filename).first()
    xdata, ydata = readfile(filepath = filepath(filename), u_amp = file.amplification)
    xrange = np.linspace(np.amin(xdata),np.amax(xdata),100)
    p11 =  np.polyfit(xdata, ydata,11)
    if file.remove_offset ==True:
        for i in range(0,len(ydata)):
            ydata[i] -= p11[-1]

    if file.remove_ohm:
        ohmic_res_p1 = ohmig_res(xdata,ydata)
        for i in range(0,len(ydata)):
            ydata[i] -= ohmic_res_p1[0]*xdata[i]

    p11 = np.polyfit(xdata,ydata,11)
    p = np.poly1d(p11)
    roots = solve_for_y_real(p11, p11[-1]+10)
    froots = filter_roots_by_range(roots = roots, min = np.amin(xdata), max = np.amax(xdata))
    ohmic_res_p1 = ohmig_res(xdata,ydata)

    #discrete derivate
    #dy = np.zeros(xrange.shape,np.float)
    #dy[0:-1] = np.diff(p(xrange))/np.diff(xrange)
    #dy[-1] = dy[-2]

    #d2y = np.zeros(xrange.shape,np.float)
    #d2y[0:-1] = np.diff(dy)/np.diff(xrange)
    #d2y[-1] = d2y[-2]

    plt.plot(xdata,ydata, ".b", label="U(I), amplification "+str(file.amplification))

    plt.plot(xrange,p(xrange),"-r",label="polyfit: n=11")

    plt.plot(xrange,[p11[-1]+10]*100,"--r")
    if len(froots)==1:
        plt.plot([froots[0]]*2,[np.amin(ydata),np.amax(ydata)],"--r", label = "j_C = %.3fmA"%froots[0])

    plt.plot(xrange,ohmic_res_p1[0]*xrange+ohmic_res_p1[-1],"--g", label = "R = %.5fmOhm"%ohmic_res_p1[0])
    #plt.plot(xrange,dy,"--y", label = "derivate of p11")
    #plt.plot(xrange,d2y,"g", label = "2nd derivate of p11")
    plt.xlabel('I in mA')
    plt.ylabel('U in uV')
    plt.legend()
    plt.grid(which="both",axis="both")

    plt.savefig(plotpath(filename,"_j_C.png"))
