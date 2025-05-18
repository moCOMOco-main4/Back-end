# apps/app_users/views.py
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, parser_classes

from allauth.account.models import EmailAddress, EmailConfirmation
from allauth.socialaccount.models import SocialAccount, SocialToken
from rest_framework.authtoken.models import Token
from apps.chat.models import ChatRoomParticipant, ChatMessage
from apps.notifications.models import Notification
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

from .models import User
from .serializers import (
    UserDetailSerializer, UserUpdateSerializer,
    PositionSerializer, UserProfileSerializer
)
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from storages.backends.s3boto3 import S3Boto3Storage
from django.core.files.base import ContentFile

# S3 스토리지 인스턴스
s3_storage = S3Boto3Storage()

# Position 헬퍼
POSITION_NAMES = {1: "백엔드", 2: "프론트엔드", 3: "풀스택", 4: "디자이너"}

def _update_user_position(user, position):
    if position not in POSITION_NAMES:
        raise ValueError("유효하지 않은 포지션 값입니다.")
    user.position = position
    user.position_name = POSITION_NAMES[position]
    user.save()

def _prepare_position_response(user, position_value):
    _update_user_position(user, position_value)
    return {
        'user_id': user.id,
        'position_id': user.position,
        'position_name': user.position_name,
    }

class UserDetailView(APIView):
    """회원 정보 조회, 수정, 탈퇴(APIView)"""
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        # S3 이미지 업로드
        if 'profile_image_file' in request.FILES:
            uploaded_file = request.FILES['profile_image_file']
            file_name = f"profile_images/user_{request.user.id}_{uploaded_file.name}"
            s3_storage.save(file_name, ContentFile(uploaded_file.read()))
            request.data['profile_image'] = s3_storage.url(file_name)
        if serializer.is_valid():
            serializer.save()
            return Response(UserDetailSerializer(request.user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        회원 탈퇴 처리:
        1) SocialToken 및 SocialAccount 삭제
        2) EmailAddress 및 EmailConfirmation 삭제
        3) Chat/Notification 데이터 삭제
        4) Token(REST) 및 JWT Refresh 토큰 블랙리스트 처리
        5) 세션 로그아웃
        6) User 레코드 삭제
        """
        user = request.user
        # 1) 소셜 토큰/계정
        SocialToken.objects.filter(account__user=user).delete()
        SocialAccount.objects.filter(user=user).delete()
        # 2) 이메일 주소/인증
        EmailConfirmation.objects.filter(email_address__user=user).delete()
        EmailAddress.objects.filter(user=user).delete()
        # 3) 기타 연관 데이터
        ChatRoomParticipant.objects.filter(user=user).delete()
        ChatMessage.objects.filter(chat_user=user).delete()
        Notification.objects.filter(user=user).delete()
        # 3-1) Posts 관련 데이터
        from apps.posts.models import Post, Application, PostLike, Schedule
        # 사용자가 쓴 포스트, 지원, 좋아요, 스케줄 삭제
        Post.objects.filter(user=user).delete()
        Application.objects.filter(user=user).delete()
        PostLike.objects.filter(user=user).delete()
        Schedule.objects.filter(user=user).delete()
        # 4) REST Token, JWT Refresh, JWT Refresh
        Token.objects.filter(user=user).delete()
        for tk in OutstandingToken.objects.filter(user=user):
            BlacklistedToken.objects.get_or_create(token=tk)
        # 5) 세션 로그아웃
        logout(request)
        # 6) 사용자 삭제
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema(
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {'profile_image_file': {'type': 'string', 'format': 'binary'}}
        }
    },
    parameters=[
        OpenApiParameter(
            name='profile_image_file',
            description='업로드할 프로필 이미지',
            required=True,
            type=OpenApiTypes.BINARY,
            location='form'
        )
    ]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_profile_image(request):
    if 'profile_image_file' not in request.FILES:
        return Response({'error': '이미지 파일이 제공되지 않았습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    uploaded_file = request.FILES['profile_image_file']
    if not uploaded_file.content_type.startswith('image/'):
        return Response({'error': '유효한 이미지 파일이 아닙니다.'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        file_name = f"profile_images/user_{request.user.id}_{uploaded_file.name}"
        s3_storage.save(file_name, ContentFile(uploaded_file.read()))
        file_url = s3_storage.url(file_name)
        user = request.user
        user.profile_image = file_url
        user.save(update_fields=['profile_image'])
        return Response({
            'profile_image': file_url,
            'user': UserDetailSerializer(user).data,
            'message': '프로필 이미지 업로드 성공'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': f'업로드 중 오류: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PositionView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = PositionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            return Response(_prepare_position_response(request.user, serializer.validated_data['position']), status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request):
        serializer = PositionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            return Response(_prepare_position_response(request.user, serializer.validated_data['position']), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        return Response(UserProfileSerializer(user).data)