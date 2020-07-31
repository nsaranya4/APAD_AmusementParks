from marshmallow import Schema, fields, post_load
from .location import Location, LocationSchema
from .user import User, UserSchema


class Park:
    def __init__(self, id: str, name: str, description: str, image_id: str, user: User, location: Location):
        self.id = id
        self.name = name
        self.description = description
        self.image_id = image_id
        self.user = user
        self.location = location


class ParkSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    description = fields.Str()
    image_id = fields.Str()
    user = fields.Nested(UserSchema)
    location = fields.Nested(LocationSchema)

    @post_load
    def make_park(self, data, **kwargs):
        return Park(**data)


class CreateParkRequest:
    def __init__(self, name: str, description: str, image_id: str, user_id: str, location: Location):
        self.name = name
        self.description = description
        self.image_id = image_id
        self.user_id = user_id
        self.location = location


class CreateParkRequestSchema(Schema):
    name = fields.Str()
    description = fields.Str()
    image_id = fields.Str()
    user_id = fields.Str()
    location = fields.Nested(LocationSchema)

    @post_load
    def make_create_park_request(self, data, **kwargs):
        return CreateParkRequest(**data)