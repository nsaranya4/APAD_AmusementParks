from mongoengine import (Document,
                         ReferenceField,
                         StringField,
                         EmbeddedDocumentField)
from .park import Park
from .location import Location
from .user import User


class Post(Document):
    name = StringField(required=True, unique=True)
    title = StringField(required=True)
    description = StringField(required=True)
    image_id = StringField(required=True)
    user = ReferenceField(User, required=True)
    park = ReferenceField(Park, required=True)
    location = EmbeddedDocumentField(Location)
