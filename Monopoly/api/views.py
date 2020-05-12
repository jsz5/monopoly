import json

from rest_framework.response import Response
from rest_framework.generics import (
    GenericAPIView,
    CreateAPIView

)
from rest_framework.views import APIView
from django.contrib import auth
from rest_framework.authtoken.models import Token
from api.models import PlayingUser, FieldType
from rest_auth.serializers import LoginSerializer
import random


class Test(GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response("test")


class PlayingUserReadyUpdateView(APIView):
    queryset = PlayingUser.objects.all()

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
                playing_user.field=start_field
                playing_user.budget=15000
                playing_user.save()
            # todo: gra rozpoczyna się  - event
            return Response("Gra rozpoczęta.")

        return Response("Gracz jest gotowy do gry.")


class Login(CreateAPIView):
    permission_classes = []
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        validated_data = self.serializer_class(json.loads(request.body)).data
        username = validated_data['username']
        password = validated_data['password']
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
