from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
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
    path("api/admin/", admin.site.urls),
    path(
        "api/apps/",
        include(
            [
                path("users/", include("users_app.urls")),
                path("drugs/", include("drugs_app.urls")),
                path("orders/", include("orders_app.urls")),
                path("api-auth/", include("rest_framework.urls")),
            ]
        ),
    ),
    path("api/", include("django_prometheus.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
