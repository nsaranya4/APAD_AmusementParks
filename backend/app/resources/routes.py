from .park import Park, Parks
from .post import Post, Posts


def initialize_routes(api):
    api.add_resource(Park, '/funtech/v1/parks/<string:id>')
    api.add_resource(Parks, '/funtech/v1/parks')
    api.add_resource(Post, '/funtech/v1/posts/<string:id>')
    api.add_resource(Posts, '/funtech/v1/posts')
