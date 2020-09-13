from typing import cast, List, Optional
from unittest.mock import MagicMock

import pytest

from project.config import Config
from project.dal.order.order import OrderRepository
from project.dtos.order import OrderInputDTO, OrderOutputDTO
from project.logger import Logger
from project.services import OrderService
from project.services.order_service.order_service import (
    ALLOWED_DOCUMENT_LIST,
    OrderStatus
)
from test.helpers.factories.order_factory import OrderModelFactory, OrderInputDTOFactory


class TestOrderService:
    @pytest.fixture()
    def order_repository(self) -> OrderRepository:
        mocked_repository = MagicMock()
        mocked_repository.get_orders = MagicMock(
            return_value=OrderModelFactory.build_batch(10)
        )
        mocked_repository.get_order_by_id = MagicMock(return_value=OrderModelFactory())
        mocked_repository.delete_order = MagicMock()
        mocked_repository.update_order = MagicMock()
        return cast(OrderRepository, mocked_repository)

    @pytest.fixture()
    def order_service(
        self,
        config: Config,
        logger: Logger,
        order_repository: OrderRepository
    ) -> OrderService:
        return OrderService(config, logger, order_repository)

    class TestInsertOrder:
        @pytest.fixture()
        def order_input(self) -> OrderInputDTO:
            return OrderInputDTOFactory()

        @pytest.fixture()
        def order_output_dto(
                self,
                order_service: OrderService,
                order_input: OrderInputDTO
        ) -> Optional[OrderOutputDTO]:
            return order_service.insert_order(order_input)

        class TestGivenAllowedDocument:
            @pytest.fixture()
            def order_output_dto(
                self,
                order_service: OrderService,
                order_input: OrderInputDTO
            ) -> Optional[OrderOutputDTO]:
                order_input.retailer_document = ALLOWED_DOCUMENT_LIST[0]
                return order_service.insert_order(order_input)

            def test_set_status_to_approved(
                self,
                order_output_dto: OrderOutputDTO
            ) -> None:
                assert order_output_dto.status == OrderStatus.APPROVED.value

        class TestGivenNotAllowedDocument:
            def test_set_status_to_approved(
                self,
                order_output_dto: OrderOutputDTO
            ) -> None:
                assert order_output_dto.status == OrderStatus.VALIDATING.value

    class TestGetOrderList:
        @pytest.fixture()
        def output_dto_list(
            self,
            order_service: OrderService
        ) -> List[OrderOutputDTO]:
            return order_service.get_order_list(page_size=10, page=1)

        def test_get_order_list(self, output_dto_list: List[OrderOutputDTO]) -> None:
            assert all(type(o) is OrderOutputDTO for o in output_dto_list)

    class TestGetOrderById:
        class TestGivenOrderFound:
            @pytest.fixture()
            def output_dto(
                self,
                order_service: OrderService
            ) -> Optional[OrderOutputDTO]:
                return order_service.get_order_by_id(123)

            def test_get_order_by_id(self, output_dto: OrderOutputDTO) -> None:
                assert type(output_dto) is OrderOutputDTO

        class TestGivenNoOrderWasFound:
            @pytest.fixture()
            def order_repository(self) -> OrderRepository:
                mocked_repository = MagicMock()
                mocked_repository.get_order_by_id = MagicMock(
                    return_value=None)
                return cast(OrderRepository, mocked_repository)

            @pytest.fixture()
            def output_dto(
                self,
                order_service: OrderService
            ) -> Optional[OrderOutputDTO]:
                return order_service.get_order_by_id(123)

            def test_get_order_by_id(
                self,
                output_dto: Optional[OrderOutputDTO]
            ) -> None:
                assert output_dto is None

    class TestDeleteOrder:
        def test_delete_order(self, order_service: OrderService) -> None:
            order_service.delete_order(123)

    class TestUpdateOrder:
        def test_update_order(self, order_service: OrderService) -> None:
            order_service.update_order(OrderInputDTOFactory())
