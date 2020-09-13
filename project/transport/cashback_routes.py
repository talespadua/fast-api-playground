from fastapi import APIRouter, HTTPException

from project.config import Config
from project.dtos.cashback import CashbackDTO
from project.libs.cashback_client import CashbackClient
from project.logger import Logger
from project.services.cashback.cashback_service import CashbackService

config = Config()
logger = Logger()

router = APIRouter()
cashback_client = CashbackClient(config, logger)

cashback_service = CashbackService(config, logger, cashback_client)


@router.get("/cashback/credit/{document}/", response_model=CashbackDTO)
def get_cashback_credit(document: str) -> CashbackDTO:
    cashback = cashback_service.get_cashback_credit(document)
    if cashback:
        return cashback
    else:
        raise HTTPException(
            status_code=503, detail="cashback service currently unavailable"
        )
