from django.urls import path

from . import views

urlpatterns = [
    path(
        "password/forgot",
        views.ForgetPassowrd.as_view(),
        name="forget-password",
    ),
    path(
        "password/<str:uuid>/<str:token>/reset",
        views.ResetPassword.as_view(),
        name="reset-password",
    ),
    path("login", views.AuthenticateView.as_view(), name="signin-user"),
    path(
        "password/change",
        views.ChangePasswordView.as_view(),
        name="change-password",
    ),
    path("logout", views.LogoutView.as_view(), name="logout"),
]
