from flask import request
from flask_restful import Resource, reqparse
from representations.subscription import SubscriptionSchema, CreateSubscriptionRequestSchema
from resources.errors import InternalServerError, BadRequestError


class SubscriptionResource(Resource):
    def __init__(self,  **kwargs):
        self.subscription_service = kwargs['subscription_service']

    def delete(self, id: str):
        subscription, error = self.subscription_service.delete_by_id(id)
        if error is not None and error == BadRequestError:
            return None, 400
        elif error is not None:
            return None, 500
        else:
            return None, 204


class SubscriptionsResource(Resource):
    def __init__(self,  **kwargs):
        self.subscription_service = kwargs['subscription_service']
        self.create_subscription_request_schema = CreateSubscriptionRequestSchema()
        self.subscription_schema = SubscriptionSchema()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('user_id', type=str)

    def get(self):
        args = self.reqparse.parse_args()
        filters = {}
        if args['user_id'] is not None:
            filters['user_id'] = args['user_id']
        subscriptions = self.subscription_service.get_batch(filters)
        return subscriptions, 200

    def post(self):
        json_data = request.get_json()

        if not json_data:
            return {'message': 'No input data provided'}, 400
        create_subscription_request, errors = self.create_subscription_request_schema.load(json_data)
        if errors:
            return errors, 400

        try:
            subscription, error = self.subscription_service.create(create_subscription_request)
            if error is not None:
                return None, 500
            else:
                return subscription, 200
        except Exception:
            raise InternalServerError
