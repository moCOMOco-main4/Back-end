from django.apps import AppConfig

class PostsConfig(AppConfig):
    name = 'apps.posts'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import apps.posts.utils.signals