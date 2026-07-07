import logging

from django.apps import AppConfig

PERIODIC_TASK_NAME = "weni-feature-flags-scheduled-update"

logger = logging.getLogger(__name__)


class WeniFeatureFlagsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "weni.feature_flags"
    label = "weni_feature_flags"

    def ready(self):
        from weni.feature_flags.settings import FEATURE_FLAGS_USE_SCHEDULED_UPDATES

        if not FEATURE_FLAGS_USE_SCHEDULED_UPDATES:
            return

        self._setup_periodic_task()

    def _setup_periodic_task(self):
        from celery import current_app

        from weni.feature_flags.settings import (
            FEATURE_FLAGS_SCHEDULED_UPDATE_INTERVAL,
            FEATURES_CACHE_TTL,
        )

        if FEATURE_FLAGS_SCHEDULED_UPDATE_INTERVAL >= FEATURES_CACHE_TTL:
            logger.warning(
                "FEATURE_FLAGS_SCHEDULED_UPDATE_INTERVAL (%s s) is >= "
                "FEATURES_CACHE_TTL (%s s). Feature flags may become stale "
                "between scheduled updates.",
                FEATURE_FLAGS_SCHEDULED_UPDATE_INTERVAL,
                FEATURES_CACHE_TTL,
            )

        beat_schedule = getattr(current_app.conf, "beat_schedule", None) or {}
        beat_schedule[PERIODIC_TASK_NAME] = {
            "task": "weni.feature_flags.tasks.scheduled_update_feature_flags",
            "schedule": FEATURE_FLAGS_SCHEDULED_UPDATE_INTERVAL,
        }
        current_app.conf.beat_schedule = beat_schedule
