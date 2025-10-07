# from growthbook import GrowthBook

from weni_feature_flags.integrations.settings import (
    GROWTHBOOK_CLIENT_KEY,
    GROWTHBOOK_DEFINITIONS_CACHE_TTL,
    GROWTHBOOK_HOST,
)


class GrowthBookClient:
    """
    Client to interact with the GrowthBook API.
    """

    def __init__(self):
        self.api_key = GROWTHBOOK_CLIENT_KEY
        self.host = GROWTHBOOK_HOST
        self.definitions_cache_ttl = GROWTHBOOK_DEFINITIONS_CACHE_TTL
