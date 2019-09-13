# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

from outer_libraries.cheapFlightsFinder import get_cheap_flights_for_given_city


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_name = 'adin'
        # self.room_group_name = 'chat_%s' % self.room_name
        self.room_group_name = 'group1'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        print("zaczynam szukac loty")
        cheap_flights, cheap_flights_short = get_cheap_flights_for_given_city()
        print("skonczylem szukac loty, wysylam")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': cheap_flights_short
            }
        )
        print("wyslalem liste lotow")

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'cheap_flights': message
        }))