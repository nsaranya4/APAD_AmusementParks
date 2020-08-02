from repos.post_repo import PostRepo
from repos.park_repo import ParkRepo
from repos.user_repo import UserRepo
from models.post import Post, Location
from representations.post import CreatePostRequest, PostSchema


class PostService:
    def __init__(self, post_repo: PostRepo, park_repo: ParkRepo, user_repo: UserRepo):
        self.post_repo = post_repo
        self.park_repo = park_repo
        self.user_repo = user_repo
        self.post_schema = PostSchema()
        self.posts_schema = PostSchema(many=True)

    def create(self, create_post_request: CreatePostRequest):
        park = self.park_repo.get_by_id(create_post_request.park_id)
        user = self.user_repo.get_by_id(create_post_request.user_id)
        post = Post()
        location = Location()
        location.lat = create_post_request.location.lat
        location.lng = create_post_request.location.lng
        post.title = create_post_request.title
        post.description = create_post_request.description
        post.image_id = create_post_request.image_id
        post.tags = create_post_request.tags
        post.location = location
        post.park = park
        post.user = user
        post = self.post_repo.create(post)
        return self.post_schema.dump(post).data

    def get_batch(self, offset, limit, filters):
        posts = self.post_repo.get_batch(offset, limit, filters)
        return self.posts_schema.dump(posts).data

    def get_by_id(self, id):
        post = self.post_repo.get_by_id(id)
        return self.post_schema.dump(post).data

    def delete_by_id(self, id):
        post = self.post_repo.get_by_id(id)
        self.post_repo.delete(post)
