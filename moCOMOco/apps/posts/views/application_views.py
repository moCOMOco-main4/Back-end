from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

# 공통 믹스인
from apps.posts.utils.mixins import PostAccessMixin
from apps.posts.models.application import Application
from apps.posts.serializers.application_serializers import (
    ApplicationCreateSerializer,
    MyApplicationSerializer,
)
from apps.notifications.services import NotificationService



# 참여 신청
@extend_schema(
    request=ApplicationCreateSerializer,
    responses=None,
    examples=[
        {
            "name": "참여 신청 예시",
            "value": {
                "role": "backend"
            }
        }
    ]
)
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
            raise ValidationError(f"{role} 역할은 이 모임글이 존재하지 않습니다.")

        max_count = post.roles[role]
        current_count = Application.objects.filter(post=post, role=role).count()
        if current_count >= max_count:
            raise ValidationError(f"{role} 역할은 이미 마감되었습니다.")

        if Application.objects.filter(user=user, post=post).exists():
            raise ValidationError("이미 신청한 모글입니다.")

        application = serializer.save(user=user, post=post, role=role)
        NotificationService.send_apply_created(application)


# 모집글 참여 취소
class ApplicationCancelView(PostAccessMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses={204: None},
        description="참여했던 모집글에서 신청을 취소합니다."
    )
    def delete(self, request, post_id):
        post = self.get_post(post_id)
        application = Application.objects.filter(user=request.user, post=post).first()

        if not application:
            raise ValidationError("참여하지 않은 모임글입니다.")

        if post.user == request.user:
            raise PermissionDenied("작성자는 신청을 취소할 수 없습니다.")

        application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 내가 신청한 모집글 목록 조회
@extend_schema(
    responses=MyApplicationSerializer,
    description="내가 신청한 모집글 목록을 조회합니다."
)
class MyApplicationListView(generics.ListAPIView):
    serializer_class = MyApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user).select_related('post')
