from typing import List

from fastapi import APIRouter, HTTPException, Depends

from project.config import Config
from project.dtos.order import OrderOutputDTO, OrderInputDTO
from project.dtos.retailer import RetailerOutputDTO
from project.logger import Logger
from project.services.order_service import OrderService, OrderStatus
from project.dal.order.order import OrderRepository
from project.transport import auth_service

config = Config()
logger = Logger()

router = APIRouter()

order_repository = OrderRepository(config, logger)
order_service = OrderService(config, logger, order_repository)


@router.get("/order/")
def get_order_list(
    page_size: int = 10,
    page: int = 1,
    current_retailer: RetailerOutputDTO = Depends(auth_service.get_current_retailer),
) -> List[OrderOutputDTO]:
    return order_service.get_order_list(page_size, page)


@router.post("/order/", response_model=OrderOutputDTO, status_code=201)
def insert_order(
    order: OrderInputDTO,
    current_retailer: RetailerOutputDTO = Depends(auth_service.get_current_retailer),
) -> OrderOutputDTO:
    return order_service.insert_order(order)


@router.delete("/order/{order_id}/")
def remove_order(
    order_id: int,
    current_retailer: RetailerOutputDTO = Depends(auth_service.get_current_retailer),
) -> None:
    order = order_service.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="No order found")
    if order.status == OrderStatus.APPROVED.value:
        raise HTTPException(status_code=405, detail="You cannot delete orders approved")
    order_service.delete_order(order_id)


@router.put("/order/{order_id}/", response_model=OrderOutputDTO)
def update_order(
    order_id: int,
    order_payload: OrderInputDTO,
    current_retailer: RetailerOutputDTO = Depends(auth_service.get_current_retailer),
) -> None:
    order_payload.id = order_id
    order = order_service.get_order_by_id(order_id)

    if not order:
        raise HTTPException(status_code=404, detail="No order found")
    if order.status == OrderStatus.APPROVED.value:
        raise HTTPException(status_code=405, detail="You cannot update orders approved")

    order_service.update_order(order_payload)
