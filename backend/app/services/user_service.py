from representations.user import UserSchema, CreateUserRequest
from repos.user_repo import UserRepo
from models.user import User


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
        user = self.user_repo.create(user)
        return self.user_schema.dump(user).data

    def get_by_email_id(self, email):
        user = self.user_repo.get_by_email_id(email)
        return self.user_schema.dump(user).data

    def get_by_id(self, id):
        user = self.user_repo.get_by_id(id)
        return self.user_schema.dump(user).data

    def delete_by_id(self, id):
        user = self.user_repo.delete(id)

