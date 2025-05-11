from django.urls import path
from apps.posts.views.application_views import (
    ApplicationCreateView,
    ApplicationDeleteView,
    MyApplicationListView,
    ApplicationListByPostView,
    ApplicationStatusUpdateView,
)

urlpatterns = [
    path('', ApplicationCreateView.as_view(), name='application-create'),  # 신청 생성
    path('me/', MyApplicationListView.as_view(), name='application-my-list'),  # 내가 신청한 목록
    path('post/<int:post_id>/', ApplicationListByPostView.as_view(), name='application-by-post'),  # 글 별 신청자 조회
    path('<int:pk>/', ApplicationDeleteView.as_view(), name='application-delete'),  # 신청 취소
    path('<int:pk>/status/', ApplicationStatusUpdateView.as_view(), name='application-status-update'),
]
