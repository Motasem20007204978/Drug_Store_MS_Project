from django.urls import path
from .views import (
    ListCreateOrder,
    ModifyOrder,
    ListOrders,
    ExtractOrders,
    StatusOrderView,
)

urlpatterns = [
    path("", ListOrders.as_view(), name="all-orders"),
    path("extract", ExtractOrders.as_view()),
    path("<str:username>", ListCreateOrder.as_view()),
    path("<str:username>/<int:order_id>", ModifyOrder.as_view(), name="order-details"),
    path("<int:order_id>/status", StatusOrderView.as_view()),
]
