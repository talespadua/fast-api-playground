from typing import Optional, List, cast

from sqlalchemy.orm.exc import NoResultFound  # type: ignore[import]

from project.config import Config
from project.logger import Logger
from project.dal.models import OrderModel
from project.dal.mysql_connection import MySqlConnection
from project.dtos.order import  OrderInputDTO


class OrderRepository:
    def __init__(self, config: Config, logger: Logger):
        self.config = config
        self.logger = logger
        self.conn = MySqlConnection(config=config, logger=logger)

    def get_order_by_id(self, order_id: int) -> Optional[OrderModel]:
        with self.conn.session() as session:
            session.expire_on_commit = False
            try:
                order_model = (
                    session.query(OrderModel)
                    .filter(OrderModel.id == order_id)
                    .one()
                )
                return cast(OrderModel, order_model)
            except NoResultFound:
                return None

    def get_order_list(self, page_size: int, page: int) -> List[OrderModel]:
        with self.conn.session() as session:
            order_list = (
                session.query(OrderModel)
                .offset(page_size * (page-1))
                .limit(page_size).all()
            )

            return [cast(OrderModel, o) for o in order_list]

    def insert_order(
        self,
        order_model: OrderModel,
    ) -> None:
        with self.conn.session() as session:
            session.expire_on_commit = False
            session.add(order_model)
            session.commit()

    def update_order(self, order_dto: OrderInputDTO) -> None:
        with self.conn.session() as session:
            session.query(OrderModel).filter(
                OrderModel.id == order_dto.id
            ).update(order_dto.dict(by_alias=True))
            session.commit()

    def delete_order(self, order_id: int) -> None:
        with self.conn.session() as session:
            session.query(OrderModel).filter(OrderModel.id == order_id).delete()
            session.commit()
