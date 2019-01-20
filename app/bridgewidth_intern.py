import cv2
import os
import numpy as np
from scipy.signal import argrelextrema
from matplotlib import pyplot as plt
from util import *

def plotpath(filename, extension=".png"):
    return os.path.join(app.config["PLOT_FOLDER"],filename + extension)

def filepath(filename):
    return os.path.join(app.config["UPLOAD_FOLDER"],filename)

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
    cut.save(plotpath(filename,"_cut.bmp"))

def plot_picture(filename,threshold=100,brush=9,cut=False):
    if cut:
        img = cv2.imread(plotpath(filename,"_cut.bmp"))
    else:
        img = cv2.imread(filepath(filename))
    imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(imgray,(brush,brush),0)

    ret,th = cv2.threshold(blur,threshold,255,cv2.THRESH_TOZERO_INV)

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


img = cv2.imread("a9x50geschnitten.png")
imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(imgray,(9,9),0)
ret,th = cv2.threshold(blur,120,255,cv2.THRESH_TOZERO_INV)

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
    cv2.circle(img,center,10,(0,0,255),5)
print(smalestgap)

print(findlocalmaxima(bestprofile))

plt.subplot(2,2,1),plt.plot(bestprofile)
plt.ylabel("gray")
plt.xlabel("y-position")
plt.title("best profile")
plt.subplot(2,2,2),plt.plot(gapprofile)
plt.ylabel("gapdistance")
plt.xlabel("x-position")
plt.title("gapdistance over x")
plt.subplot(2,2,3),plt.imshow(img)
plt.subplot(2,2,4),plt.imshow(th)
plt.show()
