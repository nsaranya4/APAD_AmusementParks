import requests
from ..representations.post import CreatePostRequestSchema, PostSchema


class PostClient:
    def __init__(self, base_url):
        self.post_path = base_url + '/funtech/v1/posts'
        self.create_post_request_schema = CreatePostRequestSchema()
        self.post_schema = PostSchema()
        self.posts_schema = PostSchema(many=True)

    def create(self, create_post_request):
        data = self.create_post_request_schema.dump(create_post_request).data
        response = requests.post(self.post_path, data=data)
        post = self.post_schema.load(response.json())
        return post

    def get_by_user_id(self, user_id, offset, limit):
        params = {'user_id': user_id, offset: offset, limit: limit}
        response = requests.get(self.post_path, params=params)
        posts = self.posts_schema.load(response.json())
        return posts

    def get_by_id(self, id):
        response = requests.get(self.post_path + "/" + id)
        post = self.post_schema.load(response.json()).data
        return post
