import cv2
import os
import numpy as np
from scipy.signal import argrelextrema
from matplotlib import pyplot as plt
from app.j_C_intern import plotpath, filepath
from app.models import Picture, Bridge

#def plotpath(filename, extension=".png"):
#    return os.path.join(app.config["PLOT_FOLDER"],filename + extension)

#def filepath(filename):
#    return os.path.join(app.config["UPLOAD_FOLDER"],filename)

def findlocalmaxima(profile,schwellwert = 10):
    maxima=[]
    for x in np.arange(1,len(profile)-1):
        if profile[x] >= profile[x-1] and profile[x] >= profile[x+1] and profile[x] >= schwellwert:
            maxima.append(x)
    return maxima

def get_size(fpath):# [y, x]
    img=cv2.imread(fpath)
    return [np.size(img,0),np.size(img,1)]


def read_blur_image(filename):
    img = cv2.imread(filepath(filename))
    imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(imgray,(9,9),0)
    return blur

def cut_image(filename,x,y,w,h):
    img = cv2.imread(filepath(filename))
    cut = img[y:y+h,x:x+w]
    cut.save(plotpath(filename,"_cut.png"))

def plot_picture(filename,cut=False):
    picture = Picture.query.filter_by(filename=filename).first()
    if cut:
        img = cv2.imread(plotpath(filename,"_cut.png"))
    else:
        img = cv2.imread(plotpath(filename))
    imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(imgray,(picture.brushsize,picture.brushsize),0)

    ret,th = cv2.threshold(blur,picture.threshold,255,cv2.THRESH_TOZERO_INV)

    smalestgap = np.size(img,0)
    gapprofile = []
    for x in range(np.size(img,1)):
        profile = th[0:np.size(img,0),x]
        maxima = findlocalmaxima(profile)
        if len(maxima)>=2:
            diffmaxima = maxima[len(maxima)-1]-maxima[0]
            gapprofile.append(diffmaxima)
            if diffmaxima<smalestgap:
                smalestgap=diffmaxima
                position = [(x,maxima[len(maxima)-1]),(x,maxima[0])]
                bestprofile = profile
        else:
            gapprofile.append(np.size(img,0))
    for center in position:
        cv2.circle(img,center,10,(0,0,255),2)
    picture.pixelwidth = smalestgap
    plt.subplot(2,2,1),plt.plot(bestprofile)
    plt.ylabel("gray 0-255")
    plt.xlabel("y-position in px")
    plt.title("best profile")
    plt.subplot(2,2,2),plt.plot(gapprofile)
    plt.ylabel("gapdistance in px")
    plt.xlabel("x-position in px")
    plt.title("gapdistance over x")
    plt.subplot(2,2,3),plt.imshow(img)
    plt.subplot(2,2,4),plt.imshow(th)
    plt.savefig(plotpath(filename,"_4er.png"))
