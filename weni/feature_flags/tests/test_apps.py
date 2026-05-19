from unittest import TestCase
from unittest.mock import patch

from weni.feature_flags.apps import PERIODIC_TASK_NAME, WeniFeatureFlagsConfig


class TestAppReady(TestCase):
    def _get_app_config(self):
        config = WeniFeatureFlagsConfig.__new__(WeniFeatureFlagsConfig)
        config.name = "weni.feature_flags"
        config.label = "weni_feature_flags"
        return config

    @patch("weni.feature_flags.apps.WeniFeatureFlagsConfig._setup_periodic_task")
    @patch("weni.feature_flags.settings.FEATURE_FLAGS_USE_SCHEDULED_UPDATES", True)
    def test_ready_sets_up_periodic_task_when_enabled(self, mock_setup):
        config = self._get_app_config()
        config.ready()
        mock_setup.assert_called_once()

    @patch("weni.feature_flags.apps.WeniFeatureFlagsConfig._setup_periodic_task")
    @patch("weni.feature_flags.settings.FEATURE_FLAGS_USE_SCHEDULED_UPDATES", False)
    def test_ready_does_nothing_when_disabled(self, mock_setup):
        config = self._get_app_config()
        config.ready()
        mock_setup.assert_not_called()


class TestSetupPeriodicTask(TestCase):
    def _get_app_config(self):
        config = WeniFeatureFlagsConfig.__new__(WeniFeatureFlagsConfig)
        config.name = "weni.feature_flags"
        config.label = "weni_feature_flags"
        return config

    @patch("weni.feature_flags.settings.FEATURE_FLAGS_SCHEDULED_UPDATE_INTERVAL", 90)
    @patch("celery.current_app")
    def test_setup_registers_beat_schedule_entry(self, mock_app):
        mock_app.conf.beat_schedule = {}

        config = self._get_app_config()
        config._setup_periodic_task()

        self.assertIn(PERIODIC_TASK_NAME, mock_app.conf.beat_schedule)
        entry = mock_app.conf.beat_schedule[PERIODIC_TASK_NAME]
        self.assertEqual(
            entry["task"],
            "weni.feature_flags.tasks.scheduled_update_feature_flags",
        )
        self.assertEqual(entry["schedule"], 90)

    @patch("weni.feature_flags.settings.FEATURE_FLAGS_SCHEDULED_UPDATE_INTERVAL", 60)
    @patch("celery.current_app")
    def test_setup_preserves_existing_beat_schedule_entries(self, mock_app):
        mock_app.conf.beat_schedule = {
            "existing-task": {"task": "some.other.task", "schedule": 30}
        }

        config = self._get_app_config()
        config._setup_periodic_task()

        self.assertIn("existing-task", mock_app.conf.beat_schedule)
        self.assertIn(PERIODIC_TASK_NAME, mock_app.conf.beat_schedule)

    @patch("weni.feature_flags.settings.FEATURE_FLAGS_SCHEDULED_UPDATE_INTERVAL", 60)
    @patch("celery.current_app")
    def test_setup_handles_missing_beat_schedule(self, mock_app):
        mock_app.conf.beat_schedule = None

        config = self._get_app_config()
        config._setup_periodic_task()

        self.assertIn(PERIODIC_TASK_NAME, mock_app.conf.beat_schedule)

    @patch("weni.feature_flags.settings.FEATURES_CACHE_TTL", 60)
    @patch("weni.feature_flags.settings.FEATURE_FLAGS_SCHEDULED_UPDATE_INTERVAL", 120)
    @patch("celery.current_app")
    def test_setup_warns_when_interval_exceeds_cache_ttl(self, mock_app):
        mock_app.conf.beat_schedule = {}
        config = self._get_app_config()

        with self.assertLogs("weni.feature_flags.apps", level="WARNING") as cm:
            config._setup_periodic_task()

        self.assertTrue(any("stale" in msg for msg in cm.output))
        self.assertIn(PERIODIC_TASK_NAME, mock_app.conf.beat_schedule)

    @patch("weni.feature_flags.settings.FEATURES_CACHE_TTL", 120)
    @patch("weni.feature_flags.settings.FEATURE_FLAGS_SCHEDULED_UPDATE_INTERVAL", 60)
    @patch("celery.current_app")
    def test_setup_does_not_warn_when_interval_below_cache_ttl(self, mock_app):
        mock_app.conf.beat_schedule = {}
        config = self._get_app_config()

        with patch("weni.feature_flags.apps.logger") as mock_logger:
            config._setup_periodic_task()

        mock_logger.warning.assert_not_called()
