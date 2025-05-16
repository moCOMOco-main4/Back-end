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
from rest_framework_simplejwt.authentication import JWTAuthentication

# 모집글 신청
@extend_schema(request=ApplicationCreateSerializer, responses={201: ApplicationSimpleSerializer})
class ApplicationCreateView(PostAccessMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, post_id):
        user = request.user
        post = self.get_post(post_id)

        # serializer 사용 + context로 post 전달
        serializer = ApplicationCreateSerializer(
            data=request.data,
            context={'request': request, 'post': post}
        )
        serializer.is_valid(raise_exception=True)

        # save() 시 post, user 주입
        application = serializer.save(user=user, post=post)

        return Response(ApplicationSimpleSerializer(application).data, status=status.HTTP_201_CREATED)


# 모집글 신청 취소
@extend_schema(request=None, responses={204: None})
class ApplicationCancelView(PostAccessMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

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
    authentication_classes = [JWTAuthentication]
    
    def get_queryset(self):
        return Application.objects.filter(user=self.request.user).select_related("post")
