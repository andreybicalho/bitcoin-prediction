import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--s", dest="sentiment_data", nargs='?', default='reddit_bitcoin_sentiment.csv')
parser.add_argument("--p", dest="price_data", nargs='?', default='alphavantage_bitcoin_price.csv')
parser.add_argument("--o", dest="output_file", nargs='?', default='merged_data.csv')
args = parser.parse_args()

btc_price_dataset = pd.read_csv(args.price_data)
print('btc_price_dataset: '+str(btc_price_dataset.shape))
#btc_price_dataset.columns = ["date","close"]
btc_price_dataset.columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'maket cap']
btc_sentiment_dataset = pd.read_csv(args.sentiment_data)
print('btc_sentiment_dataset: '+str(btc_sentiment_dataset.shape))
btc_sentiment_dataset.columns = ["date", "sentiment"]
#merged = btc_sentiment_dataset.merge(btc_price_dataset, on='date', left_index=False, right_index=False, how="inner")
merged = pd.merge(btc_price_dataset, btc_sentiment_dataset, how='inner', on='date')
merged.to_csv(args.output_file, index=False)
print('merged: '+str(merged.shape))