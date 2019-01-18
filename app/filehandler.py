import os
import re
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

def detect_substrate_bridge(filename):
    splits = filename[:-4].split("_")#".txt" wegschneiden
    v=None
    for split in splits:
        if re.match(r"[S][0-9]+([a-z])?",split):
            s=split
        elif re.match(r"[A-B][1-9]",split):
            b=split
        elif re.match(r"[V][0-9]",split):
            v=split
    file = Document.query.filter_by(filename=filename).first()
    substrate = Substrate.query.filter_by(substratename=s).first()
    if substrate == None:
        substrate = Substrate(substratename=s)
    bridge = Bridge.query.filter_by(bridgename=s+"_"+b).first()
    if bridge==None:
        bridge = Bridge(bridgename=s+"_"+b)
    file.bridge=bridge
    bridge.substrate=substrate
    if v != None:
        file.amplification=int(v[1:])
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
    # TODO: 
