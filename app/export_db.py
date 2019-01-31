import os
import csv
from app.models import Substrate, Bridge

def export_substrate_to_dict(substratename,text=[]):
    substrate = Substrate.query.filter_by(substratename=substratename).first()
    bridges = Bridge.query.filter_by(substrate=substrate).order_by(Bridge.bridgename).all()
    text.append(["Substrate:"]+[substrate.substratename])
    text.append(["YBCO Layer in nm:"]+[substrate.YBCO_layer])
    text.append(["Au Layer in nm:"]+[substrate.Au_layer])
    text.append(["Bridgename"]+["I_C in mA"]+["Bridgewidth in px"])
    for bridge in bridges:
        if bridge.j_C != None or bridge.bridgewitdh != None:
            text.append([bridge.bridgename]+[str(bridge.j_C).replace(".",",")]+[str(bridge.bridgewitdh).replace(".",",")])
    return text

def dict_to_csv(csvname,text,delimiter=";"):
    with open(csvname,"w") as csvfile:
        writer=csv.writer(csvfile,delimiter=delimiter)
        writer.writerows(text)
