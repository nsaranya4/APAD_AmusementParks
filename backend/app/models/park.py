from repos.db import db
from .location import Location


class Park(db.Document):
    name = db.StringField(required=True, unique=True)
    image_id = db.StringField(required=True)
    description = db.StringField(required=True)
    user_id = db.StringField(required=True)
    location = db.EmbeddedDocumentField(Location)
