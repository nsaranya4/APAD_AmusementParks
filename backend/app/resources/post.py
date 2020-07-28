from flask import request
from flask_restful import Resource, reqparse
from dal.models import Post as PostModel
from dal.schemas import PostSchema
from resources.errors import InternalServerError

post_schema = PostSchema()
posts_schema = PostSchema(many=True)


class Post(Resource):

    def get(self, id):
        post = PostModel.objects.get_or_404(id=id)
        return post_schema.dump(post).data, 200


class Posts(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('offset', type=int, required=True)
        self.reqparse.add_argument('limit', type=int, required=True)
        super(Posts, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        offset = args['offset']
        limit = args['limit']
        # TODO figure out how to use pagination while querying mongodb
        posts = PostModel.objects()
        postlist = posts_schema.dump(posts).data
        return {'posts': postlist}, 200

    def post(self):
        json_data = request.get_json()

        if not json_data:
            return {'message': 'No input data provided'}, 400
        post, errors = post_schema.load(json_data)
        if errors:
            return errors, 400

        try:
            post.save()
            return post_schema.dump(post).data, 200
        except Exception:
            raise InternalServerError
