import json

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView
from rest_framework import status
from rest_framework.views import APIView
from django.contrib import auth
from rest_framework.authtoken.models import Token
from api.models import PlayingUser, FieldType, Field, Messages, Asset, Estate
from rest_auth.serializers import LoginSerializer
from rest_auth.views import LogoutView
import random

from django.http import HttpResponse

from api.serializers import PlayingUserSerializer, EstateSerializer

from django.views.generic import CreateView, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class PlayingUserReadyUpdateView(APIView):
    queryset = PlayingUser.objects.all()
    serializer_class = None

    def put(self, request, format=None):
        user = PlayingUser.objects.get(user=request.user)
        user.isActive = True
        user.save()
        all_users = PlayingUser.objects.count()
        active_users = PlayingUser.objects.filter(isActive=True).count()
        if active_users == 4 or active_users == all_users:
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
            return Response({"show_board": True, "message": "Gra rozpoczęta."})

        return Response({"show_board": False, "message": "Gracz jest gotowy do gry."})


class Login(CreateAPIView):
    permission_classes = []
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        validated_data = self.serializer_class(request.data).data
        username = validated_data["username"]
        password = validated_data["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                start_game_button = self.__add_playing_user(user)
                number_of_users = PlayingUser.objects.count()
                return Response(
                    {"key": token.key, "start_game_button": start_game_button, "number_of_users": number_of_users}
                )
        return Response("Invalid username or password", status=401)

    def __add_playing_user(self, user):
        if PlayingUser.objects.filter(user=user).count() == 0:
            PlayingUser(user=user).save()
        if not PlayingUser.objects.filter(isPlaying=True).first():
            if PlayingUser.objects.all().count() >= 2:
                return True  # gracze z tabeli mogą rozpocząć grę (przycisk ROZPOCZNIJ GRĘ jest dostępny) - event
        return False


class Logout(LogoutView):
    def post(self, request, *args, **kwargs):
        user = request.user
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            PlayingUser.objects.filter(user_id=user.id).delete()
        return response


class PlayingUserListView(ListAPIView):
    serializer_class = PlayingUserSerializer
    queryset = PlayingUser.objects.all()


class DiceRollView(ListAPIView):
    def get(self, request, *args, **kwargs):
        dice = random.randint(1, 6)
        user = PlayingUser.objects.filter(isPlaying=True).first()
        print(user)
        user.place = (user.place + dice) % Field.objects.all().count()
        user.save()
        message = {"user": user.id, "field": user.place}
        Messages(type="move", parameter=message).save()
        return Response({"number": dice})

class LobbyView(TemplateView):
    template_name = 'lobby.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

# class GameView(TemplateView):
#     template_name = 'game.html'
#
#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # kwargs['game_id']
#         self.game = Game.get_by_id(1)  # kwargs['board_name']
#
#         print(kwargs['board_name'])
#         print(self.game)
#         # context['board_name'] = Article.objects.all()[:5]
#         # get the game by the id
#         # self.game = Game.get_by_id(kwargs['game_id'])
#         # user = get_user(request)
#
#         return super().dispatch(*args, **kwargs)
#
#     def __add_playing_user(self, user):
#         PlayingUser(user=user).save()

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer


class GameView(TemplateView):
    template_name = 'game.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        print(request)
        d = {}
        for obj in Field.objects.all():
            d[obj.pk] = {
                "name": obj.name,
                "type": obj.field_type.name,
                "price": obj.price,
                "zone": obj.zone.pk if obj.zone else None,
                "owner": None,
            }
        for user in PlayingUser.objects.filter(isPlaying=True):
            if "users" in d[user.field.pk]:
                d[user.field.pk]["users"].append(user.pk)
            else:
                d[user.field.pk]["users"] = [user.pk]

        for asset in Asset.objects.filter(playingUser__isPlaying=True):
            d[asset.field.pk]["owner"] = asset.playingUser.pk
            d[asset.field.pk]["isPledged"] = asset.isPledged
            d[asset.field.pk]["houses"] = (
                asset.estateNumber if asset.estateNumber else 0
            )

        return HttpResponse(d)

class BoardView(ListAPIView):
    def get(self, request, *args, **kwargs):
        d = {}
        for obj in Field.objects.all():
            d[obj.pk] = {
                "name": obj.name,
                "type": obj.field_type.name,
                "price": obj.price,
                "zone": obj.zone.pk if obj.zone else None,
                "owner": None,
            }
        for user in PlayingUser.objects.filter(isPlaying=True):
            if "users" in d[user.field.pk]:
                d[user.field.pk]["users"].append(user.pk)
            else:
                d[user.field.pk]["users"] = [user.pk]

        for asset in Asset.objects.filter(playingUser__isPlaying=True):
            d[asset.field.pk]["owner"] = asset.playingUser.pk
            d[asset.field.pk]["isPledged"] = asset.isPledged
            d[asset.field.pk]["houses"] = (
                asset.estateNumber if asset.estateNumber else 0
            )

        return Response(d)


class FieldView(ListAPIView):
    def get(self, request, *args, **kwargs):

        try:
            estate = Estate.objects.get(field=self.kwargs["pk"])
        except Estate.DoesNotExist:
            return Response("")
        d = EstateSerializer(estate).data

        d["id"] = estate.field.pk
        d["name"] = estate.field.name
        d["type"] = estate.field.field_type.name
        d["price"] = estate.field.price
        d["zone"] = estate.field.zone.pk if estate.field.zone else None
        d["owner"] = None

        for user in PlayingUser.objects.filter(isPlaying=True, field=estate.field):
            if "users" in d[user.field.pk]:
                d[user.field.pk]["users"].append(user.pk)
            else:
                d[user.field.pk]["users"] = [user.pk]

        for asset in Asset.objects.filter(playingUser__isPlaying=True):
            d["owner"] = asset.playingUser.pk
            d["isPledged"] = asset.isPledged
            d["houses"] = asset.estateNumber if asset.estateNumber else 0

        return Response(d)
