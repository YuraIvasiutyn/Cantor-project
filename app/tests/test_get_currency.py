import pytest
from app.scraping.kantor import get_currency


@pytest.mark.parametrize("curr1, curr2, curr3", [('USD', 'EUR', 'GBP'),
                                                 ('CHF', 'AUD', 'CAD'),
                                                 ('JPY', 'DKK', 'NOK'),
                                                 ('SEK', 'CZK', 'RUB'),
                                                 ('HUF', 'RON', 'BGN'),
                                                 ('UAH', 'TRY', 'ILS'),
                                                 ('CNY', 'ALL', 'GEL'),
                                                 ('', '', '')]
                         )
@pytest.mark.asyncio
async def test_actual_currency(curr1, curr2, curr3):
    currency_list = [curr1, curr2, curr3]
    assert await get_currency(currency_list)
