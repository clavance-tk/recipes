# Standard Library
import logging
import sys
import unittest
from unittest.mock import patch

# From apps
from configuration.settings import Settings


@patch.dict(sys.modules, clear=True)
class TestSettings(unittest.TestCase):
    def test_settings(self):
        settings = Settings()
        self.assertEqual(settings.log_level, logging.INFO)
        # getting a strange type error , comparing string values instead.
        # FAILED tests/configuration/test_settings.py::TestSettings::test_settings - AssertionError: <Environment.TEST: 'test'> != <Environment.TEST: 'test'>
        self.assertEqual(settings.env, "test")
