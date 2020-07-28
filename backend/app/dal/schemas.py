from marshmallow_mongoengine import ModelSchema
from .models import Park
from .models import Post


class ParkSchema(ModelSchema):
    class Meta:
        model = Park


class PostSchema(ModelSchema):
    class Meta:
        model = Post
