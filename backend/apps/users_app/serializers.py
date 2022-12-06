from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User
from drf_base64.fields import Base64ImageField
from drf_queryfields.mixins import QueryFieldsMixin


class UserSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    picture = Base64ImageField()

    class Meta:
        model = User
        fields = (
            "username",
            "full_name",
            "picture",
            "location",
            "first_name",
            "last_name",
            "date_joined",
            "updated_at",
        )
        read_only_fields = (
            "full_name",
            "date_joined",
            "updated_at",
        )
        extra_kwargs = {
            "first_name": {"write_only": True},
            "last_name": {"write_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        pharmacy_data = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "full_name": self.user.full_name,
            "is_staff": self.user.is_staff,
        }
        context = {
            "access": data["access"],
            "refresh": data["refresh"],
            "pharmacy": pharmacy_data,
        }

        return context
