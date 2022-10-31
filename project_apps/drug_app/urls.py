from django.urls import path
from .views import ListCreateDrugView, OneDrugView

urlpatterns = [
    path("all-drugs/", ListCreateDrugView.as_view(), name="list-create-drug"),
    path("drug-detail/<int:drug_id>/", OneDrugView.as_view(), name="get-update-drug"),
]
