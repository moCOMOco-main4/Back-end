from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import User


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    일반 계정용 커스텀 어댑터
    - 회원가입, 로그인 등 프로세스 커스터마이징
    """

    def get_login_redirect_url(self, request):
        """로그인 성공 후 리다이렉션 URL"""
        return settings.LOGIN_REDIRECT_URL

    def get_logout_redirect_url(self, request):
        """로그아웃 후 리다이렉션 URL"""
        return settings.LOGOUT_REDIRECT_URL


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):

    def save_user(self, request, sociallogin, form=None):
        """
        소셜 계정으로 사용자 저장 시 추가 정보 설정
        - 프로필 정보 동기화
        - 기본 포지션 설정
        - 신규 사용자 플래그 설정
        """
        # 신규 사용자인지 확인 (나중에 응답에서 사용)
        email = sociallogin.account.extra_data.get('email') or sociallogin.user.email
        is_new_user = not User.objects.filter(email=email).exists()

        # 기본 사용자 저장 로직 실행
        user = super().save_user(request, sociallogin, form)

        # 소셜 계정 정보 처리
        social_data = sociallogin.account.extra_data
        provider = sociallogin.account.provider

        # 제공자 정보 저장
        user.provider = provider

        # 제공자별 데이터 처리
        if provider == 'kakao':
            kakao_account = social_data.get('kakao_account', {})
            profile = kakao_account.get('profile', {})

            user.nickname = profile.get('nickname', user.nickname or f'Kakao_{user.id}')
            user.profile_image = profile.get('profile_image_url', user.profile_image)
            user.name = profile.get('nickname', user.name)

        elif provider == 'naver':
            response = social_data.get('response', {})

            user.nickname = response.get('nickname', user.nickname or f'Naver_{user.id}')
            user.profile_image = response.get('profile_image', user.profile_image)
            user.name = response.get('name', user.name)

        elif provider == 'github':
            user.nickname = social_data.get('login', user.nickname or f'GitHub_{user.id}')
            user.profile_image = social_data.get('avatar_url', user.profile_image)
            user.name = social_data.get('name', user.name)

        # 신규 사용자 플래그 설정
        setattr(user, '_is_new_user', is_new_user)

        # 포지션이 설정되지 않은 경우 기본값 설정
        if not user.position:
            user.position = 1
            user.position_name = "백엔드(BE)"

        user.save()
        return user