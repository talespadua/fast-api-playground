from fastapi import APIRouter, HTTPException

from project.config import Config
from project.logger import Logger
from project.retailers.dto import RetailerInputDTO, RetailerOutputDTO
from project.retailers.retailer_service import RetailerService

config = Config()
logger = Logger()

router = APIRouter()
retailerService = RetailerService(config, logger)


@router.get("/retailer/{retailer_id}/", response_model=RetailerOutputDTO)
async def get_retailer(retailer_id: int) -> RetailerOutputDTO:
    logger.info(f"Retailer ID: {str(retailer_id)}")
    retailer = retailerService.get_retailer(retailer_id)
    if not retailer:
        raise HTTPException(status_code=404, detail="Retailer not found")
    return retailer


@router.post("/retailer/", response_model=RetailerOutputDTO, status_code=201)
async def post_retailer(retailer: RetailerInputDTO) -> RetailerOutputDTO:
    return retailerService.insert_retailer(retailer)
