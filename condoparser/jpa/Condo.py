from datetime import datetime

from condoparser.jpa import db


class Condo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    details = db.Column(db.UnicodeText)
    name = db.Column(db.String(100))
    zone = db.Column(db.String(100))
    url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    condo_status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    source_id = db.Column(db.Integer, db.ForeignKey('source.id'),
                          nullable=False)
    record_status_id = db.Column(db.Integer, db.ForeignKey('status.id'),
                                 nullable=False)
    mongo_id = db.Column(db.String(100))

    def __init__(
            self,
            id=None,
            details=None,
            name=None,
            url=None,
            condo_status_id=None,
            source_id=None,
            created_at=None,
            updated_at=None,
            record_status_id=None,
            mongo_id=None,
            zone=None):
        self.id = id
        self.details = details
        self.name = name
        self.url = url
        self.condo_status_id = condo_status_id
        self.source_id = source_id
        self.updated_at = updated_at
        self.created_at = created_at
        self.record_status_id = record_status_id
        self.mongo_id = mongo_id
        self.zone = zone
