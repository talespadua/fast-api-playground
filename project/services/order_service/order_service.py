from decimal import Decimal
from enum import Enum
from typing import Optional, List

from project.config import Config
from project.dal.models import OrderModel
from project.logger import Logger
from project.dal.order import OrderRepository
from project.dtos.order import OrderOutputDTO, OrderInputDTO
from project.services.order_service.cashback_rules import CASHBACK_RULES
from project.mappers.order_mappers import map_order_model_to_response


class OrderStatus(Enum):
    VALIDATING = "Em Validação"
    APPROVED = "Aprovado"


ALLOWED_DOCUMENT_LIST = [
    "153.509.460-56",
]


class OrderService:
    def __init__(
        self, config: Config, logger: Logger, order_repository: OrderRepository
    ):
        self.config = config
        self.logger = logger
        self.order_repository = order_repository

    def get_order_by_id(self, order_id: int) -> Optional[OrderOutputDTO]:
        order_model = self.order_repository.get_order_by_id(order_id)
        if order_model:
            return map_order_model_to_response(order_model)
        return None

    def get_order_list(self, page_size: int, page: int) -> List[OrderOutputDTO]:
        orders = self.order_repository.get_order_list(page_size, page)
        return [map_order_model_to_response(o) for o in orders]

    def insert_order(self, order_dto: OrderInputDTO) -> OrderOutputDTO:
        order_status = self._generate_order_status(order_dto.retailer_document)
        order_cashback = self._calculate_order_cashback(order_dto.value)

        order_model = OrderModel(
            code=order_dto.code,
            value=float(order_dto.value),
            retailer_document=order_dto.retailer_document,
            status=order_status,
            cashback=float(order_cashback),
        )

        self.order_repository.insert_order(order_model)
        return map_order_model_to_response(order_model)

    def update_order(self, order_dto: OrderInputDTO) -> None:
        self.order_repository.update_order(order_dto)

    def delete_order(self, order_id: int) -> None:
        self.order_repository.delete_order(order_id)

    def _generate_order_status(self, document: str) -> str:
        if document in ALLOWED_DOCUMENT_LIST:
            return OrderStatus.APPROVED.value
        return OrderStatus.VALIDATING.value

    def _calculate_order_cashback(self, value: Decimal) -> Decimal:
        for rule in CASHBACK_RULES:
            if rule.accept(value):
                return rule.calculate_cashback(value)
        return Decimal(0.0)
