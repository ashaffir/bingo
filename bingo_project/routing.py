# from channels.routing import ProtocolTypeRouter

# application = ProtocolTypeRouter({
#     # Empty for now (http->django views is added by default)
# })

from django.urls import path, re_path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from game import consumers as game_consumers

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter([
            re_path(r'ws/game/(?P<game_room>\w+)/$', game_consumers.GameConsumer),
            # re_path(r'ws/game/', game_consumers.GameConsumer),
            # re_path(r'ws/players/', orders_consumers.OrderConsumer),
        ])
    ),
})