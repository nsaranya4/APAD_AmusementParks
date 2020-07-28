from flask import request
from flask_restful import Resource, reqparse
from models.user_schema import UserSchema
from resources.errors import InternalServerError

user_schema = UserSchema()


class UserResource(Resource):
    def __init__(self,  **kwargs):
        self.user_repo = kwargs['user_repo']
        self.reqparse = reqparse.RequestParser()
    

    def post(self):
        json_data = request.get_json()

        if not json_data:
            return {'message': 'No input data provided'}, 400
        user, errors = user_schema.load(json_data)
        if errors:
            return errors, 400

        try:
            user = self.user_repo.create(user)
            return user_schema.dump(user).data, 200
        except Exception:
            raise InternalServerError