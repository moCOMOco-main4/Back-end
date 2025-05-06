from django.conf import settings
from rest_framework.permissions import AllowAny
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.naver.views import NaverOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework import serializers

from .serializers import UserDetailSerializer

# 프론트엔드 URL 가져오기
FRONTEND_URL = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')

# 커스텀 시리얼라이저 추가
class SocialLoginSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    provider = serializers.CharField(required=False)  # provider 필드를 필수가 아닌 것으로 설정


class KakaoLoginView(SocialLoginView):
    """
    카카오 소셜 로그인 뷰
    - 프론트엔드에서 받은 인증 코드로 사용자 인증 처리
    - JWT 토큰 발급
    """
    adapter_class = KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = settings.KAKAO_REDIRECT_URI
    permission_classes = [AllowAny]

    def get_response(self):
        """응답 데이터에 사용자 정보 추가"""
        response = super().get_response()

        # 사용자 정보 추가
        user = self.user
        response.data['user'] = UserDetailSerializer(user).data
        response.data['isNewUser'] = getattr(user, '_is_new_user', False)

        return response


class NaverLoginView(SocialLoginView):
    """
    네이버 소셜 로그인 뷰
    - 프론트엔드에서 받은 인증 코드로 사용자 인증 처리
    - JWT 토큰 발급
    """
    adapter_class = NaverOAuth2Adapter
    client_class = OAuth2Client
    callback_url = settings.NAVER_REDIRECT_URI
    permission_classes = [AllowAny]

    def get_response(self):
        """응답 데이터에 사용자 정보 추가"""
        response = super().get_response()

        # 사용자 정보 추가
        user = self.user
        response.data['user'] = UserDetailSerializer(user).data
        response.data['isNewUser'] = getattr(user, '_is_new_user', False)

        return response


class GithubLoginView(SocialLoginView):
    """
    GitHub 소셜 로그인 뷰
    - 프론트엔드에서 받은 인증 코드로 사용자 인증 처리
    - JWT 토큰 발급
    """
    adapter_class = GitHubOAuth2Adapter
    client_class = OAuth2Client
    callback_url = settings.GITHUB_REDIRECT_URI
    permission_classes = [AllowAny]

    def get_response(self):
        """응답 데이터에 사용자 정보 추가"""
        response = super().get_response()

        # 사용자 정보 추가
        user = self.user
        response.data['user'] = UserDetailSerializer(user).data
        response.data['isNewUser'] = getattr(user, '_is_new_user', False)

        return response