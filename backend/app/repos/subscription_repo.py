from models.subscription import Subscription


class SubscriptionRepo:

    def get_by_id(self, id: str):
        try:
            subscription = Subscription.objects.get(id=id)
            return subscription, None
        except Subscription.DoesNotExist:
            return None, None
        except Exception as e:
            return None, e

    def get_batch(self, filters: dict):
        subscription_list = Subscription.objects
        if filters.keys().__contains__('user_id'):
            subscription_list = subscription_list.filter(user=filters['user_id']).order_by('-created_at')
        return subscription_list

    def create(self, subscription: Subscription):
        try:
            subscription = subscription.save()
            return subscription, None
        except Exception as e:
            return None, e

    def delete(self, subscription: Subscription):
        subscription.delete()
