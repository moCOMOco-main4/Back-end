from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema
from apps.posts.utils.mixins import PostAccessMixin
from apps.posts.models.schedule import Schedule
from apps.posts.serializers.schedule_serializers import (
    ScheduleCreateSerializer,
    ScheduleUpdateSerializer,
    ScheduleListSerializer,
)
from apps.notifications.services import NotificationService
from drf_spectacular.utils import extend_schema, OpenApiParameter

# 일정 등록
@extend_schema(
    summary="일정 등록",
    request=ScheduleCreateSerializer,
    responses={201: None}
)
class ScheduleCreateView(PostAccessMixin, generics.CreateAPIView):
    serializer_class = ScheduleCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = self.get_post(post_id)

        if not Application.objects.filter(post=post, user=user).exists():
            raise PermissionDenied("참여한 모임에만 일정을 등록할 수 있습니다.")

        schedule = serializer.save(post=post)
        NotificationService.send_schedule_created(schedule)


# 일정 수정
@extend_schema(
    summary="일정 수정",
    request=ScheduleUpdateSerializer,
    responses={200: None}
)
class ScheduleUpdateView(generics.UpdateAPIView):
    serializer_class = ScheduleUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Schedule.objects.all()
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        schedule = super().get_object()
        if schedule.post.user != self.request.user:
            raise PermissionDenied("작성자만 일정을 수정할 수 있습니다.")
        return schedule


# 일정 삭제
@extend_schema(
    summary="일정 삭제",
    responses={204: None}
)
class ScheduleDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Schedule.objects.all()
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        schedule = super().get_object()
        if schedule.post.user != self.request.user:
            raise PermissionDenied("작성자만 삭제할 수 있습니다.")
        return schedule


# 일정 목록 조회
@extend_schema(
    summary="일정 목록 조회 (여러 post_id 가능)",
    responses=ScheduleListSerializer,
    parameters=[
        OpenApiParameter(
            name='post_id',
            type={'type': 'array', 'items': {'type': 'integer'}},
            location=OpenApiParameter.QUERY,
            required=True,
            explode=True,
            description='여러 모집글 ID (예: ?post_id=1&post_id=2&post_id=3)'
        )
    ]
)
class ScheduleListView(generics.ListAPIView):
    serializer_class = ScheduleListSerializer
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        post_ids = self.request.query_params.getlist('post_id')
        return Schedule.objects.filter(post_id__in=post_ids).order_by('date')