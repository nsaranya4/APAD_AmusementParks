from mongoengine import Document, IntField, ReferenceField, CASCADE
from .park import Park
from .user import User


class Subscription(Document):
    created_at = IntField(required=True)
    user = ReferenceField(User, required=True, reverse_delete_rule=CASCADE)
    park = ReferenceField(Park, required=True, reverse_delete_rule=CASCADE)
