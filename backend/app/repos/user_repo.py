from models.user import User


class UserRepo:

      def create(self, user: User):
        user.save()
        return user

      def get_by_id(self, id: str):
         return User.objects.get(id=id)

      def get_by_email_id(self, email: str):
         return User.objects.get(email=email)

      def delete(self, id: str):
        user = User.objects(id=id)
        user.delete()
