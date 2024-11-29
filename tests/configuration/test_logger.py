# Standard Library
from unittest.mock import patch

# From apps
from configuration.constants import Environment
from configuration.logger import Logger


@patch("configuration.logger.configure_logs")
@patch("configuration.settings.settings.env", Environment.LOCAL)
def test_configure_logs(mock_configure_logs):
    Logger.configure(force=True)
    mock_configure_logs.assert_called_once()
