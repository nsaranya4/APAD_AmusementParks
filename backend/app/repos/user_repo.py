from models.user import User


class UserRepo:

      def create(self, user: User):
          try:
              user = user.save()
              return user, None
          except Exception as e:
             return None, e

      def get_by_id(self, id: str):
          try:
              user = User.objects.get(id=id)
              return user, None
          except User.DoesNotExist:
              return None, None
          except Exception as e:
              return None, e

      def get_by_email_id(self, email: str):
          try:
              user = User.objects.get(email=email)
              return user, None
          except User.DoesNotExist:
              return None, None
          except Exception as e:
              return None, e


      def delete(self, user: User):
          user.delete()
