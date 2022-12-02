from django.urls import path
from .views import MyTokenView, SignoutView, UserView, AddListUsers

urlpatterns = [
    path("signin", MyTokenView.as_view()),
    path("signout", SignoutView.as_view()),
    path("<str:code>", UserView.as_view()),
    path("", AddListUsers.as_view()),
]
