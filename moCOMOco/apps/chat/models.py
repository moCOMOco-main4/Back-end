from django.db import models
from django.conf import settings

class ChatRoomParticipant(models.Model):
    participant_id = models.AutoField(
        primary_key=True,
        db_column='participant_id'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='User_id'
    )
    room_id = models.CharField(
        max_length=100,
        db_column='room_id'
    )
    alarm_on = models.BooleanField(
        default=True,
        db_column='alarm_on'
    )
    joined_at = models.DateTimeField(
        auto_now_add=True,
        db_column='joined_at'
    )

    class Meta:
        db_table = 'Chat_room_participant'
        verbose_name = '채팅방 참여자'

class ChatMessage(models.Model):
    ChatMessage_id = models.AutoField(
        primary_key=True,
        db_column='ChatMessage_id'
    )

    chat_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column='chat_user_id',
        related_name='chat_messages'
    )
    room_id = models.CharField(
        max_length=100,
        db_column='room_id'
    )
    content = models.TextField(
        db_column='content'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_column='created_at'
    )
    updated_at = models.DateTimeField(
        null=True, blank=True,
        db_column='updated_at'
    )
    is_deleted = models.BooleanField(
        default=False,
        db_column='is_deleted'
    )

    class Meta:
        db_table = 'ChatMessage'
        verbose_name = '채팅 메시지'
        ordering = ['created_at']
