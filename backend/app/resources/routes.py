from .park_resources import ParkResource, ParksResource
from .post_resources import PostResource, PostsResource
from .user_resources import UserResource
from repos.post_repo import PostRepo
from repos.park_repo import ParkRepo
from repos.user_repo import UserRepo
from .post_resources import PostResource, PostsResource


def initialize_routes(api):
    park_repo = ParkRepo()
    post_repo = PostRepo()
    user_repo = UserRepo()
    api.add_resource(ParkResource, '/funtech/v1/parks/<string:id>', resource_class_kwargs={'park_repo': park_repo})
    api.add_resource(ParksResource, '/funtech/v1/parks', resource_class_kwargs={'park_repo': park_repo})
    api.add_resource(PostResource, '/funtech/v1/posts/<string:id>', resource_class_kwargs={'post_repo': post_repo})
    api.add_resource(PostsResource, '/funtech/v1/posts', resource_class_kwargs={'post_repo': post_repo})
    api.add_resource(UserResource, '/funtech/v1/users', resource_class_kwargs={'user_repo': user_repo})
