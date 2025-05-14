from django.db import models
from django.conf import settings
from apps.posts.models.post import Post


ROLE_CHOICES = [
    ('backend', '백엔드'),
    ('frontend', '프론트엔드'),
    ('designer', '디자이너'),
]


class Application(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='applications',
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_user_post')
        ]

    def __str__(self):
        return f"{self.user.nickname} -> {self.post.title} ({self.role})"
