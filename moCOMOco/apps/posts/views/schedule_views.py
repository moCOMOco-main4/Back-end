from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.http import Http404

from apps.posts.models import Post, Application, Schedule, PostLike
from apps.posts.serializers.application_serializers import (
    ApplicationCreateSerializer,
    MyApplicationSerializer,
)
from apps.posts.serializers.post_serializers import PostListSerializer
from apps.posts.serializers.schedule_serializers import (
    ScheduleCreateSerializer,
    ScheduleUpdateSerializer,
    ScheduleListSerializer,
)
from apps.notifications.services import NotificationService

# 모집글 조회 헬퍼
class PostAccessMixin:
    def get_post(self, post_id):
        try:
            return Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise Http404("모집글을 찾을 수 없습니다.")


# ===== 신청 관련 =====

# 참여 신청
class ApplicationCreateView(PostAccessMixin, generics.CreateAPIView):
    serializer_class = ApplicationCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['post'] = self.get_post(self.kwargs['post_id'])
        return context

    def perform_create(self, serializer):
        user = self.request.user
        post = self.get_post(self.kwargs['post_id'])
        role = self.request.data.get('role')

        if post.is_closed:
            raise ValidationError("모집이 마감된 글입니다.")
        if role not in post.roles:
            raise ValidationError(f"{role} 역할은 이 모집글에 존재하지 않습니다.")

        max_count = post.roles[role]
        current_count = Application.objects.filter(post=post, role=role).count()
        if current_count >= max_count:
            raise ValidationError(f"{role} 역할은 이미 마감되었습니다.")

        if Application.objects.filter(user=user, post=post).exists():
            raise ValidationError("이미 신청한 모집글입니다.")

        serializer.save(user=user, post=post, role=role)


# 참여 취소
class ApplicationCancelView(PostAccessMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, post_id):
        post = self.get_post(post_id)
        application = Application.objects.filter(user=request.user, post=post).first()

        if not application:
            raise ValidationError("참여하지 않은 모집글입니다.")

        if post.user == request.user:
            raise PermissionDenied("작성자는 신청을 취소할 수 없습니다.")

        application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 내가 신청한 모집글 목록 조회
class MyApplicationListView(generics.ListAPIView):
    serializer_class = MyApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user).select_related('post')


# ===== 좋아요 관련 =====

# 즐겨찾기 추가
class PostLikeCreateView(PostAccessMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = self.get_post(post_id)
        user = request.user

        if PostLike.objects.filter(user=user, post=post).exists():
            raise ValidationError("이미 즐겨찾기한 모집글입니다.")

        PostLike.objects.create(user=user, post=post)
        return Response({"message": "즐겨찾기에 추가되었습니다."}, status=status.HTTP_201_CREATED)


# 내가 즐겨찾기한 모집글 목록
class MyLikedPostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(liked_users__user=self.request.user)


# ===== 일정 관련 =====

# 일정 등록
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
class ScheduleDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Schedule.objects.all()

    def get_object(self):
        schedule = super().get_object()
        if schedule.post.user != self.request.user:
            raise PermissionDenied("작성자만 삭제할 수 있습니다.")
        return schedule


# 모집글 일정 목록 조회
class ScheduleListView(generics.ListAPIView):
    serializer_class = ScheduleListSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Schedule.objects.filter(post_id=post_id).order_by('date')