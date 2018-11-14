import requests

def get_market_pair_from_alphavantage(function='DIGITAL_CURRENCY_DAILY', symbol='BTC', market='USD'):
    API_KEY = 'GXEH3WTB0KG6CVPZ'

    url = 'https://www.alphavantage.co/query?function='+function+'&symbol='+symbol+'&market='+market+'&apikey='+API_KEY
    r = requests.get(url)
    if (r.status_code == 200):
        return r.json()
        
    return r.reason