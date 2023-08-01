from django.urls import path

from .views import (
    ExtractOrders,
    ListCreateOrder,
    ModifyOrder,
    StatusOrderView,
)

urlpatterns = [
    path("extract", ExtractOrders.as_view()),
    path("", ListCreateOrder.as_view()),
    path(
        "<int:order_id>",
        ModifyOrder.as_view(),
        name="order-details",
    ),
    path("<int:order_id>/status", StatusOrderView.as_view()),
]
