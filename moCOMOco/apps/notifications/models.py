from django.db import models
from django.conf import settings
from apps.chat.models import ChatMessage, ChatRoomParticipant

class Notification(models.Model):
    Notification_id = models.AutoField(
        primary_key=True,
        db_column='Notification_id'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='User_id'
    )
    post = models.ForeignKey(
        'posts.Post',
        on_delete=models.CASCADE,
        db_column='Post_id',
        null=True, blank=True,
    )
    application = models.ForeignKey(
        'posts.Application',
        on_delete=models.CASCADE,
        db_column='application_id',
        null=True, blank=True,
    )
    chat_message = models.ForeignKey(
        ChatMessage,
        on_delete=models.CASCADE,
        db_column='ChatMessage_id'
    )
    participant = models.ForeignKey(
        ChatRoomParticipant,
        on_delete=models.CASCADE,
        db_column='participant_id'
    )
    schedule = models.ForeignKey(
        'posts.Schedule',
        on_delete=models.CASCADE,
        db_column='schedule_id',
        null=True, blank=True,
    )
    content = models.CharField(
        max_length=255,
        db_column='content'
    )
    url = models.CharField(
        max_length=255,
        null=True, blank=True,
        db_column='url'
    )
    is_read = models.BooleanField(
        db_column='is_read'
    )
    type = models.CharField(
        max_length=230,
        db_column='type'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_column='created_at'
    )

    class Meta:
        db_table = 'NOTIFICATION'
        verbose_name = '알림'
        verbose_name_plural = '알림'
