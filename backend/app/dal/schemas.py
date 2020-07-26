from marshmallow_mongoengine import ModelSchema
from .models import Park


class ParkSchema(ModelSchema):
    class Meta:
        model = Park
