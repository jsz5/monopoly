from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
# import game.routing
import api.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            api.routing.websocket_urlpatterns
            # api.routing.websocket_urlpatterns
        )
    ),
})

# from channels.routing import route, route_class
# from channels.staticfiles import StaticFilesConsumer
 
# routes defined for channel calls
# this is similar to the Django urls, but specifically for Channels
# channel_routing = []