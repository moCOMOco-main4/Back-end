from django.db import models
from apps.posts.models.post import Post

class Schedule(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='schedules')
    date = models.DateTimeField()
    memo = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['post', 'date'], name='unique_post_schedule_date')
        ]
