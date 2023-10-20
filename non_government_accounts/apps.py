from django.apps import AppConfig


class NonGovernmentAccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'non_government_accounts'
    verbose_name = "طرف‌ حساب غیردولتی"

    def ready(self):
        return self.import_models()
