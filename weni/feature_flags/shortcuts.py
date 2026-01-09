from typing import Optional
from uuid import UUID

from weni.feature_flags.services import FeatureFlagsService
from weni.feature_flags.validators import is_email_valid


def is_feature_active_for_attributes(
    key: str, attributes: dict, should_convert_uuids_to_strings: bool = True
) -> bool:
    """
    Check if a feature is active by its key and attributes.
    """
    features_service = FeatureFlagsService()

    return features_service.evaluate_feature_flag_by_attributes(
        key=key,
        attributes=attributes,
        should_convert_uuids_to_strings=should_convert_uuids_to_strings,
    )


def is_feature_active(key: str, user_email: Optional[str], project_uuid: Optional[str]) -> bool:
    """
    Check if a feature is active by user email and/or project UUID.
    """
    if not key:
        raise ValueError("key must be a non-empty string")

    attributes = {}

    if project_uuid:
        if not isinstance(project_uuid, UUID):
            try:
                UUID(project_uuid)
            except ValueError:
                raise ValueError("project_uuid must be a valid UUID")

        attributes["projectUUID"] = str(project_uuid)

    if user_email:
        if not is_email_valid(user_email):
            raise ValueError("user_email must be a valid email")

        attributes["userEmail"] = user_email

    if not attributes:
        raise ValueError("at least one of project_uuid or user_email must be provided")

    return is_feature_active_for_attributes(
        key,
        attributes,
    )
