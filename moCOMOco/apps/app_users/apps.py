from django.apps import AppConfig

class UsersConfig(AppConfig):
    """
    Django 앱 설정 클래스(앱의 기본 설정을 정의)
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.app_users"
    path = "apps.app_users"

