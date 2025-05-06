from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView,  SpectacularRedocView

# 개발용 URL 구성은 base와 동일하게 사용
urlpatterns = base_urlpatterns