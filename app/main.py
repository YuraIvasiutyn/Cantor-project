import re

from fastapi import FastAPI, Query
from typing import Optional

from app.scraping import kantor
from app.models.api_model import ResponseList
from app.models.exceptions import CustomHTTPExceptionModel


app = FastAPI()


@app.get(
    "/actual-currency",
    response_model=ResponseList,
    status_code=200,
    responses={
        500: {"model": CustomHTTPExceptionModel},
    },
)
async def get_currencies(
    currency: Optional[str] = Query(
        None,
        description="Dostępne waluty:"
                    "USD,EUR,GBP,CHF,AUD,CAD,JPY,DKK,NOK,SEK,CZK,RUB,HUF,RON,BGN,UAH,TRY,ILS,CNY,ALL,GEL,HRK")
) -> ResponseList:

    if currency:
        currency_list = re.split(r',\s*', currency)
    else:
        currency_list = None

    return await kantor.get_currency(currency_list=currency_list)