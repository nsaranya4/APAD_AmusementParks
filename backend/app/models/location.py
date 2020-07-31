from mongoengine import EmbeddedDocument, FloatField


class Location(EmbeddedDocument):
    lat = FloatField(required=True)
    lng = FloatField(required=True)
