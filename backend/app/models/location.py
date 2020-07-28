from repos.db import db


class Location(db.EmbeddedDocument):
    lat = db.FloatField(required=True)
    lng = db.FloatField(required=True)