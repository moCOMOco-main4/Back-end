from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema
from django.db.models import Q

# models
from apps.posts.models.post import Post

# serializers
from apps.posts.serializers.post_serializers import (
    PostListSerializer,
    PostDetailSerializer,
    PostSimpleDetailSerializer,
    PostUpdateSerializer,
    PostCreateSerializer,
)


# 모집글 생성
@extend_schema(responses=None)
class PostCreateView(generics.CreateAPIView):
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 모집글 전체 목록 조회 (상우님)
@extend_schema(responses=PostListSerializer)
class PostListView(generics.ListAPIView):
    serializer_class = PostListSerializer

    def get_queryset(self):
        qs = Post.objects.all()
        category = self.request.query_params.get('category')
        is_closed = self.request.query_params.get('is_closed')

        if category:
            qs = qs.filter(category=category)
        if is_closed is not None:
            qs = qs.filter(is_closed=(is_closed.lower() == 'true'))

        return qs


# 내가 쓴 모집글 목록 조회
@extend_schema(responses=PostListSerializer)
class MyPostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).order_by('-created_at')


# 내가 작성하거나 신청한 모집글 목록 조회 (joined)
@extend_schema(responses=PostListSerializer)
class ParticipatedPostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(
            Q(user=user) | Q(applications__user=user)
        ).distinct().order_by('-created_at')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


# 모집글 상세 조회 (상우님: 숫자형 role_status)
@extend_schema(responses=PostDetailSerializer)
class PostDetailView(generics.RetrieveAPIView):
    serializer_class = PostDetailSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


# 모집글 상세 조회 (선형님: 비율형 role_status)
@extend_schema(responses=PostSimpleDetailSerializer)
class PostDetailedRatioView(generics.RetrieveAPIView):
    serializer_class = PostSimpleDetailSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


# 모집글 수정
@extend_schema(responses=PostDetailSerializer)
class PostUpdateView(generics.UpdateAPIView):
    serializer_class = PostUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()

    def get_object(self):
        post = super().get_object()
        if post.user != self.request.user:
            raise PermissionDenied("수정 권한이 없습니다.")
        if post.is_closed:
            raise PermissionDenied("마감된 모집글은 수정할 수 없습니다.")
        return post


# 모집글 삭제
@extend_schema(responses=None)
class PostDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()

    def get_object(self):
        post = super().get_object()
        if post.user != self.request.user:
            raise PermissionDenied("삭제 권한이 없습니다.")
        return post
