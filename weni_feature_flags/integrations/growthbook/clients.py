from growthbook import GrowthBook

from weni_feature_flags.settings import get_setting

from weni_feature_flags.models import FeatureFlagsDefinitions


DEFAULT_DEFINITIONS_CACHE_TTL = 300  # 5 minutes


class GrowthBookClient:
    """
    Client to interact with the GrowthBook API.
    """

    def __init__(self):
        self.api_key = get_setting("GROWTHBOOK_CLIENT_KEY", is_required=True)
        self.host = get_setting("GROWTHBOOK_HOST", is_required=True)
        self.definitions_cache_ttl = get_setting(
            "GROWTHBOOK_DEFINITIONS_CACHE_TTL",
            is_required=False,
            default_value=DEFAULT_DEFINITIONS_CACHE_TTL,
        )
