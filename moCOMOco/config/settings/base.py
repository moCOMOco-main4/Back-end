import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

# ─── 경로 설정 ─────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / 'apps'))

# ─── .env 로드 ─────────────────────────────────────────────
env_path = BASE_DIR / '.env'
if env_path.exists():
    load_dotenv(env_path)

def get_env_variable(var_name, default=None, required=False):
    value = os.getenv(var_name, default)
    if required and value is None:
        raise ValueError(f"필수 환경 변수 {var_name}이(가) 설정되지 않았습니다.")
    return value

# ─── 보안 설정 ─────────────────────────────────────────────
SECRET_KEY = get_env_variable('SECRET_KEY', 'django-insecure-development-key-change-in-production')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = []  # dev.py 또는 prod.py에서 개별 설정

# ─── 프론트엔드 URL (CORS 및 리다이렉트에 사용) ───────────────
FRONTEND_URL = get_env_variable('FRONTEND_URL', 'http://localhost:3000')

# ─── 사용자 모델 ───────────────────────────────────────────
AUTH_USER_MODEL = 'app_users.User'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ─── installed apps ───────────────────────────────────────
INSTALLED_APPS = [
    # 기본 앱
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # 서드파티
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.kakao',
    'allauth.socialaccount.providers.naver',
    'allauth.socialaccount.providers.github',
    'django_extensions',

    # 로컬 앱
    'apps.app_users.apps.UsersConfig',
]

# ─── 미들웨어 ─────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

# ─── URL / WSGI ───────────────────────────────────────────
ROOT_URLCONF = 'config.urls.urls_dev'  # prod에서는 urls_prod로 오버라이드
WSGI_APPLICATION = 'config.wsgi.application'

# ─── 템플릿 ───────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ─── 데이터베이스 ──────────────────────────────────────────
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

# ─── CORS 설정 ────────────────────────────────────────────
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [FRONTEND_URL]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT"]
CORS_ALLOW_HEADERS = [
    "accept", "accept-encoding", "authorization", "content-type",
    "dnt", "origin", "user-agent", "x-csrftoken", "x-requested-with"
]
CORS_EXPOSE_HEADERS = ["Content-Type", "X-CSRFToken"]

# ─── DRF 설정 ─────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'API 문서',
    'DESCRIPTION': '코모코모 프로젝트 API 명세',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# ─── JWT 설정 ─────────────────────────────────────────────
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'access_token',
    'JWT_AUTH_REFRESH_COOKIE': 'refresh_token',
    'JWT_AUTH_HTTPONLY': True,
    'USER_DETAILS_SERIALIZER': 'apps.app_users.serializers.UserDetailSerializer',
}

# ─── allauth 인증 백엔드 ────────────────────────────────
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# ─── allauth 기본 설정 ───────────────────────────────────
SITE_ID = 1
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_ADAPTER = 'apps.app_users.adapters.CustomAccountAdapter'
SOCIALACCOUNT_ADAPTER = 'apps.app_users.adapters.CustomSocialAccountAdapter'
ACCOUNT_UNIQUE_EMAIL = True
SOCIALACCOUNT_LOGIN_ON_GET = True

# ─── 리다이렉트 URL ──────────────────────────────────────
LOGIN_REDIRECT_URL = FRONTEND_URL
LOGOUT_REDIRECT_URL = FRONTEND_URL

# ─── 소셜 로그인 설정 ───────────────────────────────────
KAKAO_CLIENT_ID = get_env_variable('KAKAO_CLIENT_ID', '')
KAKAO_CLIENT_SECRET = get_env_variable('KAKAO_CLIENT_SECRET', '')
KAKAO_REDIRECT_URI = get_env_variable('KAKAO_REDIRECT_URI', 'http://localhost:8000/accounts/kakao/callback/')

NAVER_CLIENT_ID = get_env_variable('NAVER_CLIENT_ID', '')
NAVER_CLIENT_SECRET = get_env_variable('NAVER_CLIENT_SECRET', '')
NAVER_REDIRECT_URI = get_env_variable('NAVER_REDIRECT_URI', 'http://localhost:8000/accounts/naver/callback/')
NAVER_STATE = get_env_variable('NAVER_STATE', 'RANDOM_STATE')

GITHUB_CLIENT_ID = get_env_variable('GITHUB_CLIENT_ID', '')
GITHUB_CLIENT_SECRET = get_env_variable('GITHUB_CLIENT_SECRET', '')
GITHUB_REDIRECT_URI = get_env_variable('GITHUB_REDIRECT_URI', 'http://localhost:8000/accounts/github/callback/')

SOCIALACCOUNT_PROVIDERS = {
    'kakao': {
        'APP': {
            'client_id': KAKAO_CLIENT_ID,
            'secret': KAKAO_CLIENT_SECRET,
            'key': ''
        },
        'SCOPE': ['account_email', 'profile_nickname'],
        'PROFILE_FIELDS': ['email', 'nickname', 'profile_image_url'],
    },
    'naver': {
        'APP': {
            'client_id': NAVER_CLIENT_ID,
            'secret': NAVER_CLIENT_SECRET,
            'key': ''
        },
        'SCOPE': ['email', 'name', 'nickname', 'profile_image'],
    },
    'github': {
        'APP': {
            'client_id': GITHUB_CLIENT_ID,
            'secret': GITHUB_CLIENT_SECRET,
            'key': ''
        },
        'SCOPE': ['user:email', 'read:user'],
    }
}

# ─── 비밀번호 검증 ────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─── 국제화 / 시간대 ──────────────────────────────────────
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True

# ─── 정적 파일 설정 ──────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
