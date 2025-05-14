from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema
# Mixin
from apps.posts.utils.mixins import PostAccessMixin

# models
from apps.posts.models.post import Post
from apps.posts.models.post_like import PostLike

# serializers
from apps.posts.serializers.post_serializers import PostListSerializer


# 즐겨찾기 추가
@extend_schema(
    request=None,
    responses={201: {"message": "즐겨찾기에 추가되었습니다."}},
    examples=[
        {
            "name": "즐겨찾기 추가 예시",
            "value": None
        }
    ]
)
class PostLikeCreateView(PostAccessMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = self.get_post(post_id)
        user = request.user

        if PostLike.objects.filter(user=user, post=post).exists():
            raise ValidationError("이미 즐겨찾기한 모집글입니다.")

        PostLike.objects.create(user=user, post=post)
        return Response({"message": "즐겨찾기에 추가되었습니다."}, status=status.HTTP_201_CREATED)


# 즐겨찾기 해제
@extend_schema(
    request=None,
    responses={
        204: {"message": "즐겨찾기에서 제거되었습니다."},
        400: {"detail": "즐겨찾기하지 않은 글입니다."}
    },
    examples=[
        {
            "name": "즐겨찾기 해제 예시",
            "value": None
        }
    ]
)
class PostLikeDeleteView(PostAccessMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, post_id):
        post = self.get_post(post_id)
        user = request.user

        try:
            like = PostLike.objects.get(user=user, post=post)
            like.delete()
            return Response({"message": "즐겨찾기에서 제거되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        except PostLike.DoesNotExist:
            return Response({"detail": "즐겨찾기하지 않은 글입니다."}, status=status.HTTP_400_BAD_REQUEST)


# 내가 즐겨찾기한 모집글 목록
@extend_schema(
    responses=PostListSerializer,
    description="현재 로그인한 사용자가 즐겨찾기한 모집글 목록을 반환합니다."
)
class MyLikedPostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(liked_users__user=self.request.user)
