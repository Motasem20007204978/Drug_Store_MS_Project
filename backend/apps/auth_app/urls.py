from django.urls import path
from .views import *


urlpatterns = [
    path("password/forgot", ForgetPassowrd.as_view(), name="forget-password"),
    path(
        "password/<str:uuid>/<str:token>/reset",
        ResetPassword.as_view(),
        name="reset-password",
    ),
    path("login", LoginView.as_view(), name="signin-user"),
    path("token/refresh", RefreshAccess.as_view(), name="refresh-access"),
    path("password/change", ChangePasswordView.as_view(), name="change-password"),
    path("logout", Logout.as_view(), name="logout"),
]
