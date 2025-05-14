from django.db import models
from django.conf import settings

CATEGORY_CHOICES = [
    ('project', '프로젝트'),
    ('study', '스터디'),
]

class Post(models.Model):
    # 작성자
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    # 모집글 필드
    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    date = models.DateTimeField()
    place_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    # 이미지 (선택)
    image = models.ImageField(
        upload_to='posts/images/',
        null=True,
        blank=True,
        default='posts/images/default.png'
    )

    # 모집 관련
    is_closed = models.BooleanField(default=False)
    max_people = models.PositiveIntegerField()  # 전체 모집 인원
    roles = models.JSONField(default=dict)      # 역할별 인원 ex) {"frontend": 2, "backend": 3}

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    # 현재 전체 참여 인원 (신청된 개수)
    @property
    def current_people(self):
        return self.applications.count()

    # 전체 인원 현황 ex) "3/5"
    @property
    def people_status(self):
        return f"{self.current_people}/{self.max_people}"

    # 역할별 모집 현황 ex) {"backend": "2/3", "frontend": "1/2"}
    @property
    def role_status(self):
        from apps.posts.models.application import Application  # 순환 import 방지

        result = {}
        for role, max_count in self.roles.items():
            current_count = Application.objects.filter(post=self, role=role).count()
            result[role] = f"{current_count}/{max_count}"
        return result
