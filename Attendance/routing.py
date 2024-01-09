# myproject/routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from myapp.consumers import TimerConsumer  # Import your consumer

websocket_urlpatterns = [
    path('ws/timer/', TimerConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': URLRouter(websocket_urlpatterns),
})
