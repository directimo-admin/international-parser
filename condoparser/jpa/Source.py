from condoparser.jpa import db


class Source(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True)

    url = db.Column(db.String(200), unique=True)
    config = db.Column(db.JSON)

    def __init__(self, id=None, name=None, url=None, config=None):
        self.id = id
        self.name = name
        self.url = url
        self.config = config
