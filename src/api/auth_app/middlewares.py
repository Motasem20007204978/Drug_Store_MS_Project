from urllib.parse import parse_qs

from channels.middleware import BaseMiddleware
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from .models import UserToken

User = get_user_model()


async def get_user(user_id):
    try:
        return await User.objects.aget(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class WebSocketJWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        parsed_query_string = parse_qs(scope["query_string"])
        key = parsed_query_string.get(b"token")[0].decode("utf-8")

        try:
            user = await User.objects.aget(auth_token__key=key)
            scope["user"] = user
        except UserToken.DoesNotExist:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)
