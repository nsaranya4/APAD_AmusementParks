from mongoengine import Document, StringField, EmailField


class User(Document):
    name = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    image_id = StringField(required=True)
    role = StringField(required=True)
