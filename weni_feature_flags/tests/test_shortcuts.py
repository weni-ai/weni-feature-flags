from unittest import TestCase
from unittest.mock import Mock, patch

from weni_feature_flags.services import FeatureFlagsService
from weni_feature_flags.shortcuts import (
    is_feature_active,
    is_feature_active_for_attributes,
)


class TestShortcuts(TestCase):
    def setUp(self):
        self.mock_service = Mock(spec=FeatureFlagsService)

    @patch("weni_feature_flags.shortcuts.FeatureFlagsService")
    def test_is_feature_active_for_attributes_when_the_feature_is_active(
        self, mock_feature_flags_svc
    ):
        self.mock_service.evaluate_feature_flag_by_attributes.return_value = True
        mock_feature_flags_svc.return_value = self.mock_service

        self.assertTrue(is_feature_active_for_attributes("test", {"test": "test"}))
