import requests

from bs4 import BeautifulSoup
from typing import Optional
from app.models.exceptions import CustomHTTPException

from app.models.api_model import ApiResponse, CurrencyList, ResponseList
from app.logger.logger import logger
from app.conf.configurate import config
from app.models.config_model import CantorURL

url = CantorURL(**config["url_cantor"])

_DICT = {
    'Kantor 1913': [1, url.url1],
    'Czarny Koń': [0, url.url2]
}


def html_parser_generator(response_html: str, index: int, currency_list: Optional[list] = None) -> CurrencyList:
    soup = BeautifulSoup(response_html, 'html.parser')

    for curr in soup.find_all('tr'):
        try:
            price = [pr.text for pr in curr.find_all('td')]
            # Oczekujemy przynajmniej 4 elementy w liście, jeśli jest mniej - zwracamy pustą listę
            if len(price) >= 4:
                if currency_list is None:
                    yield CurrencyList(currency=price[index],
                                       buying=price[2],
                                       selling=price[3])
                    logger.info("Response full list")
                elif price[index] in currency_list:
                    yield CurrencyList(currency=price[index],
                                       buying=price[2],
                                       selling=price[3])
                    logger.info("Specific list of response")
                else:
                    logger.info("Empty list")
            else:
                logger.info("The list has less than 4 items")
        except IndexError as e:
            logger.error(f"Сannot find exchange rate data. {e}")
            raise CustomHTTPException(status_code=500,
                                      msg=f"Сannot find exchange rate data",
                                      devMsg=f"Сannot find exchange rate data. {e}")


async def get_currency(currency_list: Optional[list] = None) -> ResponseList:
    urls = _DICT

    items = []
    # Iterujemy przez wszystkie strony dla porównania kursu
    for key, values in urls.items():
        try:
            response = requests.get(url=values[1])
            html = response.text

            if response.status_code != requests.codes.ok:
                logger.error(
                    f"Unable to get data from web resources. Status Code: {response.status_code}, "
                    f"{response.raise_for_status()}")
                raise CustomHTTPException(status_code=500,
                                          msg="Unable to get data from web resources",
                                          devMsg=f"Unable to get data from web resources.{response.raise_for_status()}")
        except Exception as e:
            logger.error(f"There was a problem trying to receive the data. {e}")
            raise CustomHTTPException(status_code=500,
                                      msg="There was a problem trying to receive the data.",
                                      devMsg=f"There was a problem trying to receive the data. {e}")

        curr_list = []
        for curr in html_parser_generator(html, index=values[0], currency_list=currency_list):
            curr_list.append(curr)

        items.append(ApiResponse(name=key, currency=curr_list))

    return ResponseList(items=items)
