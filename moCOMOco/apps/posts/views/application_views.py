from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema

from apps.posts.models.application import Application
from apps.posts.models.post import Post
from apps.posts.serializers.application_serializers import (
    ApplicationCreateSerializer,
    ApplicationSimpleSerializer,
    MyApplicationSerializer,
)
from apps.posts.utils.mixins import PostAccessMixin


# 모집글 신청
@extend_schema(request=ApplicationCreateSerializer, responses={201: ApplicationSimpleSerializer})
class ApplicationCreateView(PostAccessMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        user = request.user
        post = self.get_post(post_id)
        role = request.data.get("role")

        if post.is_closed:
            raise ValidationError("이미 마감된 모집글입니다.")

        if Application.objects.filter(user=user, post=post).exists():
            raise ValidationError("이미 신청한 모집글입니다.")

        max_count = post.roles.get(role)
        if max_count is None:
            raise ValidationError(f"{role}는 존재하지 않는 역할입니다.")

        current_count = Application.objects.filter(post=post, role=role).count()
        if current_count >= max_count:
            raise ValidationError(f"{role} 역할 인원이 이미 가득 찼습니다.")

        application = Application.objects.create(user=user, post=post, role=role)

        # 총 신청자 수 계산
        total_current = Application.objects.filter(post=post).count()
        if total_current >= post.max_people:
            post.is_closed = True
            post.save()

        return Response(ApplicationSimpleSerializer(application).data, status=status.HTTP_201_CREATED)


# 모집글 신청 취소
@extend_schema(request=None, responses={204: None})
class ApplicationCancelView(PostAccessMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, post_id):
        post = self.get_post(post_id)
        user = request.user

        try:
            application = Application.objects.get(user=user, post=post)
            application.delete()

            # 모집글 자동 오픈 조건 확인
            total_current = Application.objects.filter(post=post).count()
            if post.is_closed and total_current < post.max_people:
                post.is_closed = False
                post.save()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Application.DoesNotExist:
            return Response({"detail": "신청 기록이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)


# 내가 신청한 모집글 목록
@extend_schema(responses=MyApplicationSerializer)
class MyApplicationListView(generics.ListAPIView):
    serializer_class = MyApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user).select_related("post")
