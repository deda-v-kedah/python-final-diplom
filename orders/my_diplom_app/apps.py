from django.apps import AppConfig


class MyDiplomAppConfig(AppConfig):
    name = 'my_diplom_app'

    def ready(self):
        import my_diplom_app.signal
