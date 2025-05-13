from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

# Mixin
from apps.posts.utils.mixins import PostAccessMixin

# models
from apps.posts.models.post import Post
from apps.posts.models.post_like import PostLike

# serializers
from apps.posts.serializers.post_serializers import PostListSerializer


# 즐겨찾기 추가
class PostLikeCreateView(PostAccessMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = self.get_post(post_id)
        user = request.user

        if PostLike.objects.filter(user=user, post=post).exists():
            raise ValidationError("이미 즐겨찾기한 모집글입니다.")

        PostLike.objects.create(user=user, post=post)
        return Response({"message": "즐겨찾기에 추가되었습니다."}, status=status.HTTP_201_CREATED)


# 내가 즐겨찾기한 모집글 목록
class MyLikedPostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(liked_users__user=self.request.user)
