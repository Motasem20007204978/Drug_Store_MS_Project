from django.urls import path

from .views import AddListUsers, FileUploadView, UserView

urlpatterns = [
    path("", AddListUsers.as_view()),
    path("upload", FileUploadView.as_view(), name="upload-users-data"),
    path("<str:username>", UserView.as_view()),
]
