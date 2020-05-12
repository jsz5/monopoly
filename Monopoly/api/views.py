import json

from rest_framework.response import Response
from rest_framework.generics import (
    GenericAPIView,
    CreateAPIView

)
from rest_framework.views import APIView
from django.contrib import auth
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.authtoken.models import Token
from api.models import PlayingUser
from rest_auth.serializers import LoginSerializer


class Test(GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response("test")


class PlayingUserReadyUpdateView(APIView):
    queryset = PlayingUser.objects.all()

    def put(self, request, format=None):
        request.user.isActive = True
        print(request.user)
        return Response(request.user.id)


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
