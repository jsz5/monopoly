import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from api.models import PlayingUser, FieldType, Field, Messages, Asset, Estate
from django.contrib.auth.models import User
import random

# from .models import Game


class LobbyConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print(self.scope["user"])
        self.user = User.objects.filter(username=self.scope["user"]).first()
        self.lobby_group_name = 'game'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.lobby_group_name,
            self.channel_name
        )

        self.__add_playing_user()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)

        self.__check_game_availability()

    def __add_playing_user(self):
        # todo: nie dodawać podwórjnie etc.
        PlayingUser(user=self.user).save()

    def __check_game_availability(self):
        if not PlayingUser.objects.filter(isPlaying=True).first():
            print(PlayingUser.objects.all().count())
            all_users = PlayingUser.objects.count()
            active_users = PlayingUser.objects.filter(isActive=True).count()
            print(active_users)

            if 2 <= all_users < 4:
                print('two or three players')
                # gracze z tabeli mogą rozpocząć grę (przycisk ROZPOCZNIJ GRĘ jest dostępny) - event
                async_to_sync(self.channel_layer.group_send)(
                    self.lobby_group_name, {
                        'type': 'lobby_message',
                        'message': 'load'
                    }
                )
            elif all_users == 4 or active_users == all_users:
                # gra rozpoczyna się automatycznie - event
                print('four players')
                async_to_sync(self.channel_layer.group_send)(
                    self.lobby_group_name, {
                        'type': 'lobby_message',
                        'message': 'start'
                    }
                )

    # Receive message from room group
    def lobby_message(self, event):
        message = event['message']

        print(message)

        if message == 'start':
            user = PlayingUser.objects.filter(user=self.user).first()
            user.isActive = True
            user.save()

            playing_order = list(PlayingUser.objects.filter(isActive=True))
            random.shuffle(playing_order)
            start_field = FieldType.objects.filter(name="START").first().get_field
            for place, playing_user in enumerate(playing_order):
                if place == 0:
                    playing_user.isPlaying = True
                playing_user.place = place + 1
                playing_user.field = start_field
                playing_user.budget = 15000
                playing_user.save()

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

    def disconnect(self, close_code):
        self.close()
        # Called when the socket closes


class BoardConsumer(WebsocketConsumer):
    def connect(self):
        # self.board_name = self.scope['url_route']['kwargs']['board_name']
        self.board_group_name = 'board'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.board_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave board group
        async_to_sync(self.channel_layer.group_discard)(
            self.board_group_name,
            self.channel_name
        )

    # TODO: Here
    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['button']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.board_group_name, {
                'type': 'board_message',
                'message': message
            }
        )

    # Receive message from room group
    def board_message(self, event):
        message = 'Clicked' + event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

# class BoardConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.board_name = self.scope['url_route']['kwargs']['board_name']
#         self.board_group_name = 'board_%s' % self.board_name

#         # Join room group
#         await self.channel_layer.group_add(
#             self.board_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave bodar group
#         await self.channel_layer.group_discard(
#             self.channel_name
#         )

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['button']

#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.board_group_name, {
#                 'type': 'board_message',
#                 'message': message
#             }
#         )

#     # Receive message from room group
#     async def board_message(self, event):
#         message = 'Clicked' + event['message']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))
