from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token


class UserToken(Token):
    @property
    def representation(self):
        data = {
            "token": self.key,
            "username": self.user.username,
            "profile_pic": self.user.profile_pic.url,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "is_staff": self.user.is_staff,
        }
        return data

    class Meta(Token.Meta):
        db_table = "tokens_db"
        indexes = [models.Index(fields=["user", "key"], name="user_key_idx")]
