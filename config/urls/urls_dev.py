from django.contrib import admin
from django.urls import path, include
from ninja import NinjaAPI
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

# Ninja API 인스턴스 생성
api = NinjaAPI()

# 예제 엔드포인트
@api.get("/Ninja")
def hello(request):
    return {"message": "Hello from Django Ninja!"}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),

    # API 문서 URL
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]