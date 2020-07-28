from models.user import User


class UserRepo():

     def create(self, user: User):
        user.save()
        return user
