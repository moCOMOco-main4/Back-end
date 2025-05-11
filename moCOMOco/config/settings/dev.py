from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# 개발용 SQLite 데이터베이스
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DRF Spectacular 설정
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Django Mini Project API',
    'DESCRIPTION': 'API documentation for Django Mini Project',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}