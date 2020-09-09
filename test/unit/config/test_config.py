from typing import Any

import pytest

from project.config.config import Environment
from project.config.exceptions import InvalidEnvironmentError
from project.config import Config


class TestConfig:
    @pytest.fixture()
    def config(self) -> Config:
        return Config()

    @pytest.fixture()
    def env_key(self) -> str:
        return "PORT"

    @pytest.fixture()
    def env_value(self) -> Any:
        return "8080"

    @pytest.fixture()
    def expected_config_value(self, config: Config, config_key: str) -> Any:
        return config.get_config(config_key)

    @pytest.fixture()
    def expected_config_or_default_value(
        self, config: Config, config_key: str, default_value: Any
    ) -> Any:
        return config.get_config_or_default(config_key, default_value)

    @pytest.fixture()
    def mock_env_var(  # type: ignore
        self,
        monkeypatch,
        env_key: str,
        env_value: Any,
    ) -> None:
        monkeypatch.setenv(env_key, env_value)

    class TestGivenExistingConfig:
        class TestGivenExistingEnvironmentConfig:
            @pytest.fixture()
            def config_key(self, env_key: str) -> str:
                return env_key

            def test_get_config_from_environment(  # type: ignore
                self, mock_env_var, expected_config_value: Any, env_value: Any
            ) -> None:
                assert expected_config_value == env_value

            def test_get_config_or_default_from_environment(  # type: ignore
                self, mock_env_var, expected_config_value: Any, env_value: Any
            ) -> None:
                assert expected_config_value == env_value

    class TestGivenMissingConfig:
        @pytest.fixture()
        def default_value(self) -> Any:
            return "default"

        @pytest.fixture()
        def config_key(self, env_key: str) -> str:
            return env_key

        def test_config_or_default(
            self, expected_config_or_default_value: Any, default_value: Any
        ) -> None:
            assert expected_config_or_default_value == default_value

    class TestGetEnvironment:
        class TestGivenEnvironmentExist:
            @pytest.fixture()
            def mock_env_var(  # type: ignore
                self,
                monkeypatch,
            ) -> None:
                monkeypatch.setenv("ENVIRONMENT", "staging")

            @pytest.fixture()
            def environment(  # type: ignore
                self, mock_env_var, config: Config
            ) -> Environment:
                return config.get_environment()

            def test_get_environment(self, environment: Environment):  # type: ignore
                assert environment.value == "staging"

        class TestGivenEnvironmentDoesNotExist:
            @pytest.fixture()
            def mock_env_var(  # type: ignore
                self,
                monkeypatch,
            ) -> None:
                monkeypatch.setenv("ENVIRONMENT", "foobar")

            def test_get_environment(  # type: ignore
                self, mock_env_var, config: Config
            ):
                with pytest.raises(InvalidEnvironmentError):
                    config.get_environment()
