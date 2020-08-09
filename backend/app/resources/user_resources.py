from flask import request
from flask_restful import Resource, reqparse
from resources.errors import InternalServerError
from representations.user import CreateUserRequestSchema
from .errors import BadRequestError, EntityNotFoundError


class UserResource(Resource):
    def __init__(self,  **kwargs):
        self.user_service = kwargs['user_service']

    def get(self, id):
        user, error = self.user_service.get_by_id(id=id)
        if error is not None:
            return None, 500
        elif user is None:
            return None, 404
        else:
            return user, 200

    def delete(self, id):
        user, error = self.user_service.delete_by_id(id=id)
        if error is not None and error == BadRequestError:
            return None, 400
        elif error is not None:
            return None, 500
        else:
            return None, 204


class UsersResource(Resource):
    def __init__(self,  **kwargs):
        self.user_service = kwargs['user_service']
        self.create_user_request_schema = CreateUserRequestSchema()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type=str)

    def get(self):
        args = self.reqparse.parse_args()
        email = args['email']
        user, error = self.user_service.get_by_email_id(email)
        if error is not None:
            return None, 500
        elif user is None:
            return None, 404
        else:
            return user, 200

    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {'message': 'No input data provided'}, 400
        create_user_request, errors = self.create_user_request_schema.load(json_data)
        if errors:
            return errors, 400
        try:
            user, error = self.user_service.create(create_user_request)
            if error is not None:
                return None, 500
            else:
                return user, 200
                
        except Exception:
            raise InternalServerError
