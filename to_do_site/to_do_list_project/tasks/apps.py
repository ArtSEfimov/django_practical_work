from django.apps import AppConfig
from to_do_list_project import settings


class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'

    def ready(self):
        settings.IS_EMAIL_SENT = False
