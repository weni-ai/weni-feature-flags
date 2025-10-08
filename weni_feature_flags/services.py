from django.core.cache import cache
import json


from weni_feature_flags.integrations.growthbook.clients import GrowthBookClient
from weni_feature_flags.integrations.settings import CACHE_KEY_PREFIX


CACHE_KEY = f"{CACHE_KEY_PREFIX}_definitions"


class FeatureFlagsService:
    def __init__(self, growthbook_client: GrowthBookClient = GrowthBookClient()):
        self.growthbook_client = growthbook_client

    def _get_definitions_from_cache(self) -> dict:
        """
        Get feature flags definitions from cache.
        """

        data = cache.get(CACHE_KEY)

        if not data:
            return

        if not isinstance(data, dict):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                return

        return data

    def get_definitions(self) -> dict:
        """
        Get feature flags definitions.
        """

        return self.growthbook_client.get_definitions()

    def update_definitions(self):
        pass