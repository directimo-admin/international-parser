from datetime import datetime

from condoparser.jpa import db


class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bathroom_no = db.Column(db.Integer)
    construction_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    current_price = db.Column(db.Numeric)
    description = db.Column(db.UnicodeText)
    room_no = db.Column(db.Integer)
    terase_usable_area = db.Column(db.Numeric)
    usable_area = db.Column(db.Numeric)
    mongo_id = db.Column(db.String(100))
    url = db.Column(db.String(200))
    offer_status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    source_id = db.Column(db.Integer, db.ForeignKey('source.id'),
                          nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('offer.id'))
    condo_id = db.Column(db.Integer, db.ForeignKey('condo.id'),
                         nullable=False)
    record_status_id = db.Column(db.Integer, db.ForeignKey('status.id'),
                                 nullable=False)

    def __init__(
            self,
            id=None,
            bathroom_no=None,
            construction_date=None,
            current_price=None,
            description=None,
            room_no=None,
            terase_usable_area=None,
            usable_area=None,
            url=None,
            created_at=None,
            updated_at=None,
            source_id=None,
            parent_id=None,
            condo_id=None,
            record_status_id=None,
            offer_status_id=None,
            mongo_id=None):
        self.id = id
        self.bathroom_no = bathroom_no
        self.construction_date = construction_date
        self.current_price = current_price
        self.description = description
        self.room_no = room_no
        self.terase_usable_area = terase_usable_area
        self.usable_area = usable_area
        self.url = url
        self.created_at = created_at
        self.updated_at = updated_at
        self.record_status_id = record_status_id
        self.offer_status_id = offer_status_id
        self.source_id = source_id
        self.parent_id = parent_id
        self.condo_id = condo_id
        self.mongo_id = mongo_id
