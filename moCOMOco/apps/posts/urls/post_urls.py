from django.urls import path
from apps.posts.views.post_views import (
    PostCreateView,
    PostListView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView,
    MyPostListView,
    PostLocationListView,
)

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),  # 전체 글 목록
    path('create/', PostCreateView.as_view(), name='post-create'),  # 모집글 작성
    path('me/', MyPostListView.as_view(), name='post-my-list'),  # 내가 쓴 글 목록
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),  # 상세 조회
    path('<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),  # 수정
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),  # 삭제
    path('locations/', PostLocationListView.as_view(), name='post-location-list'),  # 위치 목록
]
