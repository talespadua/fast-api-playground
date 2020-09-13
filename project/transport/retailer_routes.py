from fastapi import APIRouter, HTTPException

from project.config import Config
from project.dal.retailer import RetailerRepository
from project.logger import Logger
from project.dtos.retailer import RetailerInputDTO, RetailerOutputDTO
from project.services import RetailerService

config = Config()
logger = Logger()

router = APIRouter()
retailer_repository = RetailerRepository(config, logger)

retailerService = RetailerService(config, logger, retailer_repository)


@router.get("/retailer/{retailer_id}/", response_model=RetailerOutputDTO)
async def get_retailer(retailer_id: int) -> RetailerOutputDTO:
    logger.info(f"Retailer ID: {str(retailer_id)}")
    retailer = retailerService.get_retailer(retailer_id)
    if not retailer:
        raise HTTPException(status_code=404, detail="Retailer not found")
    return retailer


@router.post("/retailer/", response_model=RetailerOutputDTO, status_code=201)
async def post_retailer(retailer: RetailerInputDTO) -> RetailerOutputDTO:
    retailer_output = retailerService.insert_retailer(retailer)
    if not retailer_output:
        raise HTTPException(
            status_code=405,
            detail="Integrity Error. Check payload data"
        )
    return retailer_output
