from django.apps import AppConfig


class WarehousingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'warehousing'
    verbose_name = 'انبارداری'

    def ready(self):
        return self.import_models()
