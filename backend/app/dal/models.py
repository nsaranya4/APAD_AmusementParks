from .db import db


class Location(db.EmbeddedDocument):
    lat = db.FloatField(required=True)
    lng = db.FloatField(required=True)


class Park(db.Document):
    name = db.StringField(required=True, unique=True)
    image_id = db.StringField(required=True)
    description = db.StringField(required=True)
    user_id = db.StringField(required=True)
    location = db.EmbeddedDocumentField(Location)

class Post(db.Document):
    name = db.StringField(required=True, unique=True)
    title = db.StringField(required=True)
    description = db.StringField(required=True)
    image_id = db.StringField(required=True)
    user_id = db.StringField(required=True)
    park_id = db.StringField(required=True)
    location = db.EmbeddedDocumentField(Location)
