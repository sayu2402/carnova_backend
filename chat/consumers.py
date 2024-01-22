import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Chat
from accounts.models import *
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender_id = self.scope["url_route"]["kwargs"]["sender_id"]
        self.receiver_id = self.scope["url_route"]["kwargs"]["receiver_id"]
        self.room_channel_name = f"chat_{min(self.sender_id, self.receiver_id)}_{max(self.sender_id, self.receiver_id)}"

        # Connect to the individual channel for this pair
        await self.channel_layer.group_add(self.room_channel_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_channel_name, self.channel_name
        )

    @database_sync_to_async
    def create_message(self, message, sender, receiver):
        message_obj = Chat.objects.create(
            message=message, sender=sender, receiver=receiver
        )
        return message_obj

    @database_sync_to_async
    def get_user(self, id):
        return UserAccount.objects.get(id=id)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        sender_id = self.scope["url_route"]["kwargs"]["sender_id"]
        receiver_id = self.scope["url_route"]["kwargs"]["receiver_id"]
        receiver = await self.get_user(receiver_id)
        sender = await self.get_user(sender_id)

        # Create a new message object and save it to the database
        message_obj = await self.create_message(message, sender, receiver)
        username = sender.username

        # Send the message to the individual channel for this pair
        await self.channel_layer.group_send(
            self.room_channel_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender_id,
                "timestamp": str(message_obj.timestamp),
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        timestamp = event["timestamp"]
        sender = event["sender"]

        # Send the message to the websocket
        await self.send(
            text_data=json.dumps(
                {"message": message, "sender": sender, "timestamp": timestamp}
            )
        )


class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "user"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        user_id = data["user_id"]
        connection_type = data["type"]
        await self.change_online_status(user_id, connection_type)

    async def send_onlineStatus(self, event):
        data = json.loads(event.get("value"))
        user_id = data["id"]
        online_status = data["status"]
        await self.send(
            text_data=json.dumps({"user_id": user_id, "online_status": online_status})
        )

    async def disconnect(self, message):
        self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    @database_sync_to_async
    def change_online_status(self, user_id, c_type):
        try:
            user = UserAccount.objects.get(id=user_id)
        except UserAccount.DoesNotExist:
            return

        if c_type == "open":
            user.online_status = True
        else:
            user.online_status = False

        user.save()


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("WebSocket connected")
        self.group_name = 'vendor_notifications'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        print("Sending notification:", event)
        if event['notification_type'] == 'car_approved':
            await self.send(text_data=json.dumps({'message': event['message'], 'notification_type': 'car_approved'}))
            print("Notification sent successfully")
