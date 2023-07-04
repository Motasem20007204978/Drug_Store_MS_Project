from django.urls import path

from . import views

app_name = "user"

urlpatterns = [
    path("profile", views.profile, name="profile"),
    path("orders/current", views.current_orders, name="current-orders"),
    path("orders/archived", views.archived_orders, name="arch-orders"),
    path("orders/create", views.create_order, name="create-order"),
    path("users/add", views.add_users, name="add-users"),
    path("drugs/add", views.add_drugs, name='add-drugs'),
]
