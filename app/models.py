from app import db

class Document(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(64))

    def __repr__(self):
        return "<Document {}>".format(self.filename)
