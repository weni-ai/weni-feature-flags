from uuid import UUID
from weni_feature_flags.services import FeatureFlagsService


def is_feature_active_for_attributes(key: str, attributes: dict) -> bool:
    """
    Check if a feature is active by its key and attributes.
    """
    features_service = FeatureFlagsService()

    return features_service.evaluate_feature_flag_by_attributes(
        key=key,
        attributes=attributes,
    )


def is_feature_active(key: str, user_email: str, project_uuid: UUID) -> bool:
    """
    Check if a feature is active by user email and project uuid.
    """

    if not isinstance(project_uuid, UUID):
        raise ValueError("project_uuid must be a valid UUID")

    if not isinstance(user_email, str):
        raise ValueError("user_email must be a valid email")

    return is_feature_active_for_attributes(
        key,
        {
            "userEmail": user_email,
            "projectUUID": project_uuid,
        },
    )
