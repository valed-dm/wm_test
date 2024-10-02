import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "wm_test.users"
    verbose_name = _("Users")

    def ready(self):
        with contextlib.suppress(ImportError):
            import wm_test.users.signals  # noqa: F401
