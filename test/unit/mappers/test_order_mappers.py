from typing import cast

import pytest

from project.dal.models import OrderModel
from project.dtos.order import OrderOutputDTO
from project.mappers.order_mappers import map_order_model_to_response
from test.helpers.factories.order_factory import OrderModelFactory


class TestMapOrderModelToResponseDTO:
    @pytest.fixture()
    def order_model(self) -> OrderModel:
        return cast(OrderModel, OrderModelFactory())

    @pytest.fixture()
    def order_dto(self, order_model: OrderModel) -> OrderOutputDTO:
        return map_order_model_to_response(order_model)

    def test_map_order_model_to_response(
        self, order_model: OrderModel, order_dto: OrderOutputDTO
    ) -> None:
        assert order_dto.value == order_model.value
        assert order_dto.code == order_model.code
        assert order_dto.retailer_document == order_model.retailer_document
        assert order_dto.status == order_model.status
        assert order_dto.cashback_value == order_model.cashback
        assert order_dto.cashback_percentage
