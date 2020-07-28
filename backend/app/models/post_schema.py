from marshmallow_mongoengine import ModelSchema
from .post import Post


class PostSchema(ModelSchema):
    class Meta:
        model = Post
