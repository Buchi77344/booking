import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatMessage
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.experience_id = self.scope['url_route']['kwargs']['experience_id']
        self.vendor_id = self.scope['url_route']['kwargs']['vendor_id']
        self.room_group_name = f'chat_{self.experience_id}'

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        # Handle message sending
        if data['type'] == 'message':
            message = data['message']
            vendor_id = data['vendor_id']
            experience_id = data['experience_id']
            sender = self.scope["user"]

            # Save the message to the database
            await self.save_message(sender, vendor_id, experience_id, message)

            # Send the message to the room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': sender.username
                }
            )
        elif data['type'] == 'typing':
            # Send typing notification to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_notification',
                    'sender': data['sender']
                }
            )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': message,
            'sender': sender
        }))

    async def typing_notification(self, event):
        sender = event['sender']

        # Send the typing notification to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'sender': sender
        }))

    @database_sync_to_async
    def save_message(self, user, vendor_id, experience_id, message):
        # Save the message in the database
        chat_message = ChatMessage(
            user=user,
            vendor_id=vendor_id,
            experience_id=experience_id,
            message=message
        )
        chat_message.save()
