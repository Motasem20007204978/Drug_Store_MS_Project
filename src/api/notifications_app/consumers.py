from asgiref.sync import async_to_sync
from channels.exceptions import DenyConnection
from channels.generic.websocket import JsonWebsocketConsumer

from .tasks import load_related_notifications


class NotificationConsumer(JsonWebsocketConsumer):
    def connect(self):
        if self.scope["user"].is_anonymous:
            raise DenyConnection("Invalid user")

        self.user = self.scope["user"]
        self.group_name = self.user.username

        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name
        )
        super().connect()
        load_related_notifications(self.group_name)

    def disconnect(self, close_code=None):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )
        pass

    def send_notification(self, payload):
        self.send_json(payload)

    def delete_notification(self, event):
        event["action"] = "delete"
        self.send_json(event)
