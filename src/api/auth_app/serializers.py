from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

User = get_user_model()


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(label="email", write_only=True)

    def create(self, validated_data):
        return validated_data


class PasswordField(serializers.CharField):
    def __init__(self, **kwargs):
        kwargs["write_only"] = True
        kwargs["max_length"] = 150
        kwargs["style"] = {"input_type": "password"}
        kwargs["trim_whitespace"] = False
        super().__init__(**kwargs)


class ResetPasswordSerializer(serializers.Serializer):
    password = PasswordField(label="new password")
    pass_again = PasswordField(label="password again")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = validated_data.pop("user")
        user.set_password(password)
        user.update_login()
        user.save()
        return user

    def validate(self, attrs):
        if attrs["password"] != attrs["pass_again"]:
            raise serializers.ValidationError("passowrds must be same")
        request = self.context["request"]
        path_params = request.resolver_match.kwargs
        user = User.get_user_from_uuid(path_params["uuid"])
        user.check_token_validation(path_params["token"])
        attrs["user"] = user
        return attrs


login_response = {
    "refresh": "string",
    "access": "string",
    "refresh_token_timeout": 20000,
    "access_token_timeout": 3600,
    "user": {
        "username": "string",
        "name": "string",
        "email": "string",
        "is_staff": True,
    },
}


class ChangePasswordSerializer(serializers.Serializer):
    old_password = PasswordField(label="old password")
    new_password = PasswordField(label="new passowrd")

    def create(self, validated_data):
        new_pass = validated_data.get("new_password", "")
        request = self.context.get("request", "")
        request.user.set_password(new_pass)
        request.user.save()
        return request.user

    def validate(self, data):
        request = self.context.get("request", "")
        old_pass = data.get("old_password", "")
        request.user.check_password(old_pass)
        return data


class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = PasswordField()

    class Meta:
        fields = "__all__"

    def create(self, validated_data):
        return validated_data

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            email=email,
            password=password,
        )

        if not user:
            msg = "Unable to log in with provided credentials."
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)

    class Meta:
        fields = "__all__"

    def create(self, validated_data):
        return validated_data
