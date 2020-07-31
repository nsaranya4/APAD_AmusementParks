import requests
from ..representations.user import CreateUserRequestSchema, UserSchema


class UserClient:
    def __init__(self, base_url):
        self.user_path = base_url + '/funtech/v1/users'
        self.create_user_request_schema = CreateUserRequestSchema()
        self.user_schema = UserSchema()

    def create(self, create_user_request):
        data = self.create_user_request_schema.dump(create_user_request).data
        response = requests.post(self.user_path, data=data)
        # TODO:: handle error codes
        user = self.user_schema.load(response.json()).data
        return user

    def get_by_id(self, id):
        response = requests.get(self.user_path + "/" + id)
        # TODO:: handle error codes
        user = self.user_schema.load(response.json()).data
        return user

    def get_by_email_id(self, email_id):
        params = {'email_id': email_id}
        response = requests.get(self.user_path, params=params)
        #TODO:: handle error codes
        user = self.user_schema.load(response.json()).data
        return user
