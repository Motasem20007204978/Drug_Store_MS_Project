from django.urls import path

from .views import FileUploadView, ListCreateDrugView, OneDrugView

urlpatterns = [
    path("", ListCreateDrugView.as_view(), name="drugs"),
    path("upload", FileUploadView.as_view(), name="upload-drugs-data"),
    path("<int:drug_id>", OneDrugView.as_view(), name="drug-details"),
]
