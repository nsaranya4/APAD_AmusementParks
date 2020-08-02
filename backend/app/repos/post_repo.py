from models.post import Post


class PostRepo:

    def get_by_id(self, id: str):
        return Post.objects.get(id=id)

    def get_batch(self, offset: int, limit: int, filters: dict):
        post_list = Post.objects
        if filters.keys().__contains__('user_id'):
            post_list = post_list.filter(user=filters['user_id'])
        if filters.keys().__contains__('park_id'):
            post_list = post_list.filter(park=filters['park_id'])
        if filters.keys().__contains__('tag'):
            post_list = post_list.filter(tags=filters['tag'])
        return post_list.skip(offset).limit(limit)

    def create(self, post: Post):
        post = post.save()
        return post

    def delete(self, post: Post):
        post.delete()
