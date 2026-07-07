from unittest import TestCase
from unittest.mock import Mock, patch

from weni.feature_flags.services import FeatureFlagsService
from weni.feature_flags.tasks import scheduled_update_feature_flags, update_feature_flags

mock_service = Mock(spec=FeatureFlagsService)


class TestUpdateFeatureFlags(TestCase):
    def setUp(self):
        mock_service.reset_mock()

    @patch("weni.feature_flags.services.FeatureFlagsService", return_value=mock_service)
    def test_update_feature_flags(self, mock_feature_flags_svc):
        update_feature_flags()
        mock_service.update_features.assert_called_once_with(force=False)

    @patch("weni.feature_flags.services.FeatureFlagsService", return_value=mock_service)
    def test_update_feature_flags_with_force(self, mock_feature_flags_svc):
        update_feature_flags(force=True)
        mock_service.update_features.assert_called_once_with(force=True)


class TestScheduledUpdateFeatureFlags(TestCase):
    def setUp(self):
        mock_service.reset_mock()

    @patch("weni.feature_flags.services.FeatureFlagsService", return_value=mock_service)
    def test_scheduled_update_always_forces(self, mock_feature_flags_svc):
        scheduled_update_feature_flags()
        mock_service.update_features.assert_called_once_with(force=True)
