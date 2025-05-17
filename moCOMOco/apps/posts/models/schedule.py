from django.db import models
from apps.posts.models.post import Post


class Schedule(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='schedules',
    )
    date = models.DateTimeField()
    memo = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post.title} 일정: {self.memo} @ {self.date}"

