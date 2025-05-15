import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

import django
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from apps.chat.middleware import JWTAuthMiddleware
import apps as chat_routing

application = ProtocolTypeRouter({
  "http":      get_asgi_application(),
  "websocket": JWTAuthMiddleware(
      URLRouter(chat_routing.websocket_urlpatterns)
  ),
})