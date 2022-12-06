from django.urls import path
from .views import LoginView, UserView, AddListUsers

urlpatterns = [
    path("", AddListUsers.as_view()),
    path("signin", LoginView.as_view()),
    path("<str:username>", UserView.as_view()),
]
