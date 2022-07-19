from condoparser.jpa import db


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True)

    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name
