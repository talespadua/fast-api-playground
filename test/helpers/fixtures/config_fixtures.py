import pytest
from project.logger import Logger
from project.config import Config


@pytest.fixture(scope="session")
def config() -> Config:
    return Config()


@pytest.fixture(scope="session")
def logger() -> Logger:
    return Logger()
