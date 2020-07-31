from marshmallow import Schema, fields, post_load


class User:
    def __init__(self, id: str, name: str, email: str, image_id: str, role: str):
        self.id = id
        self.name = name
        self.email = email
        self.image_id = image_id
        self.user_type = role


class UserSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    email = fields.Email()
    image_id = fields.Str()
    role = fields.Str()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


class CreateUserRequest:
    def __init__(self, name: str, email: str, image_id: str, role: str):
        self.name = name
        self.email = email
        self.image_id = image_id
        self.role = role


class CreateUserRequestSchema(Schema):
    name = fields.Str()
    email = fields.Email()
    image_id = fields.Str()
    role = fields.Str()

    @post_load
    def make_create_user_request(self, data, **kwargs):
        return CreateUserRequest(**data)