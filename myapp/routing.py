# myapp/routing.py

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/timer/', consumers.TimerConsumer.as_asgi()),
    # Define your WebSocket URL patterns and corresponding consumers
    # Example: path('ws/chat/', consumers.ChatConsumer.as_asgi()),
]
