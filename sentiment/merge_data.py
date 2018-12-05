import pandas as pd

btc_price_dataset = pd.read_csv('alphavantage_bitcoin_price.csv')
print('btc_price_dataset: '+str(btc_price_dataset.shape))
#btc_price_dataset.columns = ["date","close"]
btc_price_dataset.columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'maket cap']
btc_sentiment_dataset = pd.read_csv('reddit_bitcoin_sentiment.csv')
print('btc_sentiment_dataset: '+str(btc_sentiment_dataset.shape))
btc_sentiment_dataset.columns = ["date", "sentiment"]
#merged = btc_sentiment_dataset.merge(btc_price_dataset, on='date', left_index=False, right_index=False, how="inner")
merged = pd.merge(btc_price_dataset, btc_sentiment_dataset, how='inner', on='date')
merged.to_csv('merged_data.csv', index=False)
print('merged: '+str(merged.shape))