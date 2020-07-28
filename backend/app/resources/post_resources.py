from flask import request
from flask_restful import Resource, reqparse
from repos.post_repo import PostRepo
from models.post import Post
from models.post_schema import PostSchema
from resources.errors import InternalServerError

post_schema = PostSchema()
posts_schema = PostSchema(many=True)


class PostResource(Resource):
    def __init__(self, **kwargs):
        self.post_repo = kwargs['post_repo']

    def get(self, id):
        post = self.post_repo.get_by_id(id=id)
        return post_schema.dump(post).data, 200


class PostsResource(Resource):
    def __init__(self,  **kwargs):
        self.post_repo = kwargs['post_repo']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('offset', type=int, required=True)
        self.reqparse.add_argument('limit', type=int, required=True)

    def get(self):
        args = self.reqparse.parse_args()
        offset = args['offset']
        limit = args['limit']
        posts = self.post_repo.get_batch(offset, limit)
        return {'posts': posts_schema.dump(posts).data}, 200

    def post(self):
        json_data = request.get_json()

        if not json_data:
            return {'message': 'No input data provided'}, 400
        post, errors = post_schema.load(json_data)
        if errors:
            return errors, 400

        try:
            post = self.post_repo.create(post)
            return post_schema.dump(post).data, 200
        except Exception:
            raise InternalServerError
