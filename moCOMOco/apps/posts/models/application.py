from django.db import models
from django.conf import settings

# 역할군 선택지
ROLE_CHOICES = [
    ('backend', '백엔드'),
    ('frontend', '프론트엔드'),
    ('designer', '디자이너'),
    ('full_stack', '풀스택'),
]

# Application 모델: 모집글에 대한 신청 내역
class Application(models.Model):
    # 신청자 (User와 연결)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications',
    )

    # 어떤 모집글에 신청했는지
    post = models.ForeignKey(
        'posts.Post',  # 지연 참조 방식으로 순환참조 방지
        on_delete=models.CASCADE,
        related_name='applications',
    )

    # 신청한 역할
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # 신청 시간
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'posts'

        # 동일 모집글에 중복 신청 방지
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_user_post')
        ]

    def __str__(self):
        return f"{self.user} -> {self.post.title} ({self.role})"
