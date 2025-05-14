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

# 모집글 즐겨 찾기 추가
@extend_schema(
    methods=["POST"],
    responses={201: None},
    description="모집글을 즐겨찾기에 추가합니다. 중복 추가는 허용되지 않습니다."
)
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


# 내가 즐겨찾기한 모집글 목록 조회
@extend_schema(
    responses=PostListSerializer,
    description="내가 즐겨찾기한 모든 모집글을 목록으로 조회합니다."
)
class MyLikedPostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(liked_users__user=self.request.user)
