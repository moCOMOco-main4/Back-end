from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps import ChatRoomParticipant
from apps import NotificationService

@receiver(post_save, sender=ChatRoomParticipant)
def on_chat_participant_join(sender, instance, created, **kwargs):
    if created:
        NotificationService.send_chat_join_notification(instance)

@receiver(post_delete, sender=ChatRoomParticipant)
def on_chat_participant_leave(sender, instance, **kwargs):
    NotificationService.send_chat_leave_notification(instance)