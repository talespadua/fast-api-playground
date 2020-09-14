from typing import Optional

import requests

from project.config import Config
from project.logger import Logger


class CashbackClient:
    def __init__(self, config: Config, logger: Logger):
        self.config = config
        self.logger = logger
        self.service_base_url = (
            "https://mdaqk8ek5j.execute-api.us-east-1.amazonaws.com/v1/"
        )
        self.token = "ZXPURQOARHiMc6Y0flhRC1LVlZQVFRnm"

    def get_cashback_credit(self, document: str) -> Optional[str]:
        cashback_url = self.service_base_url + f"/cashback?cpf={document}"
        response = requests.get(cashback_url, headers={"token": self.token})
        if response.status_code == 200:
            return response.text
        return None
