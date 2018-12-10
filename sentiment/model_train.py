import numpy as np
from matplotlib import pyplot
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

dataset = pd.read_csv("merged_data.csv")
price_dataFrame = dataset[['open','high','low','volume','maket cap','close']]
sent_dataFrame = dataset[['sentiment']]
print(price_dataFrame.shape)
print(sent_dataFrame.shape)

# 1 - Feature Scaling
from sklearn.preprocessing import MinMaxScaler

# don't need to scale sentiment feature since it is already between 0 and 1
sentiment = sent_dataFrame.values.reshape(-1, sent_dataFrame.shape[1])
print(sentiment.shape)

# price features scaling/standardization
prices = price_dataFrame.values.reshape(-1, price_dataFrame.shape[1])
print(prices.shape)
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_prices = scaler.fit_transform(prices)
print(scaled_prices.shape)

# 2 - Spliting train and test sets
train_size = int(len(scaled_prices) * 0.7)
test_size = len(scaled_prices) - train_size
train, test = scaled_prices[0:train_size,:], scaled_prices[train_size:len(scaled_prices),:]
print(len(train), len(test))
split = train_size

def create_look_back_dataset(price_data, sentiment_data, look_back):
    dataX, dataY = [], []
    for i in range(len(price_data) - look_back):
        if i >= look_back:
            a = price_data[i-look_back:i+1, :]
            a = a.reshape(1, -1)
            b = sentiment_data[i-look_back:i+1, :]
            b = b.reshape(1, -1)
            a = np.hstack([a, b])
            a = a.tolist()            
            dataX.append(a)
            dataY.append(price_data[i + look_back, 5])
    return np.array(dataX), np.array(dataY)

look_back = 2
trainX, trainY = create_look_back_dataset(train, sentiment[0:train_size], look_back)
testX, testY = create_look_back_dataset(test, sentiment[train_size:len(scaled_prices)], look_back)
