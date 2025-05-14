from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
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


# 목록 + 생성 (List + Create API 통합)
@extend_schema(
    request=PostCreateSerializer,
    responses={
        "GET": PostListSerializer,
        "POST": None
    },
    examples=[
        {
            "name": "모집글 생성 예시",
            "value": {
                "title": "강남 백엔드 구합니다",
                "content": "같이 열심히 공부하실 분!",
                "category": "project",
                "place_name": "강남역",
                "address": "서울시 강남구",
                "latitude": 37.4979,
                "longitude": 127.0276,
                "image": None,
                "date": "2025-06-01T10:00:00Z",
                "max_people": 5,
                "is_closed": False,
                "backend": 2,
                "frontend": 1,
                "designer": 0
            }
        }
    ]
)
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer
        return PostListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 내가 쓴 모집글 목록 조회
@extend_schema(
    responses=PostListSerializer,
    description="현재 로그인한 사용자가 작성한 모임글 목록을 반환합니다."
)
class MyPostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).order_by('-created_at')


# 참여한 모집글 목록 조회
@extend_schema(
    responses=PostListSerializer,
    description="현재 로그인한 사용자가 작성하거나 신청한 모임글 목록을 반환합니다. 중복 없이 정렬됩니다."
)
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


# 상세 조회 + 수정 + 삭제 통합 (상우님 기준)
@extend_schema(
    request=PostUpdateSerializer,
    responses={
        "GET": PostDetailSerializer,
        "PATCH": PostDetailSerializer,
        "DELETE": None
    },
    examples=[
        {
            "name": "모집글 수정 예시",
            "value": {
                "title": "프론트엔드도 같이 구해요",
                "content": "화/목 저녁 8시에 진행 예정입니다.",
                "category": "project",
                "place_name": "신촌역",
                "address": "서울시 마포구",
                "latitude": 37.5598,
                "longitude": 126.9423,
                "image": None,
                "date": "2025-06-10T20:00:00Z",
                "max_people": 6,
                "is_closed": False,
                "backend": 1,
                "frontend": 2,
                "designer": 1
            }
        }
    ]
)
class PostDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostDetailSerializer
        return PostUpdateSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_object(self):
        post = super().get_object()
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            if post.user != self.request.user:
                raise PermissionDenied("작성자만 수정/삭제할 수 있습니다.")
            if post.is_closed and self.request.method in ['PUT', 'PATCH']:
                raise PermissionDenied("마감된 모집글은 수정할 수 없습니다.")
        return post


# 비율형 role_status 상세 조회 (선형님 전용)
@extend_schema(responses=PostSimpleDetailSerializer)
class PostDetailedRatioView(generics.RetrieveAPIView):
    serializer_class = PostSimpleDetailSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

