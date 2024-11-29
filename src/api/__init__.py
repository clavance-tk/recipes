# Standard Library
import logging

# From apps
from configuration import settings
from configuration.logger import Logger


def _setup_local_debug():
    try:
        # Dependencies
        import pydevd_pycharm  # type: ignore[import-not-found,import-untyped]

        pydevd_pycharm.settrace(
            "host.docker.internal",
            port=settings.debugging_port,
            stdoutToServer=True,
            stderrToServer=True,
        )
    except Exception:
        logging.exception("Could not connect to PyCharm. Please, check if the debugger is running.")


# Configure the logger.
# Placed in the api init as it is the entrypoint for all AWS handlers.
# It can be run several times, but only the first time will have an effect.
Logger.configure()
