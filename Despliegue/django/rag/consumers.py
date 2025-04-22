import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "chat_rag"
        self.room_group_name = f"chat_{self.room_name}"

        # Unir al grupo
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Dejar el grupo
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Recibir un mensaje desde WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        task_id = text_data_json['task_id']

        # Simular respuesta de RAG (en este caso solo un mensaje fijo)
        response = "Respuesta procesada por RAG"

        # Enviar mensaje al grupo
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'status': 'completed',
                'response': response
            }
        )

    # Recibir mensaje desde el grupo
    async def chat_message(self, event):
        response = event['response']

        # Enviar el mensaje a WebSocket
        await self.send(text_data=json.dumps({
            'status': 'completed',
            'response': response
        }))
