from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.posts.models.application import Application
from apps.chat.models import ChatRoomParticipant
from apps.notifications.services import NotificationService


@receiver(post_save, sender=Application)
def auto_close_post_if_full(sender, instance, created, **kwargs):
    if not created:
        return

    post = instance.post
    role = instance.role
    current_count = Application.objects.filter(post=post, role=role).count()
    total_current = Application.objects.filter(post=post).count()
    total_max = sum(post.roles.values())

    if current_count >= post.roles.get(role, 0) or total_current >= total_max:
        if not post.is_closed:
            post.is_closed = True
            post.save()


@receiver(post_delete, sender=Application)
def auto_reopen_post_if_not_full(sender, instance, **kwargs):
    post = instance.post
    total_current = Application.objects.filter(post=post).count()
    total_max = sum(post.roles.values())
    if total_current < total_max and post.is_closed:
        post.is_closed = False
        post.save()


@receiver(post_save, sender=Application)
def on_application_accepted(sender, instance, created, **kwargs):
    if created:
        return
    if getattr(instance, 'status', None) == 'accepted':
        NotificationService.send_apply_accepted(instance)
        ChatRoomParticipant.objects.get_or_create(
            user=instance.user,
            room_id=str(instance.post.id),
            defaults={'alarm_on': True}
        )

