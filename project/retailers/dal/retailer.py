from typing import Optional

from sqlalchemy.orm.exc import NoResultFound  # type: ignore[import]

from project.config import Config
from project.logger import Logger
from project.mysql_connection.mysql_connection import MySqlConnection
from project.models.retailer import RetailerModel
from project.retailers.dto import RetailerInputDTO, RetailerOutputDTO


class Retailer:
    def __init__(
        self,
        config: Config,
        logger: Logger,
    ):
        self.config = config
        self.logger = logger
        self.conn = MySqlConnection(config=config, logger=logger)

    def get_retailer(self, retailer_id: int) -> Optional[RetailerOutputDTO]:
        with self.conn.session() as session:
            try:
                retailer = (
                    session.query(RetailerModel)
                    .filter(RetailerModel.id == retailer_id)
                    .one()
                )
            except NoResultFound:
                return None

            retailer_dto = self._conver_model_to_output_dto(retailer)
            return retailer_dto

    def insert_retailer(self, new_retailer: RetailerInputDTO) -> RetailerOutputDTO:
        with self.conn.session() as session:
            retailer_model = self._convert_input_dto_to_model(new_retailer)
            session.add(retailer_model)
            session.commit()

            return self._conver_model_to_output_dto(retailer_model)

    def _convert_input_dto_to_model(
        self, retailer_dto: RetailerInputDTO
    ) -> RetailerModel:
        return RetailerModel(
            full_name=retailer_dto.full_name,
            document=retailer_dto.document,
            email=retailer_dto.email,
            password=retailer_dto.password,
        )

    def _conver_model_to_output_dto(
        self, retailer_model: RetailerModel
    ) -> RetailerOutputDTO:
        return RetailerOutputDTO(
            full_name=retailer_model.full_name,
            document=retailer_model.document,
            email=retailer_model.email,
        )
