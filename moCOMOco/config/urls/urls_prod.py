from config.urls.urls_base import urlpatterns as base_urlpatterns
from django.urls.resolvers import URLPattern

# 운영용에서 Swagger 관련 라우트 제거
urlpatterns = [
    url for url in base_urlpatterns
    if not (
        isinstance(url, URLPattern) and url.name in ['schema', 'swagger-ui', 'redoc']
    )
]