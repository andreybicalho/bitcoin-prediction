import pandas as pd

btc_price_dataset = pd.read_csv('alphavantage_bitcoin_price.csv')
#btc_price_dataset.columns = ["date","close"]
btc_price_dataset.columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'maket cap']
btc_sentiment_dataset = pd.read_csv('reddit_bitcoin_sentiment.csv')
btc_sentiment_dataset.columns = ["date", "sentiment"]
merged = btc_sentiment_dataset.merge(btc_price_dataset, left_index=False, right_index=False, how="inner")
merged.to_csv('merged_data.csv')