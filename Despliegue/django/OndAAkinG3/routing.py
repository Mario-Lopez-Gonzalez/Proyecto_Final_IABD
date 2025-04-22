from django.urls import re_path
from rag import consumers  # Asegúrate de crear un consumer

websocket_urlpatterns = [
    re_path(r'ws/chat-rag/', consumers.ChatConsumer.as_asgi()),  # Asegúrate de que 'ChatConsumer' esté implementado
]
