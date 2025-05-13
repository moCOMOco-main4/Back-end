from django.urls import path

# views
from apps.posts.views.post_views import (
    PostListView, PostDetailView, MyPostListView,
    PostUpdateView, PostDeleteView, PostCreateView,
)
from apps.posts.views.application_views import (
    ApplicationCreateView, ApplicationCancelView, MyApplicationListView,
)
from apps.posts.views.like_views import (
    PostLikeCreateView, MyLikedPostListView,
)
from apps.posts.views.schedule_views import (
    ScheduleCreateView, ScheduleUpdateView,
    ScheduleDeleteView, ScheduleListView,
)

urlpatterns = [
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('', PostListView.as_view(), name='post-list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),

    # 참여 신청 및 취소
    path('<int:post_id>/apply/', ApplicationCreateView.as_view(), name='post-apply'),
    path('<int:post_id>/cancel/', ApplicationCancelView.as_view(), name='post-cancel'),
    path('applied/', MyApplicationListView.as_view(), name='applied-posts'),

    # 내가 쓴 모집글
    path('my/', MyPostListView.as_view(), name='my-posts'),

    # 수정/삭제
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post-edit'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    # 즐겨찾기
    path('<int:post_id>/like/', PostLikeCreateView.as_view(), name='post-like'),
    path('liked/', MyLikedPostListView.as_view(), name='liked-posts'),

    # 일정
    path('<int:post_id>/schedule/', ScheduleCreateView.as_view(), name='schedule-create'),
    path('<int:post_id>/schedule/<int:pk>/', ScheduleUpdateView.as_view(), name='schedule-update'),
    path('<int:post_id>/schedule/<int:pk>/delete/', ScheduleDeleteView.as_view(), name='schedule-delete'),
    path('<int:post_id>/schedule/list/', ScheduleListView.as_view(), name='schedule-list'),
]
