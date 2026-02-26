from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        """
        Import signals when the app is ready.
        This wires up the post_save listener for new user signups.
        """
        import core.signals  # noqa: F401