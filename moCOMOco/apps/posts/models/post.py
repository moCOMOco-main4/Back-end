from django.db import models
from django.conf import settings


CATEGORY_CHOICES = [
    ('study', '스터디'),
    ('project', '프로젝트'),
]


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
    address = models.TextField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    image = models.ImageField(upload_to='posts/images/', null=True, blank=True)
    date = models.DateTimeField()

    max_people = models.PositiveIntegerField()
    is_closed = models.BooleanField(default=False)

    roles = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.nickname}"
