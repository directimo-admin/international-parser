import json


class UpdatedOffer():
    def __init__(self, url, *updates):
        self.url = url
        self.updates = updates

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Update():
    def __init__(self, fieldName, oldValue, newValue):
        self.fieldName = fieldName
        self.oldValue = oldValue
        self.newValue = newValue
