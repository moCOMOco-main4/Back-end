from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.http import Http404
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

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

# ===== 시그널: 자동 모집 마감/재오픈 =====

@receiver(post_save, sender=Application)
def auto_close_post_if_full(sender, instance, created, **kwargs):
    if not created:
        return

    post = instance.post
    role = instance.role

    max_count = post.roles.get(role, 0)
    current_count = Application.objects.filter(post=post, role=role).count()
    total_current = Application.objects.filter(post=post).count()
    total_max = sum(post.roles.values())

    if current_count >= max_count or total_current >= total_max:
        if not post.is_closed:
            post.is_closed = True
            post.save()


@receiver(post_delete, sender=Application)
def auto_reopen_post_if_not_full(sender, instance, **kwargs):
    post = instance.post
    total_current = Application.objects.filter(post=post).count()
    total_max = sum(post.roles.values())

    if total_current < total_max and post.is_closed:
        post.is_closed = False
        post.save()


# ===== 공통 Mixin =====

class PostAccessMixin:
    def get_post(self, post_id):
        try:
            return Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise Http404("모집글을 찾을 수 없습니다.")


# ===== 신청 관련 =====

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


class MyApplicationListView(generics.ListAPIView):
    serializer_class = MyApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user).select_related('post')


# ===== 좋아요 관련 =====

class PostLikeCreateView(PostAccessMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = self.get_post(post_id)
        user = request.user

        if PostLike.objects.filter(user=user, post=post).exists():
            raise ValidationError("이미 즐겨찾기한 모집글입니다.")

        PostLike.objects.create(user=user, post=post)
        return Response({"message": "즐겨찾기에 추가되었습니다."}, status=status.HTTP_201_CREATED)


class MyLikedPostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(liked_users__user=self.request.user)


# ===== 일정 관련 =====

class ScheduleCreateView(PostAccessMixin, generics.CreateAPIView):
    serializer_class = ScheduleCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post = self.get_post(self.kwargs['post_id'])
        if post.user != self.request.user:
            raise PermissionDenied("작성자만 일정을 등록할 수 있습니다.")
        serializer.save(post=post)


class ScheduleUpdateView(generics.UpdateAPIView):
    serializer_class = ScheduleUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Schedule.objects.all()

    def get_object(self):
        schedule = super().get_object()
        if schedule.post.user != self.request.user:
            raise PermissionDenied("작성자만 일정을 수정할 수 있습니다.")
        return schedule


class ScheduleDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Schedule.objects.all()

    def get_object(self):
        schedule = super().get_object()
        if schedule.post.user != self.request.user:
            raise PermissionDenied("작성자만 삭제할 수 있습니다.")
        return schedule


class ScheduleListView(generics.ListAPIView):
    serializer_class = ScheduleListSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Schedule.objects.filter(post_id=post_id).order_by('date')