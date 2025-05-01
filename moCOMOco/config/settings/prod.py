from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    "www.mocomoco.store",
    "mocomoco.store",
    "127.0.0.1",
    "localhost",
    "15.164.219.164",
]

# 배포용 PostgreSQL 데이터베이스 (나중에 필요할 때 설정)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'django_db'),
        'USER': os.environ.get('DB_USER', 'huitae.95'),  # 사용자 이름 변경
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# 보안 설정
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
