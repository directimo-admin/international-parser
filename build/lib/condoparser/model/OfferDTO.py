import datetime

from condoparser.jpa.Offer import Offer


class OfferDTO():
    __slots__ = (
        'name',
        'url',
        'current_price',
        'description',
        'room_no',
        'usable_area',
        'bathroom_no',
        'construction_date',
        'terase_usable_area',
        'html_id',
        'sql_id')

    def __init__(
            self,
            name,
            url,
            current_price=None,
            description=None,
            room_no=None,
            usable_area=None,
            bathroom_no=None,
            construction_date=None,
            terase_usable_area=None,
            html_id=None,
            sql_id=None):
        self.name = name
        self.url = url
        self.current_price = current_price
        self.description = description
        self.room_no = room_no
        self.usable_area = usable_area
        self.terase_usable_area = terase_usable_area
        self.bathroom_no = bathroom_no
        self.construction_date = construction_date
        self.html_id = html_id
        self.sql_id = sql_id

    def slotted_to_dict(obj):
        return {s: getattr(obj, s) for s in obj.__slots__ if hasattr(obj, s)}

    def toJpa(self, status, source, parent_id, condo_id):
        obj = Offer()
        obj.bathroom_no = self['bathroom_no']
        obj.construction_date = datetime.datetime(
            self['construction_date'],
            1,
            1) if self['construction_date'] is not None else None
        obj.current_price = self['current_price']
        obj.description = self['description']
        obj.room_no = self['room_no']
        obj.terase_usable_area = self['terase_usable_area']
        obj.usable_area = self['usable_area']
        obj.url = self['url']
        obj.source_id = source.id
        obj.record_status_id = status.id
        obj.parent_id = parent_id
        obj.condo_id = condo_id

        return obj
