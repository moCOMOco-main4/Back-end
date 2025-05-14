from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema

from apps.posts.utils.mixins import PostAccessMixin
from apps.posts.models.post import Post
from apps.posts.models.post_like import PostLike
from apps.posts.serializers.post_serializers import PostListSerializer
from apps.posts.serializers.empty_serializers import EmptySerializer


# 즐겨찾기 추가
@extend_schema(request=None, responses={201: EmptySerializer})
class PostLikeCreateView(PostAccessMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EmptySerializer

    def post(self, request, post_id):
        post = self.get_post(post_id)
        user = request.user

        if PostLike.objects.filter(user=user, post=post).exists():
            raise ValidationError("이미 즐겨찾기한 모집글입니다.")

        PostLike.objects.create(user=user, post=post)
        return Response({"message": "즐겨찾기에 추가되었습니다."}, status=status.HTTP_201_CREATED)


# 즐겨찾기 해제
@extend_schema(request=None, responses={204: None})
class PostLikeDeleteView(PostAccessMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, post_id):
        post = self.get_post(post_id)
        user = request.user

        try:
            like = PostLike.objects.get(user=user, post=post)
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PostLike.DoesNotExist:
            return Response({"detail": "즐겨찾기하지 않은 글입니다."}, status=status.HTTP_400_BAD_REQUEST)


# 내가 즐겨찾기한 모집글 목록 조회
@extend_schema(responses=PostListSerializer)
class MyLikedPostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(liked_users__user=self.request.user)
