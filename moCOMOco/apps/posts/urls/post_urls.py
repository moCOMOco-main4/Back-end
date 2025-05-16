from django.urls import path

from apps.posts.views.application_views import (
    ApplicationCreateView, ApplicationCancelView, MyApplicationListView,
)
from apps.posts.views.like_views import (
    PostLikeCreateView, MyLikedPostListView, PostLikeDeleteView,
)
from apps.posts.views.schedule_views import (
    ScheduleCreateView, ScheduleUpdateView,
    ScheduleDeleteView, ScheduleListView,
)
from apps.posts.views.post_views import (
    PostListCreateView,
    MyPostListView,
    ParticipatedPostListView,
    PostDetailUpdateDeleteView,
    PostDetailedRatioView,
)

urlpatterns = [
    # 모집글 목록 + 생성
    path('', PostListCreateView.as_view(), name='post-list-create'),  # GET/POST /posts/

    # 단건 조회(GET) + 수정(PATCH/PUT) + 삭제(DELETE)
    path('<int:pk>/', PostDetailUpdateDeleteView.as_view(), name='post-detail-update-delete'),

    # 비율형 role_status 조회 (선형님용)
    path('<int:pk>/detailed/', PostDetailedRatioView.as_view(), name='post-detailed-ratio'),

    # 내가 작성한, 참여한 모집글 목록
    path('my/', MyPostListView.as_view(), name='my-posts'),
    path('joined/', ParticipatedPostListView.as_view(), name='joined-posts'),

    # 모집글 참여 신청/취소
    path('<int:post_id>/apply/', ApplicationCreateView.as_view(), name='post-apply'),
    path('<int:post_id>/cancel/', ApplicationCancelView.as_view(), name='post-cancel'),
    path('applied/', MyApplicationListView.as_view(), name='applied-posts'),

    # 즐겨찾기
    path('<int:post_id>/like/', PostLikeCreateView.as_view(), name='post-like'),
    path('<int:post_id>/unlike/', PostLikeDeleteView.as_view(), name='post-unlike'),
    path('liked/', MyLikedPostListView.as_view(), name='liked-posts'),

    # 일정
    path('<int:post_id>/schedules/', ScheduleCreateView.as_view(), name='schedule-create'),
    path('schedules/<int:pk>/update/', ScheduleUpdateView.as_view(), name='schedule-update'),
    path('schedules/<int:pk>/delete/', ScheduleDeleteView.as_view(), name='schedule-delete'),
    path('schedules/list/', ScheduleListView.as_view(), name='schedule-list'),
]
