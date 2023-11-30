from django.apps import AppConfig


class Config(AppConfig):
    name = "ivo"

    def ready(self):
        from . import api  # noqa
        from . import signals  # noqa
