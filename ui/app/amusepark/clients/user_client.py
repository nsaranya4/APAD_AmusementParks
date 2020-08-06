import requests
from ..representations.user import CreateUserRequestSchema, UserSchema
from ..representations.subscription import CreateSubscriptionRequestSchema, SubscriptionSchema


class UserClient:
    def __init__(self, base_url):
        self.user_path = base_url + '/funtech/v1/users'
        self.subscription_path = base_url + '/funtech/v1/subscriptions'
        self.create_user_request_schema = CreateUserRequestSchema()
        self.user_schema = UserSchema()
        self.create_subscription_request_schema = CreateSubscriptionRequestSchema()
        self.subscription_schema = SubscriptionSchema()
        self.subscriptions_schema = SubscriptionSchema(many=True)
        self.headers = {"Content-Type": "application/json", "Accept": "*/*"}

    def create(self, create_user_request):
        payload = self.create_user_request_schema.dump(create_user_request).data
        response = requests.post(self.user_path, json=payload, headers=self.headers)
        # TODO:: handle error codes
        user = self.user_schema.load(response.json()).data
        return user

    def get_by_id(self, id):
        response = requests.get(self.user_path + "/" + id)
        # TODO:: handle error codes
        user = self.user_schema.load(response.json()).data
        return user

    def get_by_email_id(self, email_id):
        params = {'email': email_id}
        response = requests.get(self.user_path, params=params)
        if response.status_code == 404:
            return None
        else:
            user = self.user_schema.load(response.json()).data
            return user

    #TODO have a separate subscription client
    def create_subscription(self, create_subscription_request):
        payload = self.create_subscription_request_schema.dump(create_subscription_request).data
        response = requests.post(self.subscription_path, json=payload, headers=self.headers)
        # TODO:: handle error codes
        subscription = self.subscription_schema.load(response.json()).data
        return subscription

    # TODO have a separate subscription client
    def get_subscriptions(self, user_id):
        params = {'user_id': user_id}
        response = requests.get(self.subscription_path, params=params)
        #TODO:: handle error codes
        subscriptions = self.subscriptions_schema.load(response.json()).data
        return subscriptions

    # TODO have a separate subscription client
    def delete_subscription(self, subscription_id):
        response = requests.delete(self.subscription_path + "/" + subscription_id)
        if response.status_code == 204:
            return None
        else:
            return Exception
