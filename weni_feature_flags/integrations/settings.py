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


DEFAULT_DEFINITIONS_CACHE_TTL = 300  # 5 minutes

GROWTHBOOK_CLIENT_KEY = get_setting("GROWTHBOOK_CLIENT_KEY", is_required=True)
GROWTHBOOK_HOST = get_setting("GROWTHBOOK_HOST", is_required=True)
GROWTHBOOK_DEFINITIONS_CACHE_TTL = get_setting(
    "GROWTHBOOK_DEFINITIONS_CACHE_TTL",
    is_required=False,
    default_value=DEFAULT_DEFINITIONS_CACHE_TTL,
)
