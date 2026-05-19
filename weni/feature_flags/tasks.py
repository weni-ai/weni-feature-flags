from celery import shared_task


@shared_task
def update_feature_flags(force: bool = False):
    """
    Update feature flags definitions.
    """
    from weni.feature_flags.services import FeatureFlagsService

    FeatureFlagsService().update_features(force=force)


@shared_task
def scheduled_update_feature_flags():
    """
    Periodically update feature flags, bypassing the cooldown.
    Intended to be registered as a periodic task via django-celery-beat
    when USE_SCHEDULED_UPDATES is enabled.
    """
    from weni.feature_flags.services import FeatureFlagsService

    FeatureFlagsService().update_features(force=True)
