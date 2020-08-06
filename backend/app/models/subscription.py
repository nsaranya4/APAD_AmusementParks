from mongoengine import Document, ReferenceField, CASCADE
from .park import Park
from .user import User


class Subscription(Document):
    user = ReferenceField(User, required=True, reverse_delete_rule=CASCADE)
    park = ReferenceField(Park, required=True, reverse_delete_rule=CASCADE)
