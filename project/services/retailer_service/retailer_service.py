from typing import Optional

from project.config import Config
from project.logger import Logger
from project.dtos.retailer import RetailerInputDTO, RetailerOutputDTO
from project.dal.retailer import RetailerRepository
from project.mappers.retailer_mappers import (
    convert_input_dto_to_model,
    convert_model_to_output_dto
)


class RetailerService:
    def __init__(
        self,
        config: Config,
        logger: Logger,
        retailer_repository: RetailerRepository
    ) -> None:
        self.config = config
        self.logger = logger
        self.retailer_repository = retailer_repository

    def get_retailer(self, retailer_id: int) -> Optional[RetailerOutputDTO]:
        response_model = self.retailer_repository.get_retailer(retailer_id=retailer_id)
        if response_model:
            return convert_model_to_output_dto(response_model)
        return None

    def insert_retailer(
        self,
        retailer: RetailerInputDTO
    ) -> Optional[RetailerOutputDTO]:
        retailer_model = convert_input_dto_to_model(retailer)
        if self.retailer_repository.insert_retailer(retailer_model):
            return convert_model_to_output_dto(retailer_model)
        return None
