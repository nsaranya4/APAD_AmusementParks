from marshmallow import Schema, fields, post_load
from representations.location import Location, LocationSchema
from representations.user import User, UserSchema
from representations.park import Park, ParkSchema


class Post:
    def __init__(self, id: str, title: str, description: str,
                 image_id: str, tags: [str], user: User, park: Park,
                 location: Location):
        self.id = id
        self.title = title
        self.description = description
        self.image_id = image_id
        self.tags = tags
        self.user = user
        self.park = park
        self.location = location


class PostSchema(Schema):
    id = fields.Str()
    title = fields.Str()
    description = fields.Str()
    image_id = fields.Str()
    tags = fields.List(fields.Str())
    user = fields.Nested(UserSchema)
    park = fields.Nested(ParkSchema)
    location = fields.Nested(LocationSchema)


    @post_load
    def make_post(self, data, **kwargs):
        return Post(**data)


class CreatePostRequest:
    def __init__(self, title: str, description: str,
                 image_id: str, tags: [str], user_id: str, park_id: str,
                 location: Location):
        self.title = title
        self.description = description
        self.image_id = image_id
        self.tags = tags
        self.user_id = user_id
        self.park_id = park_id
        self.location = location


class CreatePostRequestSchema(Schema):
    title = fields.Str()
    description = fields.Str()
    image_id = fields.Str()
    tags = fields.List(fields.Str())
    user_id = fields.Str()
    park_id = fields.Str()
    location = fields.Nested(LocationSchema)


    @post_load
    def make_create_post_Request(self, data, **kwargs):
        return CreatePostRequest(**data)
