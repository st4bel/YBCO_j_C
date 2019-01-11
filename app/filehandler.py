import os
from flask import flash


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
    
