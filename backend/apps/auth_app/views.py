from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView,
)
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiExample,
    OpenApiResponse,
)
from drf_spectacular.types import OpenApiTypes
from rest_framework.permissions import AllowAny
from .serializers import (
    LoginSerializer,
    EmailSerializer,
    ResetPasswordSerializer,
    ChangePasswordSerializer,
)
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.views import TokenObtainPairView
from users_app.tasks import send_activation
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView


@extend_schema_view(
    post=extend_schema(
        operation_id="Login",
        tags=["auth"],
        description="takes user credentials (email and password) and returns login data if the credentials is valid",
    )
)
class LoginView(TokenObtainPairView):

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer


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
            "url_name": "reset-password",
        }
        send_activation.delay(data)
        return Response({"messaga": "check your email to reset password"})


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
        return Response({"message": "user passowrd is set successfully"}, status=201)


@extend_schema_view(post=extend_schema(operation_id="refresh", tags=["auth"]))
class RefreshAccess(TokenRefreshView):
    ...


@extend_schema_view(
    post=extend_schema(
        operation_id="logout",
        tags=["auth"],
        description="takes refresh token and blacklists it into blacklist table",
        responses={
            200: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        name="success logout",
                        value={
                            "message": "the refresh token is blacklisted and you connot use it forever"
                        },
                    )
                ],
            )
        },
    )
)
class Logout(TokenBlacklistView):
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return Response(
            data={
                "message": "the refresh token is blacklisted and you connot use it forever"
            }
        )
