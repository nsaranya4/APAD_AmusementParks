from marshmallow_mongoengine import ModelSchema
from .park import Park


class ParkSchema(ModelSchema):
    class Meta:
        model = Park
