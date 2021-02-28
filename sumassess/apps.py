from django.apps import AppConfig


class SumassessConfig(AppConfig):
    name = 'sumassess'
    def ready(self):
        import sumassess.signals
