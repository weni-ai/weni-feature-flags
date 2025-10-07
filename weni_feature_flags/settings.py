from typing import Any

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get_setting(name: str, is_required: bool = False, default_value: Any = None) -> Any:
    """
    Get a setting from the settings module.
    """
    setting = getattr(settings, name, default_value)

    if is_required and not setting:
        raise ImproperlyConfigured(f"Setting {name} is required")

    return setting
