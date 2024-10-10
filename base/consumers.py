import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatMessage, CustomUser, Experience

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get experience ID and vendor ID from URL
        self.experience_id = self.scope['url_route']['kwargs'].get('experience_id')
        self.vendor_id = self.scope['url_route']['kwargs'].get('vendor_id')
        self.room_name = f'chat_{self.experience_id}_{self.vendor_id}'
        
        # Join the room group
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'message':
            message = data.get('message')
            experience_id = data.get('experience_id')
            vendor_id = data.get('vendor_id')
            sender = self.scope['user']  # Use the authenticated user

            # Save the message to the database
            await self.save_message(sender, vendor_id, experience_id, message)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': sender.username if sender.is_authenticated else 'Anonymous',
                }
            )

        elif message_type == 'typing':
            # Broadcast typing indicator to the room
            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'typing_indicator',
                    'sender': self.scope['user'].username if self.scope['user'].is_authenticated else 'Anonymous',
                }
            )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': message,
            'sender': sender,
        }))

    async def typing_indicator(self, event):
        sender = event['sender']

        # Send typing indicator to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'sender': sender,
        }))

    @database_sync_to_async
    def save_message(self, sender, vendor_id, experience_id, message):
        # Check for vendor and experience existence before saving
        vendor = CustomUser.objects.filter(id=vendor_id).first()
        experience = Experience.objects.filter(id=experience_id).first()

        if vendor and experience:  # Ensure both exist
            return ChatMessage.objects.create(
                user=sender,
                vendor=vendor,
                experience=experience,
                message=message
            )
        else:
            print(f'Error: Vendor {vendor_id} or Experience {experience_id} does not exist.')
            return None
