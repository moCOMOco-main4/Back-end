from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.posts.models import Post
from apps.posts.serializers.post_serializers import (
    PostCreateSerializer,
    PostListSerializer,
    PostDetailSerializer,
    PostUpdateSerializer,
    PostLocationSerializer,
)
from apps.posts.services.post_service import check_post_closed


# 모집글 작성
class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 모집글 전체 목록 조회
class PostListView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostListSerializer
    permission_classes = [permissions.AllowAny]


# 모집글 상세 조회
class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        post = super().get_object()
        check_post_closed(post)
        return post


# 모집글 수정
class PostUpdateView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        post = self.get_object()
        if post.user != self.request.user:
            raise PermissionDenied('작성자만 수정할 수 있습니다.')
        serializer.save()


# 모집글 삭제
class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied('작성자만 삭제할 수 있습니다.')
        instance.delete()


# 내가 작성한 모집글 목록
class MyPostListView(generics.ListAPIView):
    queryset = Post.objects.none()  # 기본값 설정
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).order_by('-created_at')


# 모집글 위치 리스트 (지도용)
class PostLocationListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostLocationSerializer
    permission_classes = [permissions.AllowAny]
