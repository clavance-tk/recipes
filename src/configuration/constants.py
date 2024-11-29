# Standard Library
from enum import Enum


class Environment(Enum):
    LOCAL = "local"
    TEST = "test"
    STAGING = "staging"
    PROD = "prod"
