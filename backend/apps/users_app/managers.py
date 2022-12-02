from django.contrib.auth.models import UserManager
from django.utils.translation import gettext as _


class CustomUserManager(UserManager):
    """
    Custom user model manager where code is the unique identifier
    for authentication instead of usernames.
    """

    def create_superuser(self, **fields):
        fields.setdefault("is_active", True)
        user = super().create_superuser(**fields)
        return user
