from repos.subscription_repo import SubscriptionRepo
from repos.park_repo import ParkRepo
from repos.user_repo import UserRepo
from models.subscription import Subscription
from representations.subscription import CreateSubscriptionRequest, SubscriptionSchema


class SubscriptionService:
    def __init__(self, subscription_repo: SubscriptionRepo, park_repo: ParkRepo, user_repo: UserRepo):
        self.subscription_repo = subscription_repo
        self.park_repo = park_repo
        self.user_repo = user_repo
        self.subscription_schema = SubscriptionSchema()
        self.subscriptions_schema = SubscriptionSchema(many=True)

    def create(self, create_subscription_request: CreateSubscriptionRequest):
        park = self.park_repo.get_by_id(create_subscription_request.park_id)
        user = self.user_repo.get_by_id(create_subscription_request.user_id)
        subscription = Subscription(park=park, user=user)
        subscription = self.subscription_repo.create(subscription)
        return self.subscription_schema.dump(subscription).data

    def get_batch(self, filters):
        subscriptions = self.subscription_repo.get_batch(filters)
        return self.subscriptions_schema.dump(subscriptions).data

    def delete_by_id(self, id: str):
        subscription = self.subscription_repo.get_by_id(id)
        self.subscription_repo.delete(subscription)
