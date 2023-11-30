from django.apps import AppConfig


class Config(AppConfig):
    name = "other"

    def ready(self):
        from . import api
