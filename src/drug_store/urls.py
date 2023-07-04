from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "api/swagger-ui/",
        SpectacularSwaggerView.as_view(),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(),
        name="redoc",
    ),
    path("api/users/", include("users_app.urls")),
    path("api/auth/", include("auth_app.urls")),
    path("api/drugs/", include("drugs_app.urls")),
    path("api/orders/", include("orders_app.urls")),
    path("api/notifications/", include("notifications_app.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("api/prometheus/", include("django_prometheus.urls")),
    path("", include("authentication.urls")),
    path("", include("users.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
