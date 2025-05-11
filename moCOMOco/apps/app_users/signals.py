from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def set_default_position(_sender, instance, created, **_kwargs):
    """
    새 사용자가 생성될 때 기본 포지션 설정
    - 포지션 값이 없는 경우에만 기본값 설정
    """
    if created and not instance.position_name:
        instance.position = 1  # 기본값: 백엔드(BE)
        instance.position_name = "백엔드(BE)"
        # update_fields를 사용하여 다른 필드는 업데이트하지 않음
        instance.save(update_fields=['position', 'position_name'])