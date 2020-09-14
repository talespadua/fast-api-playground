from fastapi import APIRouter, HTTPException, Depends

from project.config import Config
from project.dtos.cashback import CashbackDTO
from project.dtos.retailer import RetailerOutputDTO
from project.libs.cashback_client import CashbackClient
from project.logger import Logger
from project.services.cashback.cashback_service import CashbackService
from project.transport import auth_service

config = Config()
logger = Logger()

router = APIRouter()
cashback_client = CashbackClient(config, logger)

cashback_service = CashbackService(config, logger, cashback_client)


@router.get("/cashback/credit/{document}/", response_model=CashbackDTO)
def get_cashback_credit(
    document: str,
    current_retailer: RetailerOutputDTO = Depends(auth_service.get_current_retailer)
) -> CashbackDTO:
    cashback = cashback_service.get_cashback_credit(document)
    if cashback:
        return cashback
    else:
        raise HTTPException(
            status_code=503, detail="cashback service currently unavailable"
        )
