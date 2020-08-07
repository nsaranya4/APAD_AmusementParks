from flask import request
from flask_restful import Resource, reqparse
from representations.park import ParkSchema, CreateParkRequestSchema
from resources.errors import InternalServerError, BadRequestError


class ParkResource(Resource):
    def __init__(self,  **kwargs):
        self.park_service = kwargs['park_service']

    def get(self, id: str):
        park, error = self.park_service.get_by_id(id)
        if error is not None:
            return None, 500
        elif park is None:
            return None, 404
        else:
            return park, 200
    
    def delete(self, id: str):
        park, error = self.park_service.delete_by_id(id)
        if error is not None and error == BadRequestError:
            return None, 400
        elif error is not None:
            return None, 500
        else:
            return None, 204


class ParksResource(Resource):
    def __init__(self,  **kwargs):
        self.park_service = kwargs['park_service']
        self.create_park_request_schema = CreateParkRequestSchema()
        self.park_schema = ParkSchema()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('offset', type=int, required=True)
        self.reqparse.add_argument('limit', type=int, required=True)
        self.reqparse.add_argument('user_id', type=str)

    def get(self):
        args = self.reqparse.parse_args()
        offset = args['offset']
        limit = args['limit']
        filters = {}
        if args['user_id'] is not None:
            filters['user_id'] = args['user_id']
        parks = self.park_service.get_batch(offset, limit, filters)
        return parks, 200

    def post(self):
        json_data = request.get_json()

        if not json_data:
            return {'message': 'No input data provided'}, 400
        create_park_request, errors = self.create_park_request_schema.load(json_data)
        if errors:
            return errors, 400

        try:
            park, error = self.park_service.create(create_park_request)
            if error is not None:
                return None, 500            
            else:
                return park, 200

        except Exception:
            raise InternalServerError
