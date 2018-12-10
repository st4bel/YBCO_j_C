from app import db

class Document(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(64))
    remove_offset = db.Column(db.Boolean,default=False)
    remove_ohm = db.Column(db.Boolean,default=False)


    def __repr__(self):
        return "<Document {}>".format(self.filename)
