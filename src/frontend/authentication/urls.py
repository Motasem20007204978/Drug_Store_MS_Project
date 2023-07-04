from django.urls import path

from . import views

app_name = "auth"

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login, name="login"),
    path("password/reset", views.reset_password, name="reset_pass"),
    path("password/set", views.set_password, name="set_pass"),
    path("pyscript", views.pyscritp, name='pyscript'),
]
