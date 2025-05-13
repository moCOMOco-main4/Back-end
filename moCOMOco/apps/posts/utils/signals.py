from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.posts.models.application import Application


# 모집 정원 다 찼을 때 자동 마감
@receiver(post_save, sender=Application)
def auto_close_post_if_full(sender, instance, created, **kwargs):
    if not created:
        return

    post = instance.post
    role = instance.role

    max_count = post.roles.get(role, 0)
    current_count = Application.objects.filter(post=post, role=role).count()
    total_current = Application.objects.filter(post=post).count()
    total_max = sum(post.roles.values())

    if current_count >= max_count or total_current >= total_max:
        if not post.is_closed:
            post.is_closed = True
            post.save()


# 신청자 삭제 시 자동 재오픈
@receiver(post_delete, sender=Application)
def auto_reopen_post_if_not_full(sender, instance, **kwargs):
    post = instance.post
    total_current = Application.objects.filter(post=post).count()
    total_max = sum(post.roles.values())

    if total_current < total_max and post.is_closed:
        post.is_closed = False
        post.save()
