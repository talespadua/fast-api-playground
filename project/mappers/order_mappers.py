from project.dtos.order import OrderOutputDTO
from project.dal.models import OrderModel


def map_order_model_to_response(order_model: OrderModel) -> OrderOutputDTO:
    return (
        OrderOutputDTO(
            code=order_model.code,
            value=order_model.value,
            status=order_model.status,
            retailer_document=order_model.retailer_document,
            cashback_value=order_model.cashback,
            cashback_percentage=(order_model.value/order_model.cashback)
        )
    )