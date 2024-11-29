# Standard Library
from typing import Any

# Travelperk libraries
from tklib_trace.loggers import configure_logs

# From apps
from configuration import settings
from configuration.constants import Environment


class Logger:
    _initialized = False

    @staticmethod
    def configure(force: bool = False):
        if Logger._initialized is False or force is True:
            if settings.env != Environment.TEST:
                logging_config: dict[str, Any] = {
                    "version": 1,
                    "disable_existing_loggers": False,
                    "filters": {},
                    "handlers": {},
                    "formatters": {},
                    "loggers": {
                        "": {"level": settings.log_level},
                    },
                }
                configure_logs(logging_config, level=settings.log_level)
            Logger._initialized = True
