import requests
from ..representations.post import CreatePostRequest, CreatePostRequest, Post, PostSchema


class PostClient:
    def __init__(self, base_url):
        self.post_path = base_url + '/posts'
        self.create_post_request_schema = CreatePostRequest()
        self.post_schema = PostSchema()

    def create(self, create_post_request):
        data = self.create_post_request_schema.dump(create_post_request).data
        response = requests.post(self.post_path, data=data)
        post = self.post_schema.load(response.json())
        return post

