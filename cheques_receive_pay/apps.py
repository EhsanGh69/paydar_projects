from django.apps import AppConfig


class ChequesReceivePayConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cheques_receive_pay'
    verbose_name = 'حسابداری'

    def ready(self):
        return self.import_models()
