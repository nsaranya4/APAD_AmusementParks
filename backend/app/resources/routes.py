from .park_resources import ParkResource, ParksResource
from .post_resources import PostResource, PostsResource
from .user_resources import UsersResource
from repos.post_repo import PostRepo
from repos.park_repo import ParkRepo
from repos.user_repo import UserRepo
from services.post_service import PostService
from services.park_service import ParkService
from services.user_service import UserService


def initialize_routes(api):
    park_repo = ParkRepo()
    post_repo = PostRepo()
    user_repo = UserRepo()
    post_service = PostService(post_repo, park_repo, user_repo)
    park_service = ParkService(park_repo, user_repo)
    user_service = UserService(user_repo)
    api.add_resource(ParkResource, '/funtech/v1/parks/<string:id>', resource_class_kwargs={'park_service': park_service})
    api.add_resource(ParksResource, '/funtech/v1/parks', resource_class_kwargs={'park_service': park_service})
    api.add_resource(PostResource, '/funtech/v1/posts/<string:id>', resource_class_kwargs={'post_service': post_service})
    api.add_resource(PostsResource, '/funtech/v1/posts', resource_class_kwargs={'post_service': post_service})
    api.add_resource(UsersResource, '/funtech/v1/users', resource_class_kwargs={'user_service': user_service})
