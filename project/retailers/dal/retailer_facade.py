from typing import Optional

from project.config import Config
from project.logger import Logger
from project.retailers.dal.retailer import Retailer
from project.retailers.dto import RetailerOutputDTO, RetailerInputDTO


class RetailerFacade:
    def __init__(self, config: Config, logger: Logger):
        self.config = config
        self.logger = logger
        self.retailer = Retailer(config, logger)

    def get_retailer(self, retailer_id: int) -> Optional[RetailerOutputDTO]:
        return self.retailer.get_retailer(retailer_id)

    def insert_retailer(self, retailer: RetailerInputDTO) -> RetailerOutputDTO:
        return self.retailer.insert_retailer(retailer)
