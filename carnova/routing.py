from django.urls import path
from chat.consumers import *

websocket_urlpatterns = [
    path("ws/chat/<int:sender_id>/<int:receiver_id>/", ChatConsumer.as_asgi()),
    path("ws/online/<int:user_id>/", OnlineStatusConsumer.as_asgi()),
    path("ws/notification/", NotificationConsumer.as_asgi()),
]
