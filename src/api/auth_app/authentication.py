from rest_framework.authentication import TokenAuthentication

from .models import UserToken


class CustomTokenAuthentication(TokenAuthentication):
    model = UserToken
