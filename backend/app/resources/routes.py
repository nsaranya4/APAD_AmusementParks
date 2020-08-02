from .park_resources import ParkResource, ParksResource
from .post_resources import PostResource, PostsResource
from .user_resources import UsersResource, UserResource
from .subscription_resource import SubscriptionsResource, SubscriptionResource
from repos.post_repo import PostRepo
from repos.park_repo import ParkRepo
from repos.user_repo import UserRepo
from repos.subscription_repo import SubscriptionRepo
from services.post_service import PostService
from services.park_service import ParkService
from services.user_service import UserService
from services.subscription_service import SubscriptionService


def initialize_routes(api):
    park_repo = ParkRepo()
    post_repo = PostRepo()
    user_repo = UserRepo()
    subscription_repo = SubscriptionRepo()
    post_service = PostService(post_repo, park_repo, user_repo)
    park_service = ParkService(park_repo, user_repo)
    user_service = UserService(user_repo)
    subscription_service = SubscriptionService(subscription_repo, park_repo, user_repo)
    api.add_resource(ParkResource, '/funtech/v1/parks/<string:id>', resource_class_kwargs={'park_service': park_service})
    api.add_resource(ParksResource, '/funtech/v1/parks', resource_class_kwargs={'park_service': park_service})
    api.add_resource(PostResource, '/funtech/v1/posts/<string:id>', resource_class_kwargs={'post_service': post_service})
    api.add_resource(PostsResource, '/funtech/v1/posts', resource_class_kwargs={'post_service': post_service})
    api.add_resource(UsersResource, '/funtech/v1/users', resource_class_kwargs={'user_service': user_service})
    api.add_resource(UserResource, '/funtech/v1/users/<string:id>', resource_class_kwargs={'user_service': user_service})
    api.add_resource(SubscriptionsResource, '/funtech/v1/subscriptions', resource_class_kwargs={'subscription_service': subscription_service})
    api.add_resource(SubscriptionResource, '/funtech/v1/subscriptions/<string:id>', resource_class_kwargs={'subscription_service': subscription_service})
