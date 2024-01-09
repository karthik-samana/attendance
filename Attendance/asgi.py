"""
ASGI config for Attendance project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Attendance.settings')


# your_project_name/asgi.py

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import myapp.routing  # Import your routing configuration

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Attendance.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Use Django's ASGI application for HTTP
    "websocket": AuthMiddlewareStack(
        URLRouter(
            myapp.routing.websocket_urlpatterns  # Your WebSocket routing
        )
    ),
})

