# usage: run: pytest --capture=no -v

import pytest
from alphavantage import AlphaVantage

def test_get_btc_usd_1D():
    av = AlphaVantage('GXEH3WTB0KG6CVPZ')
    data = av.get_digital_currency_daily(symbol='BTC', market='USD', export_to_csv=True, csv_filename='BTC-USD_daily.csv')
    all_high_price = max(data.values[:, 1])
    print(f'The highest price is ${all_high_price}')
    assert float(all_high_price) >= 19000.00