import os
from uuid import uuid4

from django.contrib.auth.models import AbstractUser, update_last_login
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils.deconstruct import deconstructible
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

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


class NameValidator(RegexValidator):
    regex = r"^\w+$"
    message = (
        "enter name begins with capital letter and A-Z, a-z or _"
        " between 5 and 50 characters"
    )
    flags = 0


name_validator = NameValidator()


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4)
    username = models.CharField(
        max_length=50, unique=True, validators=[name_validator]
    )
    email = models.EmailField("email address", unique=True)
    location = models.CharField(max_length=50)
    profile_pic = models.ImageField(
        upload_to=PathAndRename("profile_pic/"),
        blank=True,
        verbose_name="profile picture",
        default="default-image.jpg",
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="updating date"
    )

    REQUIRED_FIELDS = ["username", "first_name", "last_name"]
    USERNAME_FIELD = "email"

    @property
    def full_name(self) -> str:
        return self.get_full_name()

    @staticmethod
    def get_user_from_uuid(uuid):
        uid = urlsafe_base64_decode(uuid).decode()
        user = get_object_or_404(User, id=uid)
        return user

    def check_password(self, raw_password: str) -> bool:
        if not super().check_password(raw_password):
            raise ValidationError("user password is incorrect")
        return True

    def generate_uuid(self):
        uidb64 = urlsafe_base64_encode(smart_bytes(self.id))
        return uidb64

    def generate_token(self):
        token = default_token_generator.make_token(self)
        return token

    def check_token_validation(self, token):
        if not default_token_generator.check_token(self, token):
            raise ValidationError("token is invalid or expired")

    def update_login(self):
        update_last_login(User, user=self)

    class Meta:
        db_table = "users_db"
        ordering = ["-date_joined"]
