from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema
from django.db.models import Q

from apps.posts.models.post import Post
from apps.posts.serializers.post_serializers import (
    PostListSerializer,         # 상우님 기준 목록
    PostDetailSerializer,       # 상우님 기준 상세
    PostUpdateSerializer,       # 상우님 기준 수정
    PostCreateSerializer,        # 생성용
    PostSimpleDetailSerializer
)

# 목록 + 생성 (상우님 기준)
@extend_schema(
    request=PostCreateSerializer,
    responses={"GET": PostListSerializer, "POST": None},
)
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer
        return PostListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 내가 작성한 모집글
@extend_schema(
    responses=PostListSerializer,
    description="현재 로그인한 사용자가 작성한 모집글 목록"
)
class MyPostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).order_by('-created_at')


# 내가 참여한 모집글
@extend_schema(
    responses=PostListSerializer,
    description="내가 작성했거나 참여한 모집글 목록 (중복 제거)"
)
class ParticipatedPostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(
            Q(user=user) | Q(applications__user=user)
        ).distinct().order_by('-created_at')


# 단건 조회 + 수정 + 삭제 (상우님 기준)
@extend_schema(
    request=PostUpdateSerializer,
    responses={"GET": PostDetailSerializer, "PATCH": PostDetailSerializer, "DELETE": None}
)
class PostDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostDetailSerializer
        return PostUpdateSerializer

    def get_object(self):
        post = super().get_object()
        if self.request.method in ['PATCH', 'DELETE']:
            if post.user != self.request.user:
                raise PermissionDenied("작성자만 수정/삭제할 수 있습니다.")
            if post.is_closed and self.request.method == 'PATCH':
                raise PermissionDenied("마감된 모집글은 수정할 수 없습니다.")
        return post


# 비율형 상세 조회 (선형님 기준)
@extend_schema(
    responses=PostSimpleDetailSerializer,
    description="총인원 기준 비율로 현재 참여자 수를 보여줍니다. (예: 3/5)"
)
class PostDetailedRatioView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSimpleDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
