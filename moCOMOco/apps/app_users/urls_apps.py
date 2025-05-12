from django.urls import path, include
from . import views
from .social_views import KakaoLoginView, NaverLoginView, GithubLoginView
from .url_views import SocialLoginURLView
from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.views import LogoutView
from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
    # dj-rest-auth 경로
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),

    # 소셜 로그인 URL
    path('login/url/<str:provider>/', SocialLoginURLView.as_view(), name='social_login_url'),

    # 소셜 로그인 콜백 처리
    path('login/kakao/', KakaoLoginView.as_view(), name='kakao_login'),
    path('login/naver/', NaverLoginView.as_view(), name='naver_login'),
    path('login/github/', GithubLoginView.as_view(), name='github_login'),

    # JWT 토큰 관련
    path('token/refresh/', get_refresh_view().as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # 사용자 관리
    path('users/me/', views.UserDetailView.as_view(), name='user_detail'),
    path('users/me/delete/', views.UserDetailView.as_view(), name='user_delete'),
    path('users/position/', views.PositionView.as_view(), name='user_position'),

    # 이미지 업로드 전용 엔드포인트 추가
    path('users/me/upload-image/', views.upload_profile_image, name='upload_profile_image'),
]