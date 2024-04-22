from time import sleep

from django.apps import AppConfig
from main.management.commands.runapscheduler import start


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    # def ready(self):
    #
    #     sleep(10)
    #     start()
