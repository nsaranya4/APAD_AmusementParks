from models.user import User


class UserRepo:

      def create(self, user: User):
        user.save()
        return user

      def get_by_id(self, id: str):
         return User.objects.get(id=id)

      def get_by_email_id(self, email: str):
          try:
              user = User.objects.get(email=email)
              return user, None
          #TODO:: fix this
          except Exception as e:
              return None, None


      def delete(self, user: User):
        user.delete()
