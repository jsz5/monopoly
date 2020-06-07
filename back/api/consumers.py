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
        self.user = self.scope[
            "user"
        ]  # User.objects.filter(username=self.scope["user"]).first()
        self.lobby_group_name = "game"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.lobby_group_name, self.channel_name
        )

        self.__add_playing_user()
        self.__check_game_availability()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(f"RECEIVE {text_data_json['type']}")
        if text_data_json["type"] == "start_clicked":
            user = PlayingUser.objects.filter(user=self.user).first()
            user.isActive = True
            user.save()
            async_to_sync(self.channel_layer.group_send)(
                self.lobby_group_name, {"type": "lobby_message", "action": "check"}
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
                print("START GAME")
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
                    self.lobby_group_name, {"type": "lobby_message", "action": "start"}
                )
            elif 2 <= all_users < 4:
                # gracze z tabeli mogą rozpocząć grę (przycisk ROZPOCZNIJ GRĘ jest dostępny) - event
                async_to_sync(self.channel_layer.group_send)(
                    self.lobby_group_name,
                    {"type": "lobby_message", "action": "load", "number": all_users},
                )
            else:
                async_to_sync(self.channel_layer.group_send)(
                    self.lobby_group_name,
                    {
                        "type": "lobby_message",
                        "action": "load_number",
                        "number": all_users,
                    },
                )

    # Receive message from room group
    def lobby_message(self, event):
        print(f"Lobby {event}")

        if event["action"] == "check":
            self.__check_game_availability()
        elif event["action"] == "start":
            self.send(text_data=json.dumps({"action": event["action"]}))
        else:  # event['action'] == 'load' or:
            self.send(
                text_data=json.dumps(
                    {"action": event["action"], "number": event["number"]}
                )
            )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.lobby_group_name, self.channel_name
        )
        self.close()
        # Called when the socket closes


class BoardConsumer(WebsocketConsumer):
    def connect(self):
        # self.board_name = self.scope['url_route']['kwargs']['board_name']
        self.board_group_name = "board"
        self.user = User.objects.filter(username=self.scope["user"]).first()

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.board_group_name, self.channel_name
        )
        self.accept()

    def next_turn(self):
        user = PlayingUser.objects.filter(isPlaying=True).first()
        if user == PlayingUser.objects.filter(user=self.user).first():
            self.send(text_data=json.dumps({"action": "turn"}))

    def disconnect(self, close_code):
        # Leave board group
        async_to_sync(self.channel_layer.group_discard)(
            self.board_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json["action"]

        if action == "update":
            self.__send_update()
        elif action == "end_turn":
            self.__end_turn()
        elif action == "refresh_transaction":
            self.__update_transaction()

    def update_message(self, event):
        board = event["board"]

        self.send(text_data=json.dumps({"action": "update", "board": board}))

    def turn_message(self, event):
        user = PlayingUser.objects.filter(isPlaying=True).first()

        event['username'] = User.objects.filter(id=user.user_id).first().username
        event['your_turn'] = (user == PlayingUser.objects.filter(user=self.user).first())

        self.send(text_data=json.dumps(event))

    def refresh_transaction(self, event):
        self.send(text_data=json.dumps({"action": event["type"], "board": event["board"]}))

    def __end_turn(self):
        self.__set_order()
        self.__send_turn()
        self.__send_update()

    def __set_order(self):
        playing_user = PlayingUser.objects.filter(isPlaying=True).first()
        next_place = playing_user.place % (PlayingUser.objects.count()) + 1
        print(f"Now should play {next_place}")
        if playing_user.prison:
            if playing_user.prison["queue"] == 0:
                playing_user.prison = None
            else:
                playing_user.prison["checked"] = False
        playing_user.isPlaying = False
        playing_user.save()
        new_playing_user = PlayingUser.objects.get(place=next_place)
        new_playing_user.isPlaying = True
        new_playing_user.dice = False
        new_playing_user.save()

    def __send_turn(self):
        async_to_sync(self.channel_layer.group_send)(
            self.board_group_name, {
                'type': 'turn_message',
                'action': 'turn',
            }
        )

    def __get_board(self):
        d = dict()
        for obj in Field.objects.all():
            d[obj.pk] = {
                "name": obj.name,
                "id": obj.id,
                "type": obj.field_type.name,
                "price": obj.price,
                "zone": obj.zone.pk if obj.zone else None,
                "owner": None,
            }
        for user in PlayingUser.objects.filter(isActive=True):
            print(d[user.field.pk].values())
            if "users" in d[user.field.pk]:
                d[user.field.pk]["users"].append(user.pk)
            else:
                d[user.field.pk]["users"] = [user.pk]

        for asset in Asset.objects.filter(playingUser__isActive=True):
            owner = User.objects.get(playing_users=asset.playingUser.pk)
            d[asset.field.pk]["owner"] = owner.username
            d[asset.field.pk]["isPledged"] = asset.isPledged
            d[asset.field.pk]["houses"] = (
                asset.estateNumber if asset.estateNumber else 0
            )
        return d

    def __update_transaction(self):
        async_to_sync(self.channel_layer.group_send)(
            self.board_group_name, {"type": "refresh_transaction", "board": self.__get_board()}
        )

    def __send_update(self):
        async_to_sync(self.channel_layer.group_send)(
            self.board_group_name, {"type": "update_message", "board": self.__get_board()}
        )
