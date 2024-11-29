# Standard Library
import logging
import sys
import unittest
from unittest.mock import patch

# From apps
from configuration.constants import Environment
from configuration.settings import Settings


@patch.dict(sys.modules, clear=True)
class TestSettings(unittest.TestCase):
    def test_settings(self):
        settings = Settings()
        self.assertEqual(settings.log_level, logging.INFO)
        self.assertEqual(settings.env, Environment.TEST)
