from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema

from apps.posts.utils.mixins import PostAccessMixin
from apps.posts.models.schedule import Schedule
from apps.posts.serializers.schedule_serializers import (
    ScheduleCreateSerializer,
    ScheduleUpdateSerializer,
    ScheduleListSerializer,
)
from apps.notifications.services import NotificationService


# 일정 등록
@extend_schema(
    request=ScheduleCreateSerializer,
    responses=ScheduleListSerializer,
    description="모집글에 일정 정보를 등록합니다. 작성자만 등록할 수 있습니다."
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
    methods=['PATCH'],
    request=ScheduleUpdateSerializer,
    responses=ScheduleListSerializer,
    description="기존 등록된 일정을 수정합니다. 작성자만 수정 가능합니다."
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
    methods=['DELETE'],
    responses={204: None},
    description="등록된 일정을 삭제합니다. 작성자만 삭제 가능합니다."
)
class ScheduleDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Schedule.objects.all()

    def get_object(self):
        schedule = super().get_object()
        if schedule.post.user != self.request.user:
            raise PermissionDenied("작성자만 삭제할 수 있습니다.")
        return schedule


# 일정 목록 조회
@extend_schema(
    responses=ScheduleListSerializer,
    description="특정 모집글에 등록된 전체 일정 목록을 조회합니다. (post_id를 쿼리 파라미터로 전달)"
)
class ScheduleListView(generics.ListAPIView):
    serializer_class = ScheduleListSerializer

    def get_queryset(self):
        post_id = self.request.query_params.get('post_id')
        return Schedule.objects.filter(post_id=post_id).order_by('date')
