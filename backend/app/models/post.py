from mongoengine import (Document,
                         ReferenceField,
                         StringField,
                         IntField,
                         ListField,
                         EmbeddedDocumentField,
                         CASCADE)
from .park import Park
from .location import Location
from .user import User


class Post(Document):
    created_at = IntField(required=True)
    title = StringField(required=True)
    description = StringField(required=True)
    image_id = StringField(required=True)
    tags = ListField(StringField(max_length=30))
    user = ReferenceField(User, required=True, reverse_delete_rule=CASCADE)
    park = ReferenceField(Park, required=True, reverse_delete_rule=CASCADE)
    location = EmbeddedDocumentField(Location)
