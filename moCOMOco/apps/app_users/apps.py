from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Django 앱 설정 클래스(앱의 기본 설정을 정의)
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.app_users"
    path = "apps.app_users"

    def ready(self):
        # 시그널 로직을 함수로 분리
        import logging
        logger = logging.getLogger(__name__)

        # 시그널 처리는 임포트만 하고 함수 정의는 별도 파일에서 처리
        try:
            import apps.app_users.signals
            logger.info("User signals imported successfully")
        except Exception as e:
            logger.error(f"Failed to import user signals: {e}")