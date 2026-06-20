import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django_asgi = get_asgi_application()

try:
    from channels.routing import ProtocolTypeRouter, URLRouter
    from channels.auth import AuthMiddlewareStack
    from notifications.routing import websocket_urlpatterns

    application = ProtocolTypeRouter({
        "http": django_asgi,
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    })
except ImportError:
    # Channels not installed — fall back to plain ASGI
    application = django_asgi
