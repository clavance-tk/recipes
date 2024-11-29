# From apps
from application.service import HelloWorldService


def test_get_message():
    assert HelloWorldService.get_message("mock") == "hello world from mock"
