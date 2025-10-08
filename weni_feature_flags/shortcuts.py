from weni_feature_flags.services import FeatureFlagsService


def is_feature_active(key: str, attributes: dict) -> bool:
    """
    Check if a feature is active by its key and attributes.
    """
    features_service = FeatureFlagsService()

    return features_service.evaluate_feature_flag_by_attributes(
        key=key,
        attributes=attributes,
    )
