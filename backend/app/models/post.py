from mongoengine import (Document,
                         ReferenceField,
                         StringField,
                         ListField,
                         EmbeddedDocumentField)
from .park import Park
from .location import Location
from .user import User


class Post(Document):
    title = StringField(required=True)
    description = StringField(required=True)
    image_id = StringField(required=True)
    tags = ListField(StringField(max_length=30))
    user = ReferenceField(User, required=True)
    park = ReferenceField(Park, required=True)
    location = EmbeddedDocumentField(Location)
