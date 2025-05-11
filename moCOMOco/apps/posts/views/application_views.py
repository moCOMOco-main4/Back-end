from rest_framework import permissions, generics, status
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from apps.posts.models import Application, Post
from apps.posts.serializers.application_serializers import (
    ApplicationCreateSerializer,
    ApplicationSimpleSerializer,
    MyApplicationSerializer,
    ApplicationStatusUpdateSerializer,
)
from apps.posts.services.post_service import check_post_closed


# 모집글 신청
class ApplicationCreateView(generics.CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        post_id = self.request.data.get('post')
        role = self.request.data.get('role')

        post = get_object_or_404(Post, id=post_id)

        if post.is_closed:
            raise ValidationError('이미 마감된 모집글입니다.')

        if Application.objects.filter(user=user, post=post).exists():
            raise ValidationError('이미 신청하셨습니다.')

        max_count = post.roles.get(role)
        if max_count is None:
            raise ValidationError(f"'{role}' 역할은 모집 대상이 아닙니다.")

        current_count = Application.objects.filter(post=post, role=role).count()
        if current_count >= max_count:
            raise ValidationError(f"'{role}' 역할은 이미 마감되었습니다.")

        # 신청 저장
        serializer.save(user=user, post=post, role=role)

        # 자동 마감 체크
        check_post_closed(post)


# 모집글 신청 취소
# 신청 취소 (탈퇴 사유 포함)
class ApplicationDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            application = Application.objects.get(pk=pk)
        except Application.DoesNotExist:
            return Response({"detail": "신청 정보가 없습니다"}, status=404)

        if application.user != request.user:
            raise PermissionDenied("본인만 탈퇴할 수 있습니다")

        leave_reason = request.data.get("leave_reason", "")
        application.leave_reason = leave_reason
        application.save()
        application.delete()

        return Response({"detail": "탈퇴 처리 완료"}, status=status.HTTP_204_NO_CONTENT)



# 내가 신청한 목록 조회
class MyApplicationListView(generics.ListAPIView):
    serializer_class = MyApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user).order_by('-created_at')


# 특정 모집글에 대한 신청자 목록 조회 (작성자 전용)
class ApplicationListByPostView(generics.ListAPIView):
    serializer_class = ApplicationSimpleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)

        if post.user != self.request.user:
            raise PermissionDenied('작성자만 신청자 목록을 조회할 수 있습니다.')

        return Application.objects.filter(post=post).order_by('-created_at')

# 신청 상태 수락 거절 처리
class ApplicationStatusUpdateView(generics.UpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        application = super().get_object()

        if application.post.user != self.request.user:
            raise PermissionDenied('작성자만 신청 상태를 변경 가능')
        return application