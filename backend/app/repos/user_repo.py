from models.user import User


class UserRepo:

     def create(self, user: User):
        user.save()
        return user

     def get_by_id(self, id: str):
         return User.objects.get(id=id)
