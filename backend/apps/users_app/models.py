from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from uuid import uuid4
import os
from django.utils.deconstruct import deconstructible
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import smart_bytes
from rest_framework.exceptions import ValidationError

# Create your models here.


@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split(".")[-1]
        filename = "{}.{}".format(uuid4().hex, ext)
        print(self.path)
        return os.path.join(self.path, filename)


class User(AbstractUser):
    id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    email = models.EmailField(
        unique=True,
        verbose_name="email address",
    )
    picture = models.ImageField(
        upload_to=PathAndRename("profile_pic/"),
        blank=True,
        null=True,
        verbose_name="profile picture",
        default="default-image.jpg",
    )
    location = models.CharField(max_length=200, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", "first_name", "last_name")

    def __str__(self):
        return self.username

    @property
    def full_name(self) -> str:
        return super().get_full_name()

    def check_password(self, raw_password: str) -> bool:
        if not super().check_password(raw_password):
            raise ValidationError("user password is incorrect")
        return True

    def check_email_activation(self):
        if not self.is_active:
            raise ValidationError(
                _(
                    "user is inactive (cannot be signed in)"
                    " please check your email and active"
                )
            )

    def generate_uuid(self):
        uidb64 = urlsafe_base64_encode(smart_bytes(self.id))
        return uidb64

    def generate_token(self):
        token = default_token_generator.make_token(self)
        return token

    def check_token(self, token):
        if not default_token_generator.check_token(self, token):
            return False
        return True

    def activate(self):
        self.is_active = True
        self.save()

    class Meta(AbstractUser.Meta):
        ordering = ["-date_joined"]
        db_table = "users_db"
