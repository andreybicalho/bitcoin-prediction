# Overview

Using data from social media (twitter, reddit, coindesk) to perform sentiment analysis and predict bitcoin price.

##### Usage #####
### Training Phase

* 1 - Generates bitcoin sentiment dataset from reddit; reddit_archived_bitcoin_sentiment.py - output: reddit_bitcoin_sentiment.csv
* 2 - Generates bitcoin price dataset from alphavantage; alphavantage.py - output: alphavantage_bitcoin_price.csv
* 3 - Merge both sentiment and price datasets; merge_data.py - output: merged_data.csv
* 4 - 
* 5 - 

### Live Phase
* live_twitter_sentiment.py continously collects twitter sentiment data till user press ctrl+c - output: bitcoin_tweets.json
* 
* 



# Credits

Credits for this code go to [sapphirine](https://github.com/Sapphirine/BITCOIN-PRICE-PREDICTION-USING-SENTIMENT-ANALYSIS). 
