from channels.routing import ProtocolTypeRouter, URLRouter
from Monopoly.token_auth import TokenAuthMiddleware
from Monopoly.token_auth import TokenAuthMiddlewareStack
from django.urls import re_path
from api.consumers import LobbyConsumer, BoardConsumer
from api.routing import websockets


application = ProtocolTypeRouter({
    "websocket": TokenAuthMiddlewareStack(
            websockets
    ),
})