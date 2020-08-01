from flask import request
from flask_restful import Resource, reqparse
from resources.errors import InternalServerError
from representations.user import CreateUserRequestSchema


class UserResource(Resource):
    def __init__(self,  **kwargs):
        self.user_service = kwargs['user_service']

    def get(self, id):
        post = self.user_service.get_by_id(id=id)
        return post, 200


class UsersResource(Resource):
    def __init__(self,  **kwargs):
        self.user_service = kwargs['user_service']
        self.create_user_request_schema = CreateUserRequestSchema()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type=str)

    def get(self):
        args = self.reqparse.parse_args()
        email = args['email']
        user = self.user_service.get_by_email_id(email)
        return user, 200

    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {'message': 'No input data provided'}, 400
        create_user_request, errors = self.create_user_request_schema.load(json_data)
        if errors:
            return errors, 400
        try:
            user = self.user_service.create(create_user_request)
            return user, 200
        except Exception:
            raise InternalServerError