from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.views import APIView
from django.http import Http404

from apps.posts.models import Post, Application
from apps.posts.serializers.application_serializers import (
    ApplicationCreateSerializer,
    MyApplicationSerializer,
)

# 모집글 조회 헬퍼
class PostAccessMixin:
    def get_post(self):
        try:
            return Post.objects.get(id=self.kwargs['post_id'])
        except Post.DoesNotExist:
            raise Http404("모집글을 찾을 수 없습니다.")


# 참여 신청
class ApplicationCreateView(PostAccessMixin, generics.CreateAPIView):
    serializer_class = ApplicationCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['post'] = self.get_post()
        return context

    def perform_create(self, serializer):
        user = self.request.user
        post = self.get_post()
        role = self.request.data.get('role')

        # 모집 마감 여부
        if post.is_closed:
            raise ValidationError("모집이 마감된 글입니다.")

        # 역할 유효성 확인
        if role not in post.roles:
            raise ValidationError(f"{role} 역할은 이 모집글에 존재하지 않습니다.")

        # 역할별 정원 초과 확인
        max_count = post.roles[role]
        current_count = Application.objects.filter(post=post, role=role).count()
        if current_count >= max_count:
            raise ValidationError(f"{role} 역할은 이미 마감되었습니다.")

        # 중복 신청 확인
        if Application.objects.filter(user=user, post=post).exists():
            raise ValidationError("이미 신청한 모집글입니다.")

        serializer.save(user=user, post=post, role=role)


# 참여 취소
class ApplicationCancelView(PostAccessMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, post_id):
        post = self.get_post()
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