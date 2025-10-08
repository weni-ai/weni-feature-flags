from django.core.cache import cache
import json
from typing import Optional


from weni_feature_flags.integrations.growthbook.clients import GrowthBookClient
from weni_feature_flags.integrations.settings import (
    CACHE_KEY_PREFIX,
    FEATURE_FLAGS_DEFINITIONS_CACHE_TTL,
)
from weni_feature_flags.models import FeatureFlagsDefinitions
from weni_feature_flags.tasks import update_feature_flags_definitions


CACHE_KEY = f"{CACHE_KEY_PREFIX}:definitions"


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
        if cached_data := self._get_definitions_from_cache():
            return cached_data

        definitions_object: Optional[
            FeatureFlagsDefinitions
        ] = FeatureFlagsDefinitions.objects.order_by("created_at").last()

        if definitions_object:
            update_feature_flags_definitions.delay()

            return definitions_object.definitions

        return self.update_definitions()

    def update_definitions(self):
        definitions = self.growthbook_client.get_definitions()

        definitions_object = FeatureFlagsDefinitions.objects.order_by(
            "created_at"
        ).last()

        if not definitions_object:
            definitions_object = FeatureFlagsDefinitions.objects.create(
                definitions=definitions
            )
        else:
            definitions_object.definitions = definitions
            definitions_object.save(update_fields=["definitions"])

        cache.set(
            CACHE_KEY,
            json.dumps(definitions, ensure_ascii=False),
            FEATURE_FLAGS_DEFINITIONS_CACHE_TTL,
        )

        return definitions
