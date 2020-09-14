from datetime import timedelta
from typing import cast, Dict, Any

import pytest
from unittest.mock import MagicMock

from project.config import Config
from project.dal.retailer import RetailerRepository
from project.dtos.auth import Token
from project.dtos.retailer import RetailerOutputDTO
from project.libs.criptography.password_handler import get_password_hash
from project.logger import Logger
from project.services.auth.auth_service import AuthService
from test.helpers.factories.retailer_factory import RetailerModelFactory


class TestAuthService:
    @pytest.fixture()
    def raw_password(self) -> str:
        return "123456"

    @pytest.fixture()
    def hashed_password(self, raw_password: str) -> str:
        return get_password_hash(raw_password)

    @pytest.fixture()
    def retailer_repository(self, hashed_password: str) -> RetailerRepository:
        mocked_repository = MagicMock()
        mocked_repository.get_retailer_by_email = MagicMock(
            return_value=RetailerModelFactory(password=hashed_password)
        )
        return cast(RetailerRepository, mocked_repository)

    @pytest.fixture()
    def expires_delta(self, config: Config) -> timedelta:
        return timedelta(
            minutes=int(config.get_config("ACCESS_TOKEN_EXPIRE_MINUTES"))
        )

    @pytest.fixture()
    def data(self) -> Dict[str, Any]:
        return {"sub": "t@gmail.com"}

    @pytest.fixture()
    def token(
        self,
        expires_delta: timedelta,
        data: Dict[str, Any],
        auth_service: AuthService
    ) -> str:
        return auth_service.generate_access_token(data, expires_delta)

    @pytest.fixture()
    def auth_service(
        self,
        config: Config,
        logger: Logger,
        retailer_repository: RetailerRepository
    ) -> AuthService:
        return AuthService(config, logger, retailer_repository)

    class TestAuthenticateRetailer:
        class TestWhenRetailerNotFound:
            @pytest.fixture()
            def retailer_repository(self) -> RetailerRepository:
                mocked_repository = MagicMock()
                mocked_repository.get_retailer_by_email = MagicMock(return_value=None)
                return cast(RetailerRepository, mocked_repository)

            def test_returns_none(self, auth_service: AuthService) -> None:
                assert auth_service.authenticate_retailer("t@gmail.com", "1234") is None

        class TestWhenPassingInvalidPassword:
            def test_return_none(self, auth_service: AuthService) -> None:
                assert auth_service.authenticate_retailer("t@gmail.com", "12") is None

        class TestWhenPassingValidPassword:
            def test_return_model(self, auth_service: AuthService) -> None:
                assert type(
                    auth_service.authenticate_retailer("t@gmail.com", "123456")
                ) is RetailerOutputDTO

    class TestGenerateAccessToken:
        def test_should_return_token(
            self,
            token: str
        ) -> None:
            assert token

    class TestGivenGetCurrentRetailer:
        class TestWhenTokenIsValid:
            def test_generate_jwt_token(
                self,
                token: str,
                auth_service: AuthService
            ) -> None:
                assert type(
                    auth_service.get_current_retailer(token)
                ) is RetailerOutputDTO
