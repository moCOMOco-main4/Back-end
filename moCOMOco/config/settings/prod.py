from .base import *

# 디버그 모드 비활성화
DEBUG = True

# 실제 운영 도메인으로 변경
ALLOWED_HOSTS = [
   # 'api.mocomoco.store',
   # '15.164.219.164',
   # 'www.mocomoco.store',
   # 'localhost:3000',
   '*'
]
# 프론트엔드 도메인
# CORS_ALLOWED_ORIGINS = [
#    'https://www.mocomoco.store',
# ]
# CORS_ALLOW_CREDENTIALS = True

# PostgreSQL 데이터베이스 설정
# ROOT_URLCONF = 'config.urls.urls_prod'

DATABASES = {
    'default': {
        'ENGINE': get_env_variable('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': get_env_variable('DB_NAME', 'django_db'),
        'USER': get_env_variable('DB_USER', ''),
        'PASSWORD': get_env_variable('DB_PASSWORD', ''),
        'HOST': get_env_variable('DB_HOST', 'localhost'),
        'PORT': get_env_variable('DB_PORT', '5432'),
    }
}

# 강화된 보안 설정
SECURE_HSTS_SECONDS = 31536000  # 1년
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# 추가 로깅 설정
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# 추가 로깅 설정
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
