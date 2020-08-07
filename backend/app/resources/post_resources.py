from flask import request
from flask_restful import Resource, reqparse
from resources.errors import InternalServerError
from representations.post import CreatePostRequestSchema
from .errors import BadRequestError, EntityNotFoundError


class PostResource(Resource):
    def __init__(self, **kwargs):
        self.post_service = kwargs['post_service']

    def get(self, id):
        post, error = self.post_service.get_by_id(id=id)
        if error is not None:
            return None, 500
        elif post is None:
            return None, 404
        else:
            return post, 200
        

    def delete(self, id):
        post, error = self.post_service.delete_by_id(id=id)
        if error is not None and error == BadRequestError:
            return None, 400
        elif error is not None:
            return None, 500
        else:
            return None, 204


class PostsResource(Resource):
    def __init__(self,  **kwargs):
        self.post_service = kwargs['post_service']
        self.create_post_request_schema = CreatePostRequestSchema()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('offset', type=int, required=True)
        self.reqparse.add_argument('limit', type=int, required=True)
        self.reqparse.add_argument('user_id', type=str)
        self.reqparse.add_argument('park_id', type=str)
        self.reqparse.add_argument('tag', type=str)

    def get(self):
        args = self.reqparse.parse_args()
        offset = args['offset']
        limit = args['limit']
        filters = {}
        if args['user_id'] is not None:
            filters['user_id'] = args['user_id']
        if args['park_id'] is not None:
            filters['park_id'] = args['park_id']
        if args['tag'] is not None:
            filters['tag'] = args['tag']
        posts = self.post_service.get_batch(offset, limit, filters)
        return posts, 200

    def post(self):
        json_data = request.get_json()

        if not json_data:
            return {'message': 'No input data provided'}, 400
        create_post_request, errors = self.create_post_request_schema.load(json_data)
        if errors:
            return errors, 400

        try:
            post, error = self.post_service.create(create_post_request)
            if error is not None:
                return None, 500
            else:
                return post, 200

        except Exception:
            raise InternalServerError
