from rest_framework import generics, permissions, filters
from rest_framework.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.posts.models.post import Post
from apps.posts.serializers.post_serializers import (
    PostListSerializer,
    PostDetailSerializer,
    PostUpdateSerializer,
    PostCreateSerializer,
    PostSimpleDetailSerializer
)


# 모집글 목록 조회 + 모집글 생성 (상우님 기준)
@extend_schema(
    request=PostCreateSerializer,
    responses={"GET": PostListSerializer, "POST": None},
)
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    # 검색(제목, 내용), 카테고리 필터 적용
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'content']
    filterset_fields = ['category']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer
        return PostListSerializer

    def perform_create(self, serializer):
        backend = serializer.validated_data.pop("backend", 0)
        frontend = serializer.validated_data.pop("frontend", 0)
        designer = serializer.validated_data.pop("designer", 0)
        fullstack = serializer.validated_data.pop("fullstack", 0)

        # Post 인스턴스 생성
        post = Post.objects.create(
            **serializer.validated_data,
            roles={
                'backend': backend,
                'frontend': frontend,
                'designer': designer,
                'fullstack': fullstack,
            },
            user=self.request.user,
        )

        # 현재 참여 인원이 max_people 도달 시 자동 마감
        if post.participants.count() >= post.max_people:
            post.is_closed = True
            post.save()

        return post


# 내가 작성한 모집글만 조회
@extend_schema(
    responses=PostListSerializer,
    description="현재 로그인한 사용자가 작성한 모집글 목록"
)
class MyPostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).order_by('-created_at')


# 내가 작성했거나 참여한 모집글 조회
@extend_schema(
    responses=PostListSerializer,
    description="내가 작성했거나 참여한 모집글 목록 (중복 제거)"
)
class ParticipatedPostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(
            Q(user=user) | Q(applications__user=user)
        ).distinct().order_by('-created_at')


# 모집글 단건 조회 + 수정 + 삭제
@extend_schema(
    request=PostUpdateSerializer,
    responses={"GET": PostDetailSerializer, "PATCH": PostDetailSerializer, "DELETE": None}
)
class PostDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostDetailSerializer
        return PostUpdateSerializer

    def get_object(self):
        post = super().get_object()

        # PATCH, DELETE는 작성자만 가능
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
    authentication_classes = [JWTAuthentication]