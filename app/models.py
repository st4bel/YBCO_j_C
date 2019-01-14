from app import db

class Document(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    bridge_id = db.Column(db.Integer, db.ForeignKey("bridge.id"))
    filename = db.Column(db.String(64))
    remove_offset = db.Column(db.Boolean,default=False)
    remove_ohm = db.Column(db.Boolean,default=False)
    amplification = db.Column(db.Integer, default = 1000)
    j_C = db.Column(db.Float)
    res = db.Column(db.Float)

    def __repr__(self):
        return "<Document {}>".format(self.filename)

class Substrate(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    substratename = db.Column(db.String(32))
    Au_layer = db.Column(db.Integer)
    YBCO_layer = db.Column(db.Integer)

    bridges = db.relationship("Bridge", backref = "substrate", lazy="dynamic")

    def __repr__(self):
        return "<Substrate {}>".format(self.substratename)

class Bridge(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    substrate_id = db.Column(db.Integer, db.ForeignKey("substrate.id"))
    bridgename = db.Column(db.String(32))
    j_C = db.Column(db.Float)
    res = db.Column(db.Float)

    documents = db.relationship("Document", backref = "bridge", lazy = "dynamic")

    def __repr__(self):
        return "<Bridge {}>".format(self.bridgename)
