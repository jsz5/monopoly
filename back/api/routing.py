from django.urls import re_path
from channels.routing import URLRouter
from . import consumers

websockets = URLRouter([
    re_path(r'ws/lobby/$', consumers.LobbyConsumer, name='lobby'),
    re_path(r'ws/lobby$', consumers.LobbyConsumer, name='lobby'),
    re_path(r'ws/game/$', consumers.BoardConsumer)
    # re_path(r'ws/board/(?P<board_name>\w+)/$', consumers.BoardConsumer),
])