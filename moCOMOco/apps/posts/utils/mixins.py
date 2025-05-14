from django.http import Http404
from apps.posts.models.post import Post


# post_id로 모집글(Post)을 가져오는 공통 Mixin
class PostAccessMixin:
    def get_post(self, post_id):
        try:
            return Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise Http404("모집글을 찾을 수 없습니다.")
