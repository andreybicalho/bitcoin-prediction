# usage: run: pytest --capture=no -v

import pytest
from download_data import get_market_pair_from_alphavantage

def test_get_btc_usd_from_alphavantage():
    result = get_market_pair_from_alphavantage(function='DIGITAL_CURRENCY_DAILY', symbol='BTC', market='USD')
    dataForAllDays = result['Time Series (Digital Currency Daily)']
    dataForSingleDate = dataForAllDays['2017-12-17']
    all_high_price = dataForSingleDate['2a. high (USD)']
    print(f'The highest price is ${all_high_price}')
    assert float(all_high_price) >= 19000.00