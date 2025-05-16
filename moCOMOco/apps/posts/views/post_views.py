from rest_framework import generics, permissions, filters, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.posts.models.post import Post
from apps.posts.serializers.post_serializers import (
    PostDetailSerializer,
    PostUpdateSerializer,
    PostCreateListSerializer,
    PostSimpleDetailSerializer, PostListSerializer
)


# 모집글 목록 조회 + 모집글 생성 (상우님 기준)
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'content']
    filterset_fields = ['category', 'max_people']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateListSerializer
        return PostListSerializer

    def get_serializer_context(self):
        return {'request': self.request, 'user': self.request.user}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# 내가 작성한 모집글만 조회
@extend_schema(
    responses=PostCreateListSerializer,
    description="현재 로그인한 사용자가 작성한 모집글 목록"
)
class MyPostListView(generics.ListAPIView):
    serializer_class = PostCreateListSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).order_by('-created_at')


# 내가 참여한 모집글 조회
@extend_schema(
    responses=PostCreateListSerializer,
    description="내가 참여한 모집글 목록"
)
class ParticipatedPostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(applications__user=user).distinct().order_by('-created_at')

    def get_serializer_context(self):
        return {'request': self.request}

# 모집글 단건 조회 + 수정 + 삭제
@extend_schema_view(
    get=extend_schema(
        summary="모집글 상세 조회",
        responses=PostDetailSerializer
    ),
    patch=extend_schema(
        summary="모집글 수정",
        request=PostUpdateSerializer,
        responses=PostDetailSerializer
    ),
    delete=extend_schema(
        summary="모집글 삭제",
        responses=None
    ),
)
class PostDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostDetailSerializer
        return PostUpdateSerializer

    def get_serializer_context(self):
        return {'request': self.request}

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