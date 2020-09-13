from pydantic import BaseModel


class CashbackDTO(BaseModel):
    credit: int
