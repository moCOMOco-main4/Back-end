from django.db import models
from django.conf import settings
from apps.posts.models.post import Post

ROLE_CHOICES = [
    ('designer', '디자이너'),
    ('backend', '백엔드'),
    ('frontend', '프론트엔드'),
]


class Application(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='applications')
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(
        max_length=15,
        choices=ROLE_CHOICES,
        default='backend',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_user_post')
        ]
