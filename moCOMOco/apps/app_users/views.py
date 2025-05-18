from django.core.files.base import ContentFile
from storages.backends.s3boto3 import S3Boto3Storage
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, parser_classes

from .models import User
from .serializers import (
    UserDetailSerializer, UserUpdateSerializer, PositionSerializer,
)
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django.shortcuts import get_object_or_404
from .serializers import UserProfileSerializer
from apps.chat.models import ChatRoomParticipant, ChatMessage
from apps.notifications.models import Notification
from django.db import transaction
from apps.posts.models import PostLike, Application, Schedule, Post
from allauth.socialaccount.models import SocialAccount


# Position 매핑
POSITION_NAMES = {
    1: "백엔드",
    2: "프론트엔드",
    3: "풀스택",
    4: "디자이너"
}

# s3 스토리지 인스턴스 생성
s3_storage = S3Boto3Storage()

def _update_user_position(user, position):
    """사용자 포지션 업데이트 헬퍼 함수"""
    if position not in POSITION_NAMES:
        raise ValueError("유효하지 않은 포지션 값입니다.")
    user.position = position
    user.position_name = POSITION_NAMES[position]
    user.save()

def _prepare_position_response(user, position_value):
    """포지션 응답 데이터 준비 헬퍼 함수 (중복 코드 제거)"""
    _update_user_position(user, position_value)
    return {
        'user_id': user.id,
        'position_id': user.position,
        'position_name': user.position_name,
    }

class UserDetailView(APIView):
    """현재 사용자 정보 조회 API 뷰"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # self를 사용하므로 static 메서드로 변환하지 않음
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        # 이피지 파일 처리 기능 수정(S3Boto3 사용)
        if 'profile_image_file' in request.FILES:
            uploaded_file =  request.FILES['profile_image_file']
            # 이미지 저장 경로 변경(S3Boto3 변경)
            file_name = f"profile_images/user_{request.user.id}_{uploaded_file.name}"
            s3_storage.save(file_name, ContentFile(uploaded_file.read()))
            # S3 URL 생성
            file_url = s3_storage.url(file_name)
            request.data['profile_image'] = file_url

        if serializer.is_valid():
            serializer.save()
            return Response(UserDetailSerializer(request.user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def delete(self, request):
    user = request.user

    # 트랜잭션 처리로 모든 삭제가 성공하거나 모두 실패하도록 보장
    with transaction.atomic():
        try:
            # 알림 삭제
            Notification.objects.filter(user=user).delete()

            # 게시물 관련 데이터 삭제
            PostLike.objects.filter(user=user).delete()
            Application.objects.filter(user=user).delete()

            # 사용자가 작성한 게시물 관련 삭제
            user_posts = Post.objects.filter(user=user)
            Schedule.objects.filter(post__in=user_posts).delete()
            user_posts.delete()

            # 채팅 관련 삭제
            ChatMessage.objects.filter(chat_user=user).delete()
            ChatRoomParticipant.objects.filter(user=user).delete()

            # 소셜 계정 삭제
            SocialAccount.objects.filter(user=user).delete()

            # 마지막으로 사용자 삭제
            user.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            # 로깅 추가 (실제 환경에서는 logger 사용 권장)
            print(f"사용자 삭제 중 오류 발생: {str(e)}")
            return Response({"error": "회원 탈퇴 중 오류가 발생했습니다."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'profile_image_file': {
                    'type': 'string',
                    'format': 'binary'
                }
            }
        }
    },
    parameters=[
        OpenApiParameter(
            name='profile_image_file',
            description='업로드할 프로필 이미지',
            required=True,
            type=OpenApiTypes.BINARY,
            location= "form"
        )
    ]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])  # 명시적으로 파서 클래스 지정
def upload_profile_image(request):
    """프로필 이미지 업로드 전용 엔드포인트"""
    if 'profile_image_file' not in request.FILES:
        return Response({
            'error': '이미지 파일이 제공되지 않았습니다.'
        }, status=status.HTTP_400_BAD_REQUEST)

    uploaded_file = request.FILES['profile_image_file']

    # 이미지 파일 타입 검증 (선택사항)
    if not uploaded_file.content_type.startswith('image/'):
        return Response({
            'error': '유효한 이미지 파일이 아닙니다.'
        }, status=status.HTTP_400_BAD_REQUEST)

    # S3Boto#Storage를 사용하여 S3에 파일 업로드
    try:
        file_name = f"profile_images/user_{request.user.id}_{uploaded_file.name}"
        s3_storage.save(file_name, ContentFile(uploaded_file.read()))
        file_url = s3_storage.url(file_name)   # S3 URL 생성

        #사용자 프로필 업데이트
        user = request.user
        user.profile_image = file_url
        user.save(update_fields=['profile_image'])

        return Response({
            'profile_image': file_url,
            'user': UserDetailSerializer(user).data,
            'message': '프로필 이미지가 성공적으로 S3에 업로드되었습니다.'

        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'error': f'이미지 업로드 중 오류가 발생했습니다: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PositionView(APIView):
    """사용자 포지션 관리 API 뷰"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # self를 사용하므로 static 메서드로 변환하지 않음
        serializer = PositionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            response_data = _prepare_position_response(
                request.user,
                serializer.validated_data['position']
            )
            return Response(response_data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        serializer = PositionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            response_data = _prepare_position_response(
                request.user,
                serializer.validated_data['position']
            )
            return Response(response_data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """다른 사용자의 프로필 정보를 조회하는 API View"""
    permission_classes = [IsAuthenticated] # 로그인한 사용자만 접근 가능

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
