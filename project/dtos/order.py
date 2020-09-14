from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class OrderOutputDTO(BaseModel):
    code: int
    value: Decimal
    status: str
    retailer_document: str
    cashback_value: Decimal
    cashback_percentage: Decimal


class OrderInputDTO(BaseModel):
    id: Optional[int]
    code: int
    value: Decimal
    retailer_document: str
