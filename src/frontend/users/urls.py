from django.urls import path

from . import views

app_name = "user"

urlpatterns = [
    path("profile", views.profile, name="profile"),
    path("orders/current", views.current_orders, name="current-orders"),
    path("orders/archived", views.archived_orders, name="arch-orders"),
    path("orders/create", views.create_order, name="create-order"),
    path("users", views.add_users, name="users-page"),
    path("drugs", views.add_drugs, name="drugs-page"),
]
