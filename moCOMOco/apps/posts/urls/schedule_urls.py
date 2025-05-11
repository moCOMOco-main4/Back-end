from django.urls import path
from apps.posts.views.schedule_views import ScheduleCreateView, MyScheduleListView

urlpatterns = [
    path('', ScheduleCreateView.as_view(), name='schedule-create'),
    path('me/', MyScheduleListView.as_view(), name='schedule-my-list'),
]
