from django.urls import path
from .consumers import WSyncConsumer
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

application = ProtocolTypeRouter({
	'websocket': AuthMiddlewareStack(
		URLRouter([path('wsync/', WSyncConsumer)])
	),
})
