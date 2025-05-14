from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    """
    커스텀 유저 모델 관리자 클래스
    -유저 중심으로 운영되는 사이트
    -create_user": 사용자 생성 메서드
    """

    def create_user(self,email, password=None, **extra_fields):
        # 이메일은 필수 입력값으로 설정
        if not email:
            raise ValueError('이메알은 필수 입니다.')

        #이메일 정규화(소문자 변환 등)
        email = self.normalize_email(email)

        #user = 객처 생성
        user = self.model(email=email, **extra_fields)
        user.set_password(password) #비밀번호 해싱 처리
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password=None, **extra_fields):
        """
        슈퍼유저(관리자) 생성 메서드
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('슈퍼유저는 is_staff=True 여야 합니다.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('슈퍼유저는 is_superuser=True 여야 합니다.')

        return self.create_user(email, password, nickname=nickname, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
    커스텀 유저 모델
    - AbstractBaseUser: Django 의 기번 인증 시스템 활용
    - PermissionsMixin: 권한 관련 기능 포함 하되 관리자 기능 사용 안함
    """
    #기본 식별자 및 OAuth 관련 필드 작성
    id = models.AutoField(primary_key=True)
    provider = models.CharField(max_length=20, null=True, blank=True) # kakao, naver 등 소셜 로그인 제공자
    access_token = models.TextField(null=True, blank=True)  #OAuth 제공자 의 access_token 저장

    # 기본 사용자 정보
    email = models.EmailField(unique=True) # 이메일 을 고유 식별자 로 사용
    name = models.CharField(max_length=100, null=True, blank=True) # 사용자 이름
    nickname = models.CharField(max_length=20,) # 사용자 닉네임
    profile_image = models.URLField(max_length=500, null=True, blank=True)  # 프로필 이미지 URL
    phone = models.CharField(max_length=20, null=True, blank=True) # 사용자 핸드폰 번호
    #birthday = models.DateField(null=True, blank=True) # 사용자 태어난 날짜S
    #address = models.CharField(max_length=200, null=True, blank=True) # 사용자 거주지
    github_url = models.URLField(null=True, blank=True) # 사용자 github 주소 등록
    portfolio_url = models.URLField(null=True, blank=True) # 사용자 사진 등록
    intro = models.TextField(null=True, blank=True) # 사용자 설명란

    # 포지션 정보(API 문서에 따른 포지션 타입)
    position = models.IntegerField(default=True, blank=True) # 기본값 없음(사용자가 선택할수 있게 기본값이없음)
    position_name = models.CharField(max_length=100, null=True, blank=True)

    # Django 모델 필수 필드
    is_active = models.BooleanField(default=True) # 계정 활성화 여부
    is_staff = models.BooleanField(default=False, editable=False) # 관리자 사이트 접근 불가
    is_superuser = models.BooleanField(default=False, editable=False) # 슈퍼 유저 권한 없음
    created_at = models.DateTimeField(auto_now_add=True) # 생성 시간 자동 기록
    updated_at = models.DateTimeField(auto_now=True) # 수정 시간 자동 기록

    # UserManger 연걸
    objects = UserManager()

    # Django 인증 시스템 에서 사용할 필드 지정
    USERNAME_FIELD = 'email'  # 로그인 에 사용할 필드
    REQUIRED_FIELDS = ['nickname'] # createsuperuser 명령어 실행 시 여구할 추가 필드

    def __str__(self):
        return self.email