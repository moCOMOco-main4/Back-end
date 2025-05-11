from django.db import models
from django.conf import settings

# 모임글 카테고리 선택
CATEGORY_CHOICES = [
    ('study', '스터디'),
    ('project', '프로젝트'),
]

# 신청 역할 선택
ROLE_CHOICES = [
    ('backend', '백엔드'),
    ('frontend', '프론트엔드'),
    ('designer', '디자이너'),
]

# 신청 상태 선택
STATUS_CHOICES = [
    ('pending', '대기중'),
    ('accepted', '수락됨'),
    ('rejected', '거절됨'),
]


# 모집글 모델
class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=15)

    place_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    roles = models.JSONField(default=dict)

    date = models.DateTimeField()
    is_closed = models.BooleanField(default=False)

    image = models.ImageField(
        upload_to='posts/images/',
        null=True,
        blank=True,
        help_text='대표이미지 프론트에서 파일로 보냄',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# 신청 모델
class Application(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='applications')

    role = models.CharField(max_length=15, choices=ROLE_CHOICES)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    # 탈퇴 사유
    leave_reason = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'post')  # 같은 글에 중복 신청 방지

# 일정 모델
class Schedule(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='schedules')
    date = models.DateField()
    memo = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
