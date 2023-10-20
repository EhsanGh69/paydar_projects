from django.apps import AppConfig


class GovernmentAccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'government_accounts'
    verbose_name = 'طرف حساب دولتی'

    def ready(self):
        return self.import_models()