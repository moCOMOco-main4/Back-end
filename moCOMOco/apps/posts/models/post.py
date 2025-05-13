from django.db import models
from django.conf import settings

CATEGORY_CHOICES = [
    ('project', '프로젝트'),
    ('study', '스터디'),
]

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    date = models.DateTimeField()
    place_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    image = models.ImageField(
        upload_to='posts/images/',
        null=True,
        blank=True,
        default='posts/images/default.png'
    )

    is_closed = models.BooleanField(default=False)
    max_people = models.PositiveIntegerField()
    roles = models.JSONField(default=dict)  # 예: {"frontend": 2, "backend": 2, "designer": 1}
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
