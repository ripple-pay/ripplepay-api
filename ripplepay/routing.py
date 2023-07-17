from django.urls import re_path
from apps.transactions import consumers

websocket_urlpatterns = [
    re_path(r"ws/transactions", consumers.MyConsumer.as_asgi()),
]

    