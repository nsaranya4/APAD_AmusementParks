from mongoengine import Document, ReferenceField
from .park import Park
from .user import User


class Subscription(Document):
    user = ReferenceField(User, required=True)
    park = ReferenceField(Park, required=True)
