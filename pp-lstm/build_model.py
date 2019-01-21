
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from math import sqrt
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--d", dest="dataset", nargs='?', default='merged_data.csv')
parser.add_argument("--lookback", dest="look_back", nargs='?', type=int, default=2)
parser.add_argument("--sent", dest="use_sentiment", action='store_true')
parser.add_argument("--s", dest="save_model", action='store_true')
args = parser.parse_args()

# 1 - Loading dataset
dataset = pd.read_csv(args.dataset)
price_dataFrame = dataset[['open','high','low','volume','maket cap','close']]
sent_dataFrame = dataset[['sentiment']]
#print(price_dataFrame.shape)
#print(sent_dataFrame.shape)

# 2 - Feature Scaling
# don't need to scale sentiment feature since it is already between 0 and 1
sentiment = sent_dataFrame.values.reshape(-1, sent_dataFrame.shape[1])
#print(sentiment.shape)

# price features scaling/standardization
prices = price_dataFrame.values.reshape(-1, price_dataFrame.shape[1])
#print(prices.shape)
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_prices = scaler.fit_transform(prices)
#print(scaled_prices.shape)

# 3 - Spliting train and test sets
train_size = int(len(scaled_prices) * 0.7)
test_size = len(scaled_prices) - train_size
train, test = scaled_prices[0:train_size,:], scaled_prices[train_size:len(scaled_prices),:]
print(f'Train set size: {len(train)}, Test set size: {len(test)}')
split = train_size

def create_look_back_dataset(price_data, sentiment_data, look_back, use_sentiment):
    dataX, dataY = [], []
    dataset_range = len(price_data) - look_back
    for i in range(dataset_range):
        if i >= look_back:
            a = price_data[i-look_back:i+1, :]
            a = a.reshape(1, -1)
            if use_sentiment:
                b = sentiment_data[i-look_back:i+1, :]
                b = b.reshape(1, -1)
                a = np.hstack([a, b])
            a = a.tolist()            
            dataX.append(a)
            dataY.append(price_data[i+look_back, 5]) # use the next day closing price for the dependent variable
    return np.array(dataX), np.array(dataY)

look_back = args.look_back
use_sentiment = args.use_sentiment
trainX, trainY = create_look_back_dataset(train, sentiment[0:train_size], look_back, use_sentiment)
testX, testY = create_look_back_dataset(test, sentiment[train_size:len(scaled_prices)], look_back, use_sentiment)
#print(trainX.shape[1], trainX.shape[2])

# 4 - Training the LSTM
model = Sequential()
model.add(LSTM(100, input_shape=(trainX.shape[1], trainX.shape[2]), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(100))
model.add(Dense(1))
model.compile(loss='mae', optimizer='adam')
#history = model.fit(trainX, trainY, epochs=300, batch_size=100, validation_data=(testX, testY), verbose=0, shuffle=False)
history = model.fit(trainX, trainY, epochs=50, batch_size=100, shuffle=False)

if args.save_model:
    model.save("model.h5")

# 5 - Testing the LSTM
yhat_test = model.predict(testX)

rmse = sqrt(mean_squared_error(testY, yhat_test))
print(f'Test RMSE: {rmse}')

# 6 - Visualizing the results

yhat_train = model.predict(trainX)

plt.figure(1)
plt.subplot(2, 1, 1)
plt.plot(trainY, label='Groundtruth', color='orange')
plt.plot(yhat_train, label='Predicted', color='purple')
plt.title("Training")
plt.ylabel("Scaled Price")
plt.legend(loc='upper left')

plt.subplot(2, 1, 2)
plt.plot(testY, label='Groundtruth', color='orange')
plt.plot(yhat_test, label='Predicted', color='purple')
plt.title("Test")
plt.ylabel("Scaled Price")
plt.legend(loc='upper left')

plt.show()

# 7 - Plot price (Inverse transform)
a = np.zeros((yhat_test.shape[0], 5))
yhat_test = np.hstack([a, yhat_test])
yhat_test_inverse = scaler.inverse_transform(yhat_test)
predicted_price = yhat_test_inverse[:, 5]

testY = testY.reshape(-1, 1)
testY = np.hstack([a, testY])
testY_inverse = scaler.inverse_transform(testY)
real_price = testY_inverse[:, 5]

plt.plot(real_price, label='Real', color='orange')
plt.plot(predicted_price, label='Predicted', color='purple')
plt.title("Predicted vs Real")
plt.ylabel("US$ Price")
plt.legend(loc='upper left')

plt.show()