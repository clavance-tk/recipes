# Standard Library
import os
from enum import Enum


class Environment(Enum):
    LOCAL = "local"
    TEST = "test"
    STAGING = "staging"
    PROD = "prod"


# default values
TABLE_NAME = "recipes_service.recipes"
ENDPOINT_URL = f"http://{os.getenv('LOCALSTACK_HOSTNAME', 'localhost')}:4566"
