from typing import Optional, cast

from sqlalchemy.exc import IntegrityError  # type: ignore[import]
from sqlalchemy.orm.exc import NoResultFound  # type: ignore[import]

from project.config import Config
from project.logger import Logger
from project.dal.mysql_connection import MySqlConnection
from project.dal.models import RetailerModel


class RetailerRepository:
    def __init__(
        self,
        config: Config,
        logger: Logger,
    ):
        self.config = config
        self.logger = logger
        self.conn = MySqlConnection(config=config, logger=logger)

    def get_retailer(self, retailer_id: int) -> Optional[RetailerModel]:
        with self.conn.session() as session:
            session.expire_on_commit = False
            try:
                retailer = (
                    session.query(RetailerModel)
                    .filter(RetailerModel.id == retailer_id)
                    .one()
                )
            except NoResultFound:
                return None

            return cast(RetailerModel, retailer)

    def get_retailer_by_email(
        self,
        retailer_email: Optional[str]
    ) -> Optional[RetailerModel]:
        with self.conn.session() as session:
            session.expire_on_commit = False
            try:
                retailer = (
                    session.query(RetailerModel)
                    .filter(RetailerModel.email == retailer_email)
                    .one()
                )
            except NoResultFound:
                return None

            return cast(RetailerModel, retailer)

    def insert_retailer(self, retailer_model: RetailerModel) -> bool:
        with self.conn.session() as session:
            session.expire_on_commit = False
            try:
                session.add(retailer_model)
                session.commit()
                return True
            except IntegrityError:
                return False
