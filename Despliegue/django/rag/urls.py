"""
from django.urls import path
from .views import chat_view, execute_rag

urlpatterns = [
    path('chat/', chat_view, name='rag_chat'),
    path('run-rag/', execute_rag, name='execute_rag'),
]
"""
from django.urls import path
from . import views

urlpatterns = [
    path('rag/chat/', views.rag_chat, name='rag_chat'),
    #path('rag/send/', views.rag_send_message, name='rag_send_message'),  # Definir la URL para enviar mensajes
    path('rag/send-message/', views.rag_send_message, name='rag_send_message'),
]

