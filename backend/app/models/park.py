from mongoengine import (Document,
                         ReferenceField,
                         StringField,
                         IntField,
                         EmbeddedDocumentField,
                         CASCADE)
from .location import Location
from .user import User


class Park(Document):
    created_at = IntField(required=True)
    name = StringField(required=True, unique=True)
    image_id = StringField(required=True)
    description = StringField(required=True)
    user = ReferenceField(User, required=True, reverse_delete_rule=CASCADE)
    location = EmbeddedDocumentField(Location)

