import logging

from celery import shared_task


logger = logging.getLogger(__name__)


@shared_task
def update_feature_flags(force: bool = False):
    """
    Update feature flags definitions.
    """
    from weni.feature_flags.services import FeatureFlagsService

    logger.info("[update_feature_flags] Starting feature flags update")
    FeatureFlagsService().update_features(force=force)
    logger.info("[update_feature_flags] Feature flags update completed")


@shared_task
def scheduled_update_feature_flags():
    """
    Periodically update feature flags, bypassing the cooldown.
    Intended to be registered as a periodic task via django-celery-beat
    when FEATURE_FLAGS_USE_SCHEDULED_UPDATES is enabled.
    """
    from weni.feature_flags.services import FeatureFlagsService
    logger.info("[scheduled_update_feature_flags] Starting feature flags update")

    FeatureFlagsService().update_features(force=True)
    logger.info("[scheduled_update_feature_flags] Feature flags update completed")
