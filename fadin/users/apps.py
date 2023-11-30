from django.apps import AppConfig


class Config(AppConfig):
    name = "users"

    def ready(self) -> None:
        import users.api
