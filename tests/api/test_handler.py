# Standard Library
from unittest import mock

# From apps
from api.handler import get_recipes_handler


@mock.patch("application.service.HelloWorldService.get_message", return_value="mock")
def test_get_recipes_handler(m_get_message):
    response = get_recipes_handler(None, None)
    assert response["body"] == '{"message": "mock"}'
    m_get_message.assert_called_once_with("get-recipes")
