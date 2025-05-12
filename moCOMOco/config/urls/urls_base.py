from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)

router = DefaultRouter()

urlpatterns = [
    # Django 관리자 페이지
    path('admin/', admin.site.urls),

    # REST Framework URL
    path('api/', include(router.urls)),

    # REST Framework 인증 URL
    path('api-auth/', include('rest_framework.urls')),

    # dj-rest-auth 인증 및 소셜 로그인 URL
    path('api/auth/', include('apps.app_users.urls_apps')),

    # 모임글 신청 API
    path('api/posts/', include('apps.posts.urls.post_urls')),  # 모집글 관련 API
    path('api/applications/', include('apps.posts.urls.application_urls')),  # 신청 관련 API
    path('api/schedules/', include('apps.posts.urls.schedule_urls')),  # 일정 관련 API

    # Swagger UI URL 패턴
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # Django-allauth 소셜 로그인 콜백 URL (필요한 경우)
    path('accounts/', include('allauth.urls')),
    path('chat/', include('apps.chat.urls')),
    path('notifications/', include('apps.notifications.urls'))

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
