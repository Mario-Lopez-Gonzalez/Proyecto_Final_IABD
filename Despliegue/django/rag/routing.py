from django.urls import path
from .consumers import ChatRAGConsumer  # Importa el consumidor WebSocket

websocket_urlpatterns = [
    path("ws/chat-rag/", ChatRAGConsumer.as_asgi()),
]
