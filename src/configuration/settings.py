# Standard Library
import logging
from typing import Literal, Union

# Dependencies
from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings

# From apps
from configuration.constants import Environment


class Settings(BaseSettings):
    log_level: Union[int, Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]] = Field(default=logging.INFO)
    env: str = Field(default=str(Environment.TEST), validation_alias=AliasChoices("env", "dd_env"))
    debugging_port: int = Field(default=12345)
    debug: bool = Field(default=False)


settings = Settings()
