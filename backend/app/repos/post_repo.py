from models.post import Post


class PostRepo():

    def get_by_id(self, id: str):
        return Post.objects.get_or_404(id=id)

    def get_batch(self, offset: int, limit: int):
        # TODO figure out how to use pagination while querying mongodb
        post_list = Post.objects()
        return post_list

    def create(self, post: Post):
        post.save()
        return post