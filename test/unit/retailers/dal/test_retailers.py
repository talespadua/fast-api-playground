from typing import cast
import pytest

from project.config import Config
from project.logger import Logger
from project.retailers.dal.retailer import Retailer as RetailerDAL
from project.retailers.dto import RetailerInputDTO, RetailerOutputDTO
from test.helpers.factories.retailer_factory import RetailerInputFactory


@pytest.fixture()
def retailer_dal(config: Config, logger: Logger) -> RetailerDAL:
    return RetailerDAL(config, logger)


class TestRetailerDal:
    @pytest.fixture()
    def retailer(self) -> RetailerInputDTO:
        return cast(RetailerInputDTO, RetailerInputFactory())

    class GiverNoRetailer:
        @pytest.mark.usefixtures("create_tables")  # type: ignore
        def test_get_retailer(
            self,
            retailer_dal: RetailerDAL,
            retailer: RetailerInputDTO,
        ) -> None:
            retailer_output = retailer_dal.get_retailer(cast(int, retailer.id))
            assert retailer_output is None

    class TestGivenCreatedRetailer:
        @pytest.fixture()
        def created_retailer_model(
            self, retailer: RetailerInputDTO, retailer_dal: RetailerDAL
        ) -> RetailerOutputDTO:
            retailer_model = retailer_dal.insert_retailer(retailer)
            return retailer_model

        @pytest.mark.usefixtures("create_tables")  # type: ignore
        def test_get_retailer(
            self,
            retailer_dal: RetailerDAL,
            created_retailer_model: RetailerOutputDTO,
            retailer: RetailerInputDTO,
        ) -> None:
            retailer_output = retailer_dal.get_retailer(cast(int, retailer.id))
            assert retailer_output == created_retailer_model
