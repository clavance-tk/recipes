from __future__ import annotations

# Standard Library
import json
from typing import TYPE_CHECKING

# From apps
from api import _setup_local_debug
from application.service import HelloWorldService
from configuration import settings

if TYPE_CHECKING:
    # Dependencies
    from aws_lambda_typing import context as context_, events


def get_recipes_handler(event: events.APIGatewayProxyEventV1, context: context_.Context) -> dict:
    # Please read the README instructions to configure the remote debugger in the IDE.
    if settings.debug:
        _setup_local_debug()

    message = HelloWorldService.get_message("get-recipes")
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": message,
            }
        ),
    }
