from django.urls import path
from .views import ListCreateDrugView, OneDrugView

urlpatterns = [
    path("", ListCreateDrugView.as_view(), name="drugs"),
    path("<int:drug_id>", OneDrugView.as_view(), name="drug-details"),
]
