from django.urls import path
from apps import (
    PostListView, PostDetailView, MyPostListView,
    PostUpdateView, PostDeleteView, PostCreateView,
)
from apps import (
    ApplicationCreateView, ApplicationCancelView, MyApplicationListView,
)
from apps import (
    PostLikeCreateView, MyLikedPostListView,
)
from apps import (
    ScheduleCreateView, ScheduleUpdateView,
    ScheduleDeleteView, ScheduleListView,
)

urlpatterns = [
    # 모집글 생성
    path('create/', PostCreateView.as_view(), name='post-create'),
    # 모집글 전체 목록 조회
    path('', PostListView.as_view(), name='post-list'),
    # 모집글 상세 조회
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    # 모집글 참여 신청
    path('<int:post_id>/apply/', ApplicationCreateView.as_view(), name='post-apply'),
    # 모집글 참여 취소
    path('<int:post_id>/cancel/', ApplicationCancelView.as_view(), name='post-cancel'),
    # 내가 쓴 모집글 조회
    path('my/', MyPostListView.as_view(), name='my-posts'),
    # 내가 신청한 모집글 조회
    path('applied/', MyApplicationListView.as_view(), name='applied-posts'),
    # 모집글 수정
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post-edit'),
    # 모집글 삭제
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    # 즐겨찾기 등록
    path('<int:post_id>/like/', PostLikeCreateView.as_view(), name='post-like'),
    # 즐겨찾기한 모집글 목록
    path('liked/', MyLikedPostListView.as_view(), name='liked-posts'),
    # 일정 등록
    path('<int:post_id>/schedule/', ScheduleCreateView.as_view(), name='schedule-create'),
    # 일정 수정
    path('<int:post_id>/schedule/<int:pk>/', ScheduleUpdateView.as_view(), name='schedule-update'),
    # 일정 삭제
    path('<int:post_id>/schedule/<int:pk>/delete/', ScheduleDeleteView.as_view(), name='schedule-delete'),
    # 모집글 일정 목록 조회
    path('<int:post_id>/schedule/list/', ScheduleListView.as_view(), name='schedule-list'),
]
