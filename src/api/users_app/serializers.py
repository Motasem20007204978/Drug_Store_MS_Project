from django.utils.crypto import get_random_string
from drf_base64.fields import Base64ImageField
from drf_queryfields.mixins import QueryFieldsMixin
from rest_framework import serializers

from .models import User
from .tasks import send_password


class UserSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    profile_pic = Base64ImageField(required=False)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "profile_pic",
            "location",
            "date_joined",
            "updated_at",
        )
        read_only_fields = (
            "date_joined",
            "updated_at",
        )

    def send_user_password(self, email, password):
        send_password.delay(email, password)

    def create(self, validated_data):
        user = self.Meta.model(**validated_data)
        password = get_random_string(10)
        user.set_password(password)
        user.save()
        self.send_user_password(user.email, password)
        return user
