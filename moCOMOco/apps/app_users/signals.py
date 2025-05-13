from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def log_user_save(sender, instance, created, **kwargs):
    """사용자 생성 또는 업데이트 시 로그 남기기"""
    if created:
        print(f"[DEBUG] 새 사용자 생성: {instance.email}, Provider: {instance.provider}, "
              f"Nickname: {instance.nickname}, Name: {instance.name}")
    else:
        print(f"[DEBUG] 사용자 업데이트: {instance.email}, Provider: {instance.provider}, "
              f"Nickname: {instance.nickname}, Name: {instance.name}")