from django.urls import path
from .views import (
    ListCreateOrder,
    ModifyOrder,
    ListOrders,
    ExtractOrders,
    StatusOrderView,
)

urlpatterns = [
    path("all", ListOrders.as_view(), name="all-orders"),
    path("all/extract", ExtractOrders.as_view()),
    path("<int:order_id>/set-status", StatusOrderView.as_view()),
    path("<str:code>", ListCreateOrder.as_view()),
    path("<str:code>/<int:order_id>", ModifyOrder.as_view(), name="order-details"),
]
