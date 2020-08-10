from repos.post_repo import PostRepo
from repos.park_repo import ParkRepo
from repos.user_repo import UserRepo
from models.post import Post, Location
from representations.post import CreatePostRequest, PostSchema
from resources.errors import BadRequestError
import time


class PostService:
    def __init__(self, post_repo: PostRepo, park_repo: ParkRepo, user_repo: UserRepo):
        self.post_repo = post_repo
        self.park_repo = park_repo
        self.user_repo = user_repo
        self.post_schema = PostSchema()
        self.posts_schema = PostSchema(many=True)

    def create(self, create_post_request: CreatePostRequest):
        post = Post()

        park, error = self.park_repo.get_by_id(create_post_request.park_id) 
        if park is not None and error is None:
            post.park = park
        else: 
            return None, error

        user, error = self.user_repo.get_by_id(create_post_request.user_id)
        if user is not None and error is None:
            post.user = user
        else:
            return None, error

        location = Location()
        location.lat = create_post_request.location.lat
        location.lng = create_post_request.location.lng
        post.title = create_post_request.title
        post.description = create_post_request.description
        post.image_id = create_post_request.image_id
        post.tags = create_post_request.tags
        post.location = location
        post.created_at = time.time_ns()
        post, error = self.post_repo.create(post)
        if post is not None and error is None:
            return self.post_schema.dump(post).data, None
        else:
            return None, error

    def get_batch(self, offset, limit, filters):
        posts = self.post_repo.get_batch(offset, limit, filters)
        return self.posts_schema.dump(posts).data

    def get_by_id(self, id):
        post, error = self.post_repo.get_by_id(id)
        if post is not None and error is None:
            return self.post_schema.dump(post).data, None
        else:
            return None, error

    def delete_by_id(self, id):
        post, error = self.post_repo.get_by_id(id)
        if post is not None and error is None:
           return self.post_repo.delete(post), None
        elif post is None and error is not None:
            return None, BadRequestError
        else:
            return None, error
