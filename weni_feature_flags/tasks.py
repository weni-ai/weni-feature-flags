from celery import shared_task


@shared_task
def update_feature_flags_definitions():
    """
    Update feature flags definitions.
    """
    from weni_feature_flags.services import FeatureFlagsService

    FeatureFlagsService().update_definitions()
