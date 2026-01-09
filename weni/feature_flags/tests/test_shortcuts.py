import uuid
from unittest import TestCase
from unittest.mock import Mock, patch

from weni.feature_flags.services import FeatureFlagsService
from weni.feature_flags.shortcuts import (
    is_feature_active,
    is_feature_active_for_attributes,
)

mock_service = Mock(spec=FeatureFlagsService)


@patch("weni.feature_flags.shortcuts.FeatureFlagsService", return_value=mock_service)
class TestShortcuts(TestCase):
    def setUp(self):
        self.mock_service = Mock(spec=FeatureFlagsService)

    def test_is_feature_active_for_attributes_when_the_feature_is_active(
        self, mock_feature_flags_svc
    ):
        mock_service.evaluate_feature_flag_by_attributes.return_value = True

        self.assertTrue(
            is_feature_active_for_attributes(
                "test", {"projectUUID": uuid.uuid4(), "userEmail": "test@test.com"}
            )
        )

    def test_is_feature_active_for_attributes_when_the_feature_is_not_active(
        self, mock_feature_flags_svc
    ):
        mock_service.evaluate_feature_flag_by_attributes.return_value = False

        self.assertFalse(
            is_feature_active_for_attributes(
                "test", {"projectUUID": uuid.uuid4(), "userEmail": "test@test.com"}
            )
        )

    def test_is_feature_active_when_the_feature_is_active(self, mock_feature_flags_svc):
        mock_service.evaluate_feature_flag_by_attributes.return_value = True

        self.assertTrue(is_feature_active("test", "test@test.com", uuid.uuid4()))

    def test_is_feature_active_when_the_feature_is_not_active(
        self, mock_feature_flags_svc
    ):
        mock_service.evaluate_feature_flag_by_attributes.return_value = False

        self.assertFalse(is_feature_active("test", "test@test.com", uuid.uuid4()))

    def test_is_feature_active_when_the_key_is_not_provided(self, mock_feature_flags_svc):
        with self.assertRaises(ValueError) as context:
            is_feature_active(None, "test@test.com", uuid.uuid4())
        self.assertEqual(str(context.exception), "key must be a non-empty string")

    def test_is_feature_active_with_project_uuid_and_without_user_email(self, mock_feature_flags_svc):
        mock_service.evaluate_feature_flag_by_attributes.return_value = True
        self.assertTrue(is_feature_active("test", None, uuid.uuid4()))

    def test_is_feature_active_with_user_email_and_without_project_uuid(self, mock_feature_flags_svc):
        mock_service.evaluate_feature_flag_by_attributes.return_value = True
        self.assertTrue(is_feature_active("test", "test@test.com", None))

    def test_is_feature_active_with_invalid_project_uuid(self, mock_feature_flags_svc):
        with self.assertRaises(ValueError):
            is_feature_active("test", "test@test.com", "invalid-uuid")

    def test_is_feature_active_with_invalid_user_email(self, mock_feature_flags_svc):
        with self.assertRaises(ValueError):
            is_feature_active("test", "invalid-email", uuid.uuid4())

    def test_is_feature_active_with_no_project_uuid_and_no_user_email(self, mock_feature_flags_svc):
        with self.assertRaises(ValueError) as context:
            is_feature_active("test", None, None)
        self.assertEqual(str(context.exception), "at least one of project_uuid or user_email must be provided")
