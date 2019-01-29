import os
import re
from app import app
from flask import flash
from app.models import *
from app.j_C_intern import filepath, plotpath


def deleteFile(filename):
    file=Document.query.filter_by(filename = filename).first()
    db.session.delete(file)
    db.session.commit()
    os.remove(filepath(filename))
    if os.path.isfile(plotpath(filename,"_plot.png")):
        os.remove(plotpath(filename,"_plot.png"))
    if os.path.isfile(plotpath(filename,"_j_C.png")):
        os.remove(plotpath(filename,"_j_C.png"))
    flash("removed all Files of: "+filename)

def deletePicture(filename):
    picture = Picture.query.filter_by(filename=filename).first()
    db.session.delete(picture)
    db.session.commit()
    os.remove(filepath(filename))
    if os.path.isfile(plotpath(filename,"_cut.png")):
        os.remove(plotpath(filename,"_cut.png"))
    if os.path.isfile(plotpath(filename,"_4er.png")):
        os.remove(plotpath(filename,"_4er.png"))
    flash("removed all Files of: "+filename)

def detect_substrate_bridge(filename):
    splits = filename[:-4].split("_")#".txt" wegschneiden
    v=None
    for split in splits:
        if re.match(r"[S][0-9]+([a-z])?",split):
            s=split
        elif re.match(r"[A-B][1-9]",split):
            b=split
        elif re.match(r"[V][0-9]",split):
            v=int(split[1:])
    file = Document.query.filter_by(filename=filename).first()
    substrate = Substrate.query.filter_by(substratename=s).first()
    if substrate == None:
        substrate = Substrate(substratename=s)
    bridge = Bridge.query.filter_by(bridgename=s+"_"+b).first()
    if bridge==None:
        bridge = Bridge(bridgename=s+"_"+b)
        bridge.substrate=substrate
    file.bridge=bridge
    if v == 100:
        file.amplification=10000
    elif v==10:
        file.amplification=100000
    else:
        file.amplification=1000
    db.session.add(file)
    db.session.add(substrate)
    db.session.add(bridge)
    db.session.commit()

def detect_picture_amp(filename):
    splits = filename[:-4].split("_")
    for split in splits:
        if re.match(r"[S][0-9]+([a-z])?",split):
            s=split
        elif re.match(r"[A-B][1-9]",split):
            b=split
        elif re.match(r"[0-9]+[x]?",split):
            v=re.sub("[a-z]+","", split)# removing the x if present
    picture = Picture.query.filter_by(filename=filename).first()
    substrate = Substrate.query.filter_by(substratename=s).first()
    if substrate == None:
        substrate = Substrate(substratename=s)
    bridge = Bridge.query.filter_by(bridgename=s+"_"+b).first()
    if bridge==None:
        bridge = Bridge(bridgename=s+"_"+b)
        bridge.substrate=substrate
    picture.bridge=bridge
    if v != None:
        picture.amplification = app.config["SCALE_50"] if int(v)==50 else app.config["SCALE_100"]
    else:
        picture.amplification=app.config["SCALE_100"]
    picture.threshold = app.config["THRESHOLD_START"]
    picture.brushsize = app.config["BRUSHSIZE_START"]
    db.session.add(substrate)
    db.session.add(bridge)
    db.session.add(picture)
    db.session.commit()
