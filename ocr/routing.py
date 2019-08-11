from django.conf.urls import url

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from home.consumers import ImageConsumer, InfoConsumer
import json
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ocr.settings')
django.setup()

websocket_urlpatterns = [
    url('message/', ImageConsumer),
    url('info/', InfoConsumer),
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
    	URLRouter(
            websocket_urlpatterns
    	)
    )
})