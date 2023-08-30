from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from users_app.tasks import send_activation

from .models import UserToken
from .serializers import (
    AuthSerializer,
    ChangePasswordSerializer,
    EmailSerializer,
    ResetPasswordSerializer,
    TokenSerializer,
)

User = get_user_model()


@extend_schema_view(
    post=extend_schema(
        operation_id="forget password",
        tags=["auth"],
        description="takes user's email and return a message enshure that is an activation link is sent to your email inbox to reset password",
        responses={
            200: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        name="forgetting password response",
                        value={
                            "message": "check email reset password link",
                        },
                    )
                ],
            )
        },
    )
)
class ForgetPassowrd(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = EmailSerializer

    def post(self, request):
        super().post(request)
        data = {
            "email": request.data["email"],
            "url_name": "auth:set_pass",
        }
        send_activation.delay(data)
        return Response({"message": "check your email to reset password"})


@extend_schema_view(
    post=extend_schema(
        operation_id="reset password",
        tags=["auth"],
        description="takes uuid and token from sent email as a parameters and check if the parameters is valid, then it takes new password to be reset to the users' account",
        responses={
            200: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        name="resetting password response",
                        value={
                            "message": "new password is set successfully",
                        },
                    )
                ],
            )
        },
    )
)
class ResetPassword(CreateAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return Response({"success": "user password is reset successfully"})


@extend_schema_view(
    post=extend_schema(
        operation_id="change password",
        tags=["auth"],
        description="takes the old password to check if it is correct for the curren person, and then reset the old with new password",
        responses={
            201: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        name="change password",
                        value={
                            "message": "password changed",
                        },
                    )
                ],
            ),
        },
    )
)
class ChangePasswordView(CreateAPIView):

    serializer_class = ChangePasswordSerializer

    def post(self, request):
        super().post(request)
        return Response(
            {"message": "user password is set successfully"}, status=201
        )


@extend_schema_view(
    post=extend_schema(
        operation_id="email authentication",
        description="takes the email and password to check if it is correct,"
        " and response user data with authentication data",
        responses={
            201: OpenApiResponse(
                response=dict,
                examples=[
                    OpenApiExample(
                        name="auth data",
                        value={
                            "token": "random string",
                            "username": "Ahmed",
                            "profile_pic": "example.com/media/image.jpg",
                            "first_name": "Name",
                            "last_name": "Last",
                            "is_staff": True,
                        },
                    )
                ],
            ),
        },
    )
)
class AuthenticateView(CreateAPIView):
    serializer_class = AuthSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def get_object(self):
        email = self.request.data.get("email")
        user = get_object_or_404(self.get_queryset(), email=email)
        return user

    def get_token(self, user):
        token = UserToken.objects.get_or_create(user=user)
        return token[0]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        user = self.get_object()
        token = self.get_token(user)
        return Response(data={"data": token.representation})


@extend_schema_view(
    post=extend_schema(
        operation_id="logout",
        description="takes user authentication token and delete it"
        " to logout the system",
        responses={
            200: OpenApiResponse(
                response=dict,
                examples=[
                    OpenApiExample(
                        name="logout the system",
                        value={
                            "message": "you logged out the system",
                        },
                    ),
                ],
            )
        },
    ),
)
class LogoutView(CreateAPIView):
    serializer_class = TokenSerializer
    queryset = UserToken.objects.all()

    def get_object(self):
        key = self.request.data.get("token")
        token = get_object_or_404(
            self.get_queryset(),
            user=self.request.user,
            key=key,
        )
        return token

    def perform_delete(self, token):
        token.delete()

    def post(self, request, *args, **kwargs):
        token = self.get_object()
        self.perform_delete(token)
        return Response(data={"message": "you are logged out the system"})
