from flask import request
from flask_restful import Resource, reqparse
from dal.models import Park as ParkModel
from dal.schemas import ParkSchema
from resources.errors import InternalServerError

park_schema = ParkSchema()
parks_schema = ParkSchema(many=True)


class Park(Resource):

    def get(self, id):
        park = ParkModel.objects.get_or_404(id=id)
        return park_schema.dump(park).data, 200


class Parks(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('offset', type=int, required=True)
        self.reqparse.add_argument('limit', type=int, required=True)
        super(Parks, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        offset = args['offset']
        limit = args['limit']
        # TODO figure out how to use pagination while querying mongodb
        parks = ParkModel.objects()
        parklist = parks_schema.dump(parks).data
        return {'parks': parklist}, 200

    def post(self):
        json_data = request.get_json()

        if not json_data:
            return {'message': 'No input data provided'}, 400
        park, errors = park_schema.load(json_data)
        if errors:
            return errors, 400

        try:
            park.save()
            return park_schema.dump(park).data, 200
        except Exception:
            raise InternalServerError
