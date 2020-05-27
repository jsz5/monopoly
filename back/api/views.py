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

from api.serializers import PlayingUserSerializer, EstateSerializer


class PlayingUserReadyUpdateView(APIView):
    queryset = PlayingUser.objects.all()
    serializer_class = None

    def put(self, request, format=None):
        user = PlayingUser.objects.filter(user=request.user).first()
        user.isActive = True
        user.save()
        if PlayingUser.objects.filter(isActive=True).count() == 4:
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
            # todo: gra rozpoczyna się  - event
            return Response("Gra rozpoczęta.")

        return Response("Gracz jest gotowy do gry.")


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
                self.__add_playing_user(user)
                return Response({"key": token.key})
        return Response("Invalid username or password")

    def __add_playing_user(self, user):
        PlayingUser(user=user).save()
        # todo: dodać jak będą channele
        # if not PlayingUser.objects.filter(isPlaying=True).first():
        #   if PlayingUser.objects.all().count() >= 2:
        #     gracze z tabeli mogą rozpocząć grę (przycisk ROZPOCZNIJ GRĘ jest dostępny) - event
        #   if PlayingUser.objects.all().count() >= 4:
        #     gra rozpoczyna się automatycznie - event


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
        user.place = (user.place + dice) % Field.objects.all().count()
        user.save()
        message = {"user": user.id, "field": user.place}
        Messages(type="move", parameter=message).save()
        return Response({"number": dice})


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
