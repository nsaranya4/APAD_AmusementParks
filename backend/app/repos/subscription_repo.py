from models.subscription import Subscription


class SubscriptionRepo:

    def get_batch(self, filters: dict):
        subscription_list = Subscription.objects
        if filters.keys().__contains__('user_id'):
            subscription_list = subscription_list.filter(user=filters['user_id'])
        return subscription_list

    def create(self, subscription: Subscription):
        subscription = subscription.save()
        return subscription
