import pytest
from project.logger import Logger
from project.config import Config


@pytest.fixture()
def mocked_envs(monkeypatch) -> None:  # type: ignore
    monkeypatch.setenv("DB_HOST", "db")
    monkeypatch.setenv("DB_PORT", "3306")
    monkeypatch.setenv("DB_USER", "root")
    monkeypatch.setenv("DB_DATABASE", "projectdb")
    monkeypatch.setenv("DB_PASSWORD", "password")
    monkeypatch.setenv("ENVIRONMENT", "development")


@pytest.fixture(scope="session")
def config_mock(mocked_envs) -> Config:  # type: ignore
    return Config()


@pytest.fixture(scope="session")
def logger_mock(config_mock: Config) -> Logger:
    return Logger()
