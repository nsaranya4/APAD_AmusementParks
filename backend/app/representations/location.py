from marshmallow import Schema, fields, post_load


class Location:
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng


class LocationSchema(Schema):
    lat = fields.Float()
    lng = fields.Float()

    @post_load
    def make_location(self, data, **kwargs):
        return Location(**data)

