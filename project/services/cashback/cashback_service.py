from typing import Optional

from project.config import Config
from project.dtos.cashback import CashbackDTO
from project.libs.cashback_client import CashbackClient
from project.logger import Logger


class CashbackService:
    def __init__(self, config: Config, logger: Logger, client: CashbackClient):
        self.config = config
        self.logger = logger
        self.client = client

    def get_cashback_credit(self, document: str) -> Optional[CashbackDTO]:
        return self.client.get_cashback_credit(document)
