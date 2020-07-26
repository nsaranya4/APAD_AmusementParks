from flask import request
from flask_restful import Resource, reqparse
from dal.models import Park
from dal.schemas import ParkSchema
from resources.errors import InternalServerError


class Park(Resource):
    def get(self, id):
        return {
            "name" : "Disney World",
            "image_id" : "image123",
            "description" : "Long text",
            "user_id" : "user@gmail.com",
            "location" : {
                "lat" : 23.0078201,
                "lng" : 88.5428696
            }
        }, 200


class Parks(Resource):
    def __init__(self):
        self.park_schema = ParkSchema()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('offset', type=int, required=True)
        self.reqparse.add_argument('limit', type=int, required=True)
        super(Parks, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        print(f"offset: {args['offset']}")
        print(f"limit: {args['limit']}")
        parks = Park.objects().to_json()
        return parks, 200

    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {'message': 'No input data provided'}, 400
        park, errors = self.park_schema.load(json_data)
        if errors:
            return errors, 400

        try:
            park.save()
        except Exception:
            raise InternalServerError
