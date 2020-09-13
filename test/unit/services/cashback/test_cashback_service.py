from typing import cast

import pytest
from unittest.mock import MagicMock

from project.config import Config
from project.dtos.cashback import CashbackDTO
from project.libs.cashback_client import CashbackClient
from project.logger import Logger
from project.services.cashback.cashback_service import CashbackService


class TestGetCashbackService:
    @pytest.fixture()
    def cashback_client(self, response_json: str) -> CashbackClient:
        mocked_client = MagicMock()
        mocked_client.get_cashback_credit = MagicMock(return_value=response_json)
        return cast(CashbackClient, mocked_client)

    @pytest.fixture()
    def response_json(self) -> str:
        return '{"statusCode":200,"body":{"credit":3731}}'

    @pytest.fixture()
    def cashback_service(
        self,
        cashback_client: CashbackClient,
        config: Config,
        logger: Logger,
    ) -> CashbackService:
        return CashbackService(config, logger, cashback_client)

    class TestGetGivenSuccessfulCashbackCreditCall:
        def test_returns_cashback_dto(self, cashback_service: CashbackService) -> None:
            response = cashback_service.get_cashback_credit("123456")
            assert type(response) is CashbackDTO

    class TestGivenUnsuccessfulClientCashbackCreditCall:
        @pytest.fixture()
        def cashback_client(self) -> CashbackClient:
            mocked_client = MagicMock()
            mocked_client.get_cashback_credit = MagicMock(return_value=None)
            return cast(CashbackClient, mocked_client)

        def test_return_none(self, cashback_service: CashbackService) -> None:
            response = cashback_service.get_cashback_credit("1234")
            assert response is None
