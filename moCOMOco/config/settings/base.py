import sys
from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import timedelta

# ─── 프로젝트 기본 디렉터리 ────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent

sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / 'apps'))

# ─── .env 파일 로드 ──────────────────────────────────────────
env_path = BASE_DIR / '.env'
if env_path.exists():
    load_dotenv(env_path)


# 환경 변수 로드 함수 - 값이 없을 경우 기본값 사용
def get_env_variable(var_name, default=None, required=False):
    value = os.getenv(var_name, default)
    if required and value is None:
        raise ValueError(f"필수 환경 변수 {var_name}이(가) 설정되지 않았습니다.")
    return value


# ─── 보안 및 디버그 설정 ─────────────────────────────────────
SECRET_KEY = get_env_variable('SECRET_KEY', 'django-insecure-development-key-change-in-production')
DEBUG = get_env_variable('DEBUG', 'False') == 'True'

# ─── OAuth 환경변수 추가 ───────────────────────────────────────
KAKAO_CLIENT_ID = get_env_variable('KAKAO_CLIENT_ID', '')
KAKAO_REDIRECT_URI = get_env_variable('KAKAO_REDIRECT_URI', 'http://localhost:8000/accounts/kakao/callback/')
KAKAO_CLIENT_SECRET = get_env_variable('KAKAO_CLIENT_SECRET', '')

NAVER_CLIENT_ID = get_env_variable('NAVER_CLIENT_ID', '')
NAVER_CLIENT_SECRET = get_env_variable('NAVER_CLIENT_SECRET', '')
NAVER_REDIRECT_URI = get_env_variable('NAVER_REDIRECT_URI', 'http://localhost:8000/accounts/naver/callback/')
NAVER_STATE = get_env_variable('NAVER_STATE', 'RANDOM_STATE')

GITHUB_CLIENT_ID = get_env_variable('GITHUB_CLIENT_ID', '')
GITHUB_CLIENT_SECRET = get_env_variable('GITHUB_CLIENT_SECRET', '')
GITHUB_REDIRECT_URI = get_env_variable('GITHUB_REDIRECT_URI', 'http://localhost:8000/accounts/github/callback/')

# 웹 프론트엔드 URL (CORS 및 리다이렉트에 사용)
FRONTEND_URL = get_env_variable('FRONTEND_URL', 'http://localhost:3000')

# ─── 기본 자동 필드 ────────────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ─── 커스텀 유저 모델 ──────────────────────────────────────
AUTH_USER_MODEL = 'app_users.User'

# ─── REST Framework 설정 ─────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication', # simplejwt 사용
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}
# ─── dj-rest-auth 설정 ─────────────────────────────────────
REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'access_token',
    'JWT_AUTH_REFRESH_COOKIE': 'refresh_token',
    'USER_DETAILS_SERIALIZER': 'apps.app_users.serializers.UserDetailSerializer',
    'JWT_AUTH_HTTPONLY': True,  # 보안 강화를 위해 HttpOnly 설정
}

# ─── JWT 설정(dj-rest-auth가 사용하는 simplejwt 설정) ────────────────────────────────────────────────────
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,  # 리프레시 토큰 자동 갱신
    'BLACKLIST_AFTER_ROTATION': False,  # 토큰 블랙리스트 사용 안함
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# ─── 호스트 / CORS 설정 ─────────────────────────────────────
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]
CORS_ALLOW_ALL_ORIGINS = False  # 개발 중에는 모든 오리진 허용 나중에 True 바꿔야함

CORS_ALLOWED_ORIGINS = [
    FRONTEND_URL,  # 프론트엔드 서버 허용
]

# 추가적인 CORS 설정
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

# 인증 헤더 노출 허용
CORS_EXPOSE_HEADERS = ["Content-Type", "X-CSRFToken"]

# 쿠키 허용 (필요한 경우)
CORS_ALLOW_CREDENTIALS = True

# ─── 데이터베이스 설정 ───────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': get_env_variable('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': get_env_variable('DB_NAME', 'django_db'),
        'USER': get_env_variable('DB_USER', 'huitae.95'),
        'PASSWORD': get_env_variable('DB_PASSWORD', ''),
        'HOST': get_env_variable('DB_HOST', 'localhost'),
        'PORT': get_env_variable('DB_PORT', '5432'),
    }
}

# ─── 애플리케이션 정의 ───────────────────────────────────────
INSTALLED_APPS = [
    # Django 기본 앱
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # 필수
    'django_extensions',  # 이 줄 추가

    # 서드파티 앱
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',  # dj-rest-auth 연동을 위해 필요
    'rest_framework_simplejwt',  # JWT 인증
    'drf_spectacular',  # 이 부분 추가

    # dj-rest-auth
    'dj_rest_auth',
    'dj_rest_auth.registration',

    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.kakao',
    'allauth.socialaccount.providers.naver',
    'allauth.socialaccount.providers.github',

    # 로컬 앱
    'apps.app_users.apps.UsersConfig',
]

AUTHENTICATION_BACKENDS = [
    # Django 기본 인증 백엔드
    'django.contrib.auth.backends.ModelBackend',

    # allauth 소셜 로그인 백엔드
    'allauth.account.auth_backends.AuthenticationBackend',
]

# 사이트 ID 설정 (필수)
SITE_ID = 1

# ─── allauth 관련 설정 ────────────────────────────────────
ACCOUNT_AUTHENTICATION_METHOD = 'email' # 이메일 인증
ACCOUNT_EMAIL_REQUIRED = True # 이메일 필수
ACCOUNT_USERNAME_REQUIRED = False # 사용자 명 불필요
ACCOUNT_USER_MODEL_USERNAME_FIELD = None  # 사용자 모델의 username 필드 없음
ACCOUNT_EMAIL_VERIFICATION = 'none'  # 이메일 인증 비활성화 ('mandatory', 'optional', 'none')
ACCOUNT_ADAPTER = 'apps.app_users.adapters.CustomAccountAdapter'
SOCIALACCOUNT_ADAPTER = 'apps.app_users.adapters.CustomSocialAccountAdapter'
ACCOUNT_UNIQUE_EMAIL = True

# ─── 소셜 로그인 설정 ───────────────────────────────────────
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

LOGIN_REDIRECT_URL = FRONTEND_URL
LOGOUT_REDIRECT_URL = FRONTEND_URL

# 소셜 로그인 콜백 URL 명시적 설정
SOCIALACCOUNT_LOGIN_ON_GET = True

# ─── 미들웨어 정의 ───────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CommonMiddleware 이전에 위치
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # allauth 미들웨어 추가 (맨 마지막에)
    'allauth.account.middleware.AccountMiddleware',
]

# ─── URL 설정 ───────────────────────────────────────────────
ROOT_URLCONF = 'config.urls.urls_dev'

# ─── 템플릿 설정 ───────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # 루트 템플릿 디렉터리
        'APP_DIRS': True,  # 앱 내부의 templates/ 디렉터리도 검색
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

# ─── WSGI 설정 ────────────────────────────────────────────
WSGI_APPLICATION = 'config.wsgi.application'

# ─── 비밀번호 검증 ─────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─── 국제화 / 시간대 ────────────────────────────────────────
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True

# ─── 정적 파일(Static) 설정 ─────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'