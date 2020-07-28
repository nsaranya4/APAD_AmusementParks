from flask import request
from flask_restful import Resource, reqparse
from models.park_schema import ParkSchema
from resources.errors import InternalServerError

park_schema = ParkSchema()
parks_schema = ParkSchema(many=True)


class ParkResource(Resource):
    def __init__(self,  **kwargs):
        self.park_repo = kwargs['park_repo']

    def get(self, id: str):
        park = self.park_repo.get_by_id(id)
        return park_schema.dump(park).data, 200


class ParksResource(Resource):
    def __init__(self,  **kwargs):
        self.park_repo = kwargs['park_repo']
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('offset', type=int, required=True)
        self.reqparse.add_argument('limit', type=int, required=True)


    def get(self):
        args = self.reqparse.parse_args()
        offset = args['offset']
        limit = args['limit']

        parks = self.park_repo.get_batch(offset, limit)
        return {'parks': parks_schema.dump(parks).data}, 200

    def post(self):
        json_data = request.get_json()

        if not json_data:
            return {'message': 'No input data provided'}, 400
        park, errors = park_schema.load(json_data)
        if errors:
            return errors, 400

        try:
            park = self.park_repo.create(park)
            return park_schema.dump(park).data, 200
        except Exception:
            raise InternalServerError
