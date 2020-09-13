from typing import cast

import pytest
from unittest.mock import MagicMock

from project.config import Config
from project.dal.retailer import RetailerRepository
from project.dtos.retailer import RetailerOutputDTO
from project.logger import Logger
from project.services import RetailerService
from test.helpers.factories.retailer_factory import RetailerModelFactory, \
    RetailerInputDtoFactory


class TestRetailerService:
    @pytest.fixture()
    def retailer_repository(self) -> RetailerRepository:
        mocked_repository = MagicMock()
        mocked_repository.get_retailer = MagicMock(return_value=RetailerModelFactory())
        mocked_repository.insert_retailer = MagicMock(return_value=True)
        return cast(RetailerRepository, mocked_repository)

    @pytest.fixture()
    def retailer_service(
        self,
        retailer_repository: RetailerRepository,
        config: Config,
        logger: Logger,
    ) -> RetailerService:
        return RetailerService(config, logger, retailer_repository)

    class TestGivenGettingRetailer:
        class TestWhenRetailerExists:
            def test_should_return_dto(self, retailer_service: RetailerService) -> None:
                assert type(retailer_service.get_retailer(1)) == RetailerOutputDTO

        class TestWhenRetailerDoesNotExists:
            @pytest.fixture()
            def retailer_repository(self) -> RetailerRepository:
                mocked_repository = MagicMock()
                mocked_repository.get_retailer = MagicMock(
                    return_value=None)

                return cast(RetailerRepository, mocked_repository)

            def test_should_return_none(
                self,
                retailer_service: RetailerService
            ) -> None:
                assert retailer_service.get_retailer(1) is None

    class TestGivenInsertingRetailer:
        class TestWhenInsertionIsSuccessful:
            def test_should_return_output_dto(
                self,
                retailer_service: RetailerService
            ) -> None:
                retailer_output_dto = retailer_service.insert_retailer(
                    RetailerInputDtoFactory()
                )
                assert type(retailer_output_dto) is RetailerOutputDTO

        class TestWhenInsertionIsNotSuccessful:
            @pytest.fixture()
            def retailer_repository(self) -> RetailerRepository:
                mocked_repository = MagicMock()
                mocked_repository.insert_retailer = MagicMock(return_value=False)
                return cast(RetailerRepository, mocked_repository)

            def test_should_return_none(
                self,
                retailer_service: RetailerService
            ) -> None:
                assert retailer_service.insert_retailer(
                    RetailerInputDtoFactory()
                ) is None
