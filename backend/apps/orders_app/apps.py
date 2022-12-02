from django.apps import AppConfig


class OrderappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "orderapp"

    def ready(self) -> None:
        import orderapp.signals
