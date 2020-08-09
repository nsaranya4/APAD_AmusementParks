from representations.user import UserSchema, CreateUserRequest
from repos.user_repo import UserRepo
from models.user import User
from resources.errors import BadRequestError


class UserService:
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo
        self.user_schema = UserSchema()

    def create(self, create_user_request: CreateUserRequest):
        user = User()
        user.name = create_user_request.name
        user.email = create_user_request.email
        user.image_id = create_user_request.image_id
        user.role = create_user_request.role
        user, error = self.user_repo.create(user)
        if user is not None and error is None:
            return self.user_schema.dump(user).data, None
        else:
            return None, error

    def get_by_email_id(self, email):
        user, error = self.user_repo.get_by_email_id(email)
        if user is not None:
            return self.user_schema.dump(user).data, None
        else:
            return None, error

    def get_by_id(self, id):
        user, error = self.user_repo.get_by_id(id)
        if user is not None:
            return self.user_schema.dump(user).data, None
        else:
            return None, error

    def delete_by_id(self, id):
        user, error = self.user_repo.get_by_id(id)
        if user is not None and error is None:
            return self.user_repo.delete(user), None
        elif user is None and error is not None:
            return None, BadRequestError
        else:
            return None, error

