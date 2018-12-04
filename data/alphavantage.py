import requests
import datetime
import pandas as pd

class AlphaVantage(object):

    def __init__(self, api_key):
        self.api_url = 'https://www.alphavantage.co/query?'
        self.api_key = api_key

    def __call_api(self, function, symbol, market):
        url = self.api_url + 'function='+function+'&symbol='+symbol+'&market='+market+'&apikey='+self.api_key
        print('Requesting '+url)
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()

        return response.reason

    def get_digital_currency_daily(self, symbol='BTC', market='USD', export_to_csv=False, csv_filename='BTC-USD_daily.csv'):
        function = 'DIGITAL_CURRENCY_DAILY'
        data_label = 'Time Series (Digital Currency Daily)'

        json = self.__call_api(function, symbol, market)

        data = json[data_label]
        df = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume', 'maket cap'])
        for d,p in data.items():
            date = datetime.datetime.strptime(d,'%Y-%m-%d').strftime('%Y-%m-%d')
            data_row = [date, float(p['1a. open (USD)']),float(p['2a. high (USD)']),float(p['3a. low (USD)']),float(p['4a. close (USD)']),float(p['5. volume']),float(p['6. market cap (USD)'])]            
            df.loc[-1,:] = data_row
            df.index = df.index + 1

        data = df.sort_values('date')

        if export_to_csv:
            data.to_csv(csv_filename, index=False)

        return data

if __name__ == "__main__":
    av = AlphaVantage('GXEH3WTB0KG6CVPZ')
    data = av.get_digital_currency_daily(symbol='BTC', market='USD', export_to_csv=True, csv_filename='alphavantage_bitcoin_price.csv')