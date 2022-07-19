from condoparser.jpa.Condo import Condo


class CondoDTO(object):
    __slots__ = ('name', 'url', 'offers', 'details', 'sql_id', 'zone')

    def __init__(
            self,
            name,
            url,
            *offers,
            details=None,
            sql_id=None,
            zone=None):
        self.name = name
        self.url = url
        self.offers = offers
        self.details = details
        self.sql_id = sql_id
        self.zone = zone

    def slotted_to_dict(obj):
        return {s: getattr(obj, s) for s in obj.__slots__ if hasattr(obj, s)}

    def toJpa(self, status, source, mongoId):
        obj = Condo()
        obj.name = self['name']
        obj.zone = self['zone']
        obj.url = self['url']
        obj.record_status_id = status.id
        obj.source_id = source.id
        obj.details = self['details']
        obj.mongo_id = mongoId
        return obj
