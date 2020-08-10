from repos.subscription_repo import SubscriptionRepo
from repos.park_repo import ParkRepo
from repos.user_repo import UserRepo
from models.subscription import Subscription
from representations.subscription import CreateSubscriptionRequest, SubscriptionSchema
from resources.errors import BadRequestError
import time


class SubscriptionService:
    def __init__(self, subscription_repo: SubscriptionRepo, park_repo: ParkRepo, user_repo: UserRepo):
        self.subscription_repo = subscription_repo
        self.park_repo = park_repo
        self.user_repo = user_repo
        self.subscription_schema = SubscriptionSchema()
        self.subscriptions_schema = SubscriptionSchema(many=True)

    def create(self, create_subscription_request: CreateSubscriptionRequest):
        subscription = Subscription()
        park, error = self.park_repo.get_by_id(create_subscription_request.park_id)
        if park is not None and error is None:
            subscription.park = park
        else: 
            return None, error
        
        user, error = self.user_repo.get_by_id(create_subscription_request.user_id)
        if user is not None and error is None:
            subscription.user = user
        else:
            return None, error
        
        subscription = Subscription(created_at=time.time_ns(), park=park, user=user)
        subscription, error = self.subscription_repo.create(subscription)
        if subscription is not None and error is None:
            return self.subscription_schema.dump(subscription).data, None
        else: 
            return None, error

    def get_batch(self, filters):
        subscriptions = self.subscription_repo.get_batch(filters)
        return self.subscriptions_schema.dump(subscriptions).data

    def delete_by_id(self, id: str):
        subscription, error = self.subscription_repo.get_by_id(id)
        if subscription is not None and error is None:
            return self.subscription_repo.delete(subscription), None
        elif subscription is None and error is not None:
            return None, BadRequestError
        else:
            return None, error
