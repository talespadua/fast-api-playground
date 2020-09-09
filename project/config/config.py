import os
from enum import Enum
from typing import Any

from project.config.exceptions import InvalidEnvironmentError

_ENVIRONMENT_KEY = "ENVIRONMENT"


class Environment(Enum):
    STAGING = "staging"
    PRODUCTION = "production"
    DEV = "development"


class Config:
    def get_config(self, name: str) -> Any:
        value = os.getenv(name)

        if not value:
            raise KeyError(f"Configuration [{name}] not found")
        return value

    def get_config_or_default(self, name: str, default: Any = None) -> Any:
        try:
            return self.get_config(name)
        except KeyError:
            return default

    def get_environment(self) -> Environment:
        value = self.get_config(_ENVIRONMENT_KEY)

        try:
            return Environment(value)
        except ValueError:
            raise InvalidEnvironmentError(value)
