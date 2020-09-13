from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class RetailerOutputDTO(BaseModel):
    full_name: str = Field(..., max_length=100)
    document: str = Field(..., max_length=30)
    email: EmailStr = Field(...)


class RetailerInputDTO(RetailerOutputDTO):
    id: Optional[int] = None
    password: str = Field(..., max_length=100)
