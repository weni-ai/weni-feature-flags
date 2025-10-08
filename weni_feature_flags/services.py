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

    def _save_definitions_to_cache(self, definitions: dict):
        """
        Save feature flags definitions to cache.
        """
        cache.set(
            CACHE_KEY,
            json.dumps(definitions, ensure_ascii=False),
            FEATURE_FLAGS_DEFINITIONS_CACHE_TTL,
        )

    def _get_definitions_db_object(self) -> Optional[FeatureFlagsDefinitions]:
        """
        Get feature flags definitions from the database.
        """
        return FeatureFlagsDefinitions.objects.order_by("created_at").last()

    def _get_definitions_from_db(self) -> Optional[dict]:
        """
        Get feature flags definitions from the database.
        """
        obj = self._get_definitions_db_object()

        return obj.definitions if obj else None

    def _save_definitions_to_db(
        self, definitions: dict
    ) -> Optional[FeatureFlagsDefinitions]:
        """
        Save feature flags definitions to the database.
        """
        obj = self._get_definitions_db_object()

        if obj:
            obj.definitions = definitions
            obj.save(update_fields=["definitions"])
        else:
            FeatureFlagsDefinitions.objects.create(definitions=definitions)

        return obj

    def get_definitions(self) -> dict:
        """
        Get feature flags definitions.
        """
        if definitions_from_cache := self._get_definitions_from_cache():
            return definitions_from_cache

        definitions_from_db = self._get_definitions_from_db()

        if definitions_from_db:
            update_feature_flags_definitions.delay()

            return definitions_from_db.definitions

        return self.update_definitions()

    def update_definitions(self):
        """
        Update feature flags definitions.
        """
        definitions = self.growthbook_client.get_definitions()

        self._save_definitions_to_db(definitions)
        self._save_definitions_to_cache(definitions)

        return definitions
