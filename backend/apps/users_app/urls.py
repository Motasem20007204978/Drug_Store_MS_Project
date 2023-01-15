from django.urls import path
from .views import LoginView, UserView, AddListUsers, FileUploadView

urlpatterns = [
    path("", AddListUsers.as_view()),
    path("upload", FileUploadView.as_view(), name="upload-users-data"),
    path("signin", LoginView.as_view()),
    path("<str:username>", UserView.as_view()),
]
