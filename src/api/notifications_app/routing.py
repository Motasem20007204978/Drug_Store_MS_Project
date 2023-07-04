from django.urls import path

from .consumers import NotificationConsumer

notifs_urlpatterns = [
    path(
        "api/notifs/me",
        NotificationConsumer.as_asgi(),
        name="websocket-notif",
    )
]
