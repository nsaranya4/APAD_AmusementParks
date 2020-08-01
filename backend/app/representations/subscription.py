from marshmallow import Schema, fields, post_load
from representations.user import User, UserSchema
from representations.park import Park, ParkSchema


class Subscription:
    def __init__(self, id: str, user: User, park: Park):
        self.id = id
        self.user = user
        self.park = park


class SubscriptionSchema(Schema):
    id = fields.Str()
    user = fields.Nested(UserSchema)
    park = fields.Nested(ParkSchema)


    @post_load
    def make_subscription(self, data, **kwargs):
        return Subscription(**data)


class CreateSubscriptionRequest:
    def __init__(self, user_id: str, park_id: str):
        self.user_id = user_id
        self.park_id = park_id


class CreateSubscriptionRequestSchema(Schema):
    user_id = fields.Str()
    park_id = fields.Str()


    @post_load
    def make_create_subscription_request(self, data, **kwargs):
        return CreateSubscriptionRequest(**data)


