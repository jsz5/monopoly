import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from api.models import PlayingUser, FieldType, Field, Zone, Messages, Asset, Estate
from django.contrib.auth.models import User
import random


class LobbyConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.user = self.scope['user'] #User.objects.filter(username=self.scope["user"]).first()
        self.lobby_group_name = 'game'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.lobby_group_name,
            self.channel_name
        )

        self.__add_playing_user()
        self.__check_game_availability()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(f"RECEIVE {text_data_json['type']}")
        if text_data_json['type'] == 'start_clicked':
            user = PlayingUser.objects.filter(user=self.user).first()
            user.isActive = True
            user.save()
            async_to_sync(self.channel_layer.group_send)(
                self.lobby_group_name, {
                    'type': 'lobby_message',
                    'action': 'check'
                }
            )

    def __add_playing_user(self):
        print(PlayingUser.objects.filter(user=self.user).count())
        if PlayingUser.objects.filter(user=self.user).count() == 0:
            PlayingUser(user=self.user).save()

    def __check_game_availability(self):
        if not PlayingUser.objects.filter(isPlaying=True).first():

            all_users = PlayingUser.objects.count()
            active_users = PlayingUser.objects.filter(isActive=True).count()

            if all_users == 4 or active_users == all_users:
                # gra rozpoczyna się automatycznie - event
                print('START GAME')
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

                async_to_sync(self.channel_layer.group_send)(
                    self.lobby_group_name, {
                        'type': 'lobby_message',
                        'action': 'start'
                    }
                )
            elif 2 <= all_users < 4:
                # gracze z tabeli mogą rozpocząć grę (przycisk ROZPOCZNIJ GRĘ jest dostępny) - event
                async_to_sync(self.channel_layer.group_send)(
                    self.lobby_group_name, {
                        'type': 'lobby_message',
                        'action': 'load',
                        'number': all_users
                    }
                )
            else:
                async_to_sync(self.channel_layer.group_send)(
                    self.lobby_group_name, {
                        'type': 'lobby_message',
                        'action': 'load_number',
                        'number': all_users
                    }
                )

    # Receive message from room group
    def lobby_message(self, event):
        print(f"Lobby {event}")

        if event['action'] == 'check':
            self.__check_game_availability()
        elif event['action'] == 'start':
            self.send(text_data=json.dumps({
                'action': event['action']
            }))
        else: # event['action'] == 'load' or:
            self.send(text_data=json.dumps({
                'action': event['action'],
                'number': event['number']
            }))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.lobby_group_name,
            self.channel_name
        )
        self.close()
        # Called when the socket closes


class BoardConsumer(WebsocketConsumer):
    def connect(self):
        # self.board_name = self.scope['url_route']['kwargs']['board_name']
        self.board_group_name = 'board'
        self.user = User.objects.filter(username=self.scope["user"]).first()

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.board_group_name,
            self.channel_name
        )
        self.accept()
        # pokazanie pierwszemu graczowi ze ma grac
        self.next_turn()

    def next_turn(self):
        user = PlayingUser.objects.filter(isPlaying=True).first()
        if user == PlayingUser.objects.filter(user=self.user).first():
            self.send(text_data=json.dumps({
                'action': 'turn'
            }))

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
        action = text_data_json['action']

        if action == 'game_start':
            print("DICE")
            dice = random.randint(1, 6)
            dice = 1
            print(dice)
            user = PlayingUser.objects.filter(isPlaying=True).first()
            print(user)
            user.place = (user.place + dice) % Field.objects.all().count()
            user.save()
            message = {"user": user.id, "field": user.place}
            print(user.place)
            field = Field.objects.filter(id=user.place).first()
            type = FieldType.objects.filter(id=field.field_type_id).first()
            zone = Zone.objects.filter(id=field.zone_id).first()
            print(field)
            print(type)
            print(zone)
            if field.field_type_id == 7:
                self.send(text_data=json.dumps({
                    'action': 'card_buy',
                    'roll' : dice,
                    'buy': field.name,
                    'price': field.price,
                    'zone': zone.name,
                    'house': zone.price_per_house
                }))
            # Messages(type="move", parameter=message).save()
            json_message = json.dumps(message)
            # TODO: Mamy karte -> teraz jaka akcja
        # else:
        elif action == 'buy_card':
            # TU się dzije cos jak kupujemy kartę
            user = PlayingUser.objects.filter(isPlaying=True).first()
            field = Field.objects.filter(id=user.place).first()
            self.send(text_data=json.dumps({
                'action': 'message',
                'message' : 'Congratulation! You bought a card ' + field.name
            }))
            # Finished turn -> send message to update
            self.__send_update()
        elif action =='end_turn':
            self.__send_update()


    # Receive message from room group
    def board_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'action': message
        }))

    # def __end_turn(self):

    def __send_update(self):
        async_to_sync(self.channel_layer.group_send)(
            self.board_group_name, {
                'type': 'board_message',
                'message': 'update'
            }
        )

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
