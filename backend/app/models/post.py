from repos.db import db
from .location import Location


class Post(db.Document):
    name = db.StringField(required=True, unique=True)
    title = db.StringField(required=True)
    description = db.StringField(required=True)
    image_id = db.StringField(required=True)
    user_id = db.StringField(required=True)
    park_id = db.StringField(required=True)
    location = db.EmbeddedDocumentField(Location)
    tags = db.ListField(db.StringField(),required=True)
    

