from django.urls import path
from .views import ListCreateDrugView, OneDrugView

urlpatterns = [
    path("create-drug/", ListCreateDrugView.as_view(), name="create-drug"),
    path("list-drugs/", ListCreateDrugView.as_view(), name="list-drugs"),
    path("drug-detail/<int:drug_id>/", OneDrugView.as_view(), name="get-drug-details"),
    path("update-drug/<int:drug_id>/", OneDrugView.as_view(), name="update-drug"),
]
