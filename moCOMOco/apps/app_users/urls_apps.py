# apps/app_users/urls_apps.py
from django.urls import path, include
from . import views
from .social_views import KakaoLoginView, NaverLoginView, GithubLoginView, UserLogoutView
from .url_views import SocialLoginURLView
from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.views import LogoutView
from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('login/url/<str:provider>/', SocialLoginURLView.as_view(), name='social_login_url'),
    path('login/kakao/', KakaoLoginView.as_view(), name='kakao_login'),
    path('login/naver/', NaverLoginView.as_view(), name='naver_login'),
    path('login/github/', GithubLoginView.as_view(), name='github_login'),
    path('token/refresh/', get_refresh_view().as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('users/me/', views.UserDetailView.as_view(), name='user_detail'),
    path('users/me/delete/', views.UserDetailView.as_view(), name='user_delete'),
    path('users/position/', views.PositionView.as_view(), name='user_position'),
    path('users/<int:user_id>/profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('users/me/upload-image/', views.upload_profile_image, name='upload_profile_image'),
]