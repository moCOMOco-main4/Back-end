from rest_framework import generics, permissions, status
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import PermissionDenied

# mixin
from apps.posts.utils.mixins import PostAccessMixin

# models
from apps.posts.models.schedule import Schedule

# serializers
from apps.posts.serializers.schedule_serializers import (
    ScheduleCreateSerializer,
    ScheduleUpdateSerializer,
    ScheduleListSerializer,
)

# services
from apps.notifications.services import NotificationService


# 일정 등록
@extend_schema(
    request=ScheduleCreateSerializer,
    responses=None,
    examples=[
        {
            "name": "일정 등록 예시",
            "value": {
                "date": "2025-06-15T18:30:00Z",
                "memo": "첫 만남입니다. 모두 참여 부탁드립니다!"
            }
        }
    ]
)
class ScheduleCreateView(PostAccessMixin, generics.CreateAPIView):
    serializer_class = ScheduleCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post = self.get_post(self.kwargs['post_id'])
        if post.user != self.request.user:
            raise PermissionDenied("작성자만 일정을 등록할 수 있습니다.")
        schedule = serializer.save(post=post)
        NotificationService.send_schedule_created(schedule)


# 일정 수정
@extend_schema(
    request=ScheduleUpdateSerializer,
    responses=None,
    examples=[
        {
            "name": "일정 수정 예시",
            "value": {
                "date": "2025-06-20T20:00:00Z",
                "memo": "시간이 변경되었습니다."
            }
        }
    ]
)
class ScheduleUpdateView(generics.UpdateAPIView):
    serializer_class = ScheduleUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Schedule.objects.all()

    def get_object(self):
        schedule = super().get_object()
        if schedule.post.user != self.request.user:
            raise PermissionDenied("작성자만 일정을 수정할 수 있습니다.")
        return schedule


# 일정 삭제
@extend_schema(
    request=None,
    responses={204: None},
    description="일정을 삭제합니다. 작성자만 삭제할 수 있습니다.",
    examples=[
        {
            "name": "일정 삭제 예시",
            "value": None
        }
    ]
)
class ScheduleDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Schedule.objects.all()

    def get_object(self):
        schedule = super().get_object()
        if schedule.post.user != self.request.user:
            raise PermissionDenied("작성자만 삭제할 수 있습니다.")
        return schedule


# 모임글 일정 목록 조회
@extend_schema(
    responses=ScheduleListSerializer,
    description="해당 모임글의 전체 일정 목록을 반환합니다. 날짜 오름차순 정렬됩니다."
)
class ScheduleListView(generics.ListAPIView):
    serializer_class = ScheduleListSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Schedule.objects.filter(post_id=post_id).order_by('date')
