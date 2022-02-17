from django.apps import AppConfig
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model


class RootConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'root'

    def ready(self):
        from root import signals
        User = get_user_model()
        post_save.connect(signals.add_group_for_user_signal, sender=User)
