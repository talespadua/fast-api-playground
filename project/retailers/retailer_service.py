from typing import Optional

from project.config import Config
from project.logger import Logger
from project.retailers.dal.retailer_facade import RetailerFacade
from project.retailers.dto.retailer import RetailerInputDTO, RetailerOutputDTO


class RetailerService:
    def __init__(self, config: Config, logger: Logger) -> None:
        self.config = config
        self.logger = logger
        self.facade = RetailerFacade(self.config, self.logger)

    def get_retailer(self, retailer_id: int) -> Optional[RetailerOutputDTO]:
        return self.facade.get_retailer(retailer_id=retailer_id)

    def insert_retailer(self, retailer: RetailerInputDTO) -> RetailerOutputDTO:
        return self.facade.insert_retailer(retailer)
