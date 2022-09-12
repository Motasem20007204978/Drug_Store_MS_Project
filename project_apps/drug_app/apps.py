from django.apps import AppConfig


class DrugAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "drug_app"

    def ready(self):
        import drug_app.signals
