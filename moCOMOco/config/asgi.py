import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

from django.core.asgi import get_asgi_application
asgi_application = get_asgi_application()


from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from apps.chat.middleware import JWTAuthMiddlewareStack
from apps.chat.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": asgi_application,
    "websocket": AllowedHostsOriginValidator(
        JWTAuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    ),
})