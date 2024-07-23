from pydantic import BaseModel, Field
from typing import List


class CurrencyList(BaseModel):
    currency: str = Field(..., description="Waluta")
    buying: float = Field(..., description="Kupno")
    selling: float = Field(..., description="Sprzedaż")


class ApiResponse(BaseModel):
    name: str = Field(..., description="Nazwa kantora")
    currency: List[CurrencyList]


class ResponseList(BaseModel):
    items: List[ApiResponse]
