from django.apps import AppConfig


class DrugsAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "drugs_app"

    def ready(self) -> None:
        import drugs_app.signals
