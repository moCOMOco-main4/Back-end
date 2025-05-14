from django.urls import path

# views
from apps.posts.views.post_views import (
    PostListView, PostDetailView, MyPostListView,
    PostUpdateView, PostDeleteView, PostCreateView,
    ParticipatedPostListView, PostDetailedRatioView,
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
    # 모집글 목록, 생성
    path('', PostListView.as_view(), name='post-list'),  # GET /posts/
    path('create/', PostCreateView.as_view(), name='post-create'),  # POST /posts/create/

    # 단건 조회(GET), 수정(PATCH), 삭제(DELETE) - RESTful 방식으로 통일
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),  # GET /posts/{id}/
    path('<int:pk>/', PostUpdateView.as_view(), name='post-update'),  # PATCH /posts/{id}/
    path('<int:pk>/', PostDeleteView.as_view(), name='post-delete'),  # DELETE /posts/{id}/
    path('<int:pk>/detailed/', PostDetailedRatioView.as_view(), name='post-detailed-ratio'),  # GET 비율형 상세

    # 내가 작성한, 참여한 모집글 목록
    path('my/', MyPostListView.as_view(), name='my-posts'),
    path('joined/', ParticipatedPostListView.as_view(), name='joined-posts'),

    # 모집글 참여 신청/취소
    path('<int:post_id>/apply/', ApplicationCreateView.as_view(), name='post-apply'),
    path('<int:post_id>/cancel/', ApplicationCancelView.as_view(), name='post-cancel'),
    path('applied/', MyApplicationListView.as_view(), name='applied-posts'),

    # 즐겨찾기
    path('<int:pk>/like/', PostLikeCreateView.as_view(), name='post-like'),
    path('liked/', MyLikedPostListView.as_view(), name='liked-posts'),

    # 일정 (쿼리 파라미터 방식으로 정리)
    path('schedules/', ScheduleCreateView.as_view(), name='schedule-create'),
    path('schedules/<int:pk>/', ScheduleUpdateView.as_view(), name='schedule-update'),
    path('schedules/<int:pk>/', ScheduleDeleteView.as_view(), name='schedule-delete'),
    path('schedules/list/', ScheduleListView.as_view(), name='schedule-list'),
]

