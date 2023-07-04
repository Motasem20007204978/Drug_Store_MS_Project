from drf_queryfields.mixins import QueryFieldsMixin
from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers

from .models import Notification
from .tasks import mark_as_read

user_representation = {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "username": "string",
    "full_name": "string",
    "picture": "example.com/media/profile_pic/32435223-2532.jpg",
}


class RelatedUser(serializers.RelatedField):
    def to_representation(self, value):
        bostedBy = {
            "id": value.id,
            "username": value.username,
            "full_name": value.full_name,
            "picture": value.profile_pic.url,
        }
        return bostedBy


@extend_schema_serializer(
    exclude_fields=["sender", "receiver"],
    examples=[
        OpenApiExample(
            name="notifications data",
            value={
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "sender": user_representation,
                "receiver": user_representation,
                "created": "2022-12-17T14:39:17.902Z",
                "modified": "2022-12-17T14:39:17.902Z",
                "data": {
                    "additionalProp1": "string",
                    "additionalProp2": "string",
                    "additionalProp3": "string",
                },
                "seen": True,
            },
        )
    ],
)
class NotificationSerialzier(QueryFieldsMixin, serializers.ModelSerializer):

    sender = RelatedUser(read_only=True)
    receiver = RelatedUser(read_only=True)

    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = ("seen", "data", "created", "modified")

    def update(self, instance, validated_data):
        mark_as_read.delay(instance.id)
        return instance
