# Standard Library
import logging

# Dependencies
import pytest
from ddtrace import tracer

# From apps
from configuration.logger import Logger


@pytest.fixture(autouse=True, scope="session")
def m_logger():
    """
    this is needed to avoid the following error:
        ValueError: I/O operation on closed file.
    that takes a long time to appear until this other error appears:
        RecursionError: maximum recursion depth exceeded while calling a Python object

    that happens when running pytest twice in a shell (and possibly other scenarios) because
    the output is captured by pytest in a first run (and later the output handler is closed causing logging exceptions)

    because pytest behaves like this:
    https://github.com/pytest-dev/pytest/issues/5502#issuecomment-526348052
    """
    tracer.enabled = False  # disabling DD tracer to avoid JSON format in logs (coupled to tklib_trace implementation)
    Logger.configure(
        force=True
    )  # configure everytime to ensure the new pytest stream handler (capturing output) works as expected
    yield
    # ... and tearDown cleanup inspired by https://github.com/pytest-dev/pytest/issues/5502#issuecomment-1492179828
    loggers = [logging.getLogger()] + list(logging.Logger.manager.loggerDict.values())
    for logger in loggers:
        handlers = getattr(logger, "handlers", [])
        for handler in handlers:
            # this is to let the logging platform work as expected even when the pytest stream handlers are closed
            logger.removeHandler(handler)
