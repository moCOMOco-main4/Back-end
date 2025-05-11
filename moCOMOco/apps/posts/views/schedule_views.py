from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from apps.posts.models import Post, Application, Schedule
from apps.posts.serializers.schedule_serializers import ScheduleCreateSerializer, ScheduleListSerializer

# 일정 생성
class ScheduleCreateView(generics.CreateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post = serializer.validated_data['post']
        if post.user != self.request.user:
            raise PermissionDenied('작성자만 일정을 등록할 수 있습니다.')
        serializer.save()

# 모임 전체 일정 조회
class MyScheduleListView(generics.ListAPIView):
    serializer_class = ScheduleListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # 작성자 or 수락된 유저만
        accepted_post_ids = Application.objects.filter(user=user, status='accepted').values_list('post_id', flat=True)
        return Schedule.objects.filter(post__in=list(accepted_post_ids) + list(Post.objects.filter(user=user).values_list('id', flat=True)))

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context