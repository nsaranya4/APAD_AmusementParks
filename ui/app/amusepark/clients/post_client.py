import requests
from ..representations.post import CreatePostRequestSchema, PostSchema


class PostClient:
    def __init__(self, base_url):
        self.post_path = base_url + '/funtech/v1/posts'
        self.create_post_request_schema = CreatePostRequestSchema()
        self.post_schema = PostSchema()
        self.posts_schema = PostSchema(many=True)
        self.headers = {"Content-Type": "application/json", "Accept": "*/*"}

    def create(self, create_post_request):
        data = self.create_post_request_schema.dump(create_post_request).data
        response = requests.post(self.post_path, json=data, headers=self.headers)
        # TODO:: handle error codes
        post = self.post_schema.load(response.json()).data
        return post

    def get_by_id(self, id):
        response = requests.get(self.post_path + "/" + id)
        # TODO:: handle error codes
        post = self.post_schema.load(response.json()).data
        return post

    def get_batch(self, filters, offset, limit):
        pagination = {'offset': offset, 'limit': limit}
        params = {**filters, **pagination}
        response = requests.get(self.post_path, params=params)
        #TODO:: handle error codes
        posts = self.posts_schema.load(response.json()).data
        return posts
