from django.conf import settings
from rest_framework.permissions import AllowAny
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.naver.views import NaverOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken  # 추가된 부분
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
        response = super().get_response()
        user = self.user

        # 사용자 정보 확인 및 업데이트 (필요시)
        if not user.provider or user.provider != 'kakao':
            user.provider = 'kakao'
            user .save(update_fields=['provider'])
            print(f"[DEBUG] Updated Kakao user provider: {user.provider}")

        # 사용자 정보 확인을 위해 다시 DB에서 조회
        user = user.__class__.objects.get(pk=user.pk)

        #JWT 토큰 생성
        refresh = RefreshToken.for_user(user)
        response.data['access'] =str(refresh.access_token)
        response.data['refresh'] = str(refresh)

        #사용자 정보 포함
        user_data = UserDetailSerializer(user).data
        response.data['user'] = user_data
        response.data['isNewUser'] = getattr(user, '_is_new_user', False)

        # 디버깅 정보 출력
        print(f"[DEBUG] Kakao login response user data: {user_data}")

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
        response = super().get_response()
        user = self.user

        # 사용자 정보 확인 밒 업데이트 (필요시)
        if not user.provider or user.provider != 'naver':
            user.provider = 'naver'
            user.save(update_fields=['provider'])
            print(f"[DEBUG] Updated Naver user provider: {user.provider}")

        # 사용자 정보 확인을 위해 다시 DB에서 조회
        user = user.__class__.objects.get(pk=user.pk)

        #JWT 토큰 생성
        refresh = RefreshToken.for_user(user)
        response.data['access'] =str(refresh.access_token)
        response.data['refresh'] = str(refresh)

        #사용자 정보 포함
        user_data = UserDetailSerializer(user).data
        response.data['user'] = user_data
        response.data['isNewUser'] = getattr(user, '_is_new_user', False)

        # 디버깅 정보 출력
        print(f"[DEBUG] Naver login response user data: {user_data}")

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
        response = super().get_response()
        user = self.user

        # GitHub 사용자 정보 확인 및 업데이트 (필요시)
        if not user.provider or user.provider != 'github':
            user.provider = 'github'
            user.save(update_fields=['provider'])

        # 사용자 정보 확인을 위해 다시 DB에서 조회
        user = user.__class__.objects.get(pk=user.pk)

        # JWT 토큰 생성
        refresh = RefreshToken.for_user(user)
        response.data['access'] = str(refresh.access_token)
        response.data['refresh'] = str(refresh)

        # 사용자 정보 포함
        user_data = UserDetailSerializer(user).data
        response.data['user'] = user_data
        response.data['isNewUser'] = getattr(user, '_is_new_user', False)

        return response
