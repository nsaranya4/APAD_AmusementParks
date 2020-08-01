from models.subscription import Subscription


class SubscriptionRepo:

    def get_by_id(self, id: str):
        return Subscription.objects.get(id=id)

    def get_batch(self,filters: dict):
        subscription_list = Subscription.objects
        if filters.keys().__contains__('user_id'):
            subscription_list = subscription_list.filter(user=filters['user_id'])
    
        #if filters.keys().__contains__('park_id'):
            #subscription_list = subscription_list.filter(park=filters['park_id'])
        return subscription_list

    def create(self, post: Post):
        Subscription.save()
        return Subscription