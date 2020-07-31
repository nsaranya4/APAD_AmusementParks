from mongoengine import (Document,
                         ReferenceField,
                         StringField,
                         EmbeddedDocumentField)
from .location import Location
from .user import User


class Park(Document):
    name = StringField(required=True, unique=True)
    image_id = StringField(required=True)
    description = StringField(required=True)
    user = ReferenceField(User, required=True)
    location = EmbeddedDocumentField(Location)
