from models.post import Post


class PostRepo:

    def get_by_id(self, id: str):
        try:
            post = Post.objects.get(id=id)
            return post, None
        except Post.DoesNotExist:
            return None, None
        except Exception as e:
            return None, e
            

    def get_batch(self, offset: int, limit: int, filters: dict):
        post_list = Post.objects
        if filters.keys().__contains__('user_id'):
            post_list = post_list.filter(user=filters['user_id'])
        if filters.keys().__contains__('park_id'):
            post_list = post_list.filter(park=filters['park_id'])
        if filters.keys().__contains__('tag'):
            post_list = post_list.filter(tags=filters['tag'])
        return post_list.order_by('-created_at').skip(offset).limit(limit)

    def create(self, post: Post):
        try:
            post = post.save()
            return post, None
        except Exception as e:
            return None, e

    def delete(self, post: Post):
        post.delete()
