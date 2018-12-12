# Overview

Price-Polarity-LSTM (pp-lstm) uses its sentiment data (polarity) from social media (twitter and reddit), as well as price features (open, close, low, high, volume and market capitalization) to predict bitcoin future price.

# Usage
### Training/Testing Phase

* 1 - Generates bitcoin sentiment dataset from reddit: 
    ```
        reddit_archived_bitcoin_sentiment.py
    ```
  Output: reddit_bitcoin_sentiment.csv
* 2 - Generates bitcoin price dataset from alphavantage: 
    ```
        alphavantage.py
    ```
    Output: alphavantage_bitcoin_price.csv
* 3 - Merge both sentiment and price datasets: 
  ```
    merge_data.py --s reddit_bitcoin_sentiment.csv --p alphavantage_bitcoin_price.csv
  ```
  Output: merged_data.csv
* 4 - Build the model (train and test):
    ```
        build_model.py --look_back 2 --sent --s --d merged_data.csv
    ```
* 5 - 

### Live Phase
* live_twitter_sentiment.py continously collects twitter sentiment data till user press ctrl+c - output: bitcoin_tweets.json
* 
* 



# Credits

Credits for this code go to [sapphirine](https://github.com/Sapphirine/BITCOIN-PRICE-PREDICTION-USING-SENTIMENT-ANALYSIS). 

# Requirements
Python 3.6

```bash
pip install -r requirements.txt
```
#