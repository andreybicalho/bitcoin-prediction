
# 1 - Loading dataset
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from math import sqrt
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

dataset = pd.read_csv("merged_data.csv")
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
#print(f'Train set size: {len(train)}, Test set size: {len(test)}')
split = train_size

def create_look_back_dataset(price_data, sentiment_data, look_back):
    dataX, dataY = [], []
    dataset_range = len(price_data) - look_back
    for i in range(dataset_range):
        if i >= look_back:
            a = price_data[i-look_back:i+1, :]
            a = a.reshape(1, -1)
            b = sentiment_data[i-look_back:i+1, :]
            b = b.reshape(1, -1)
            a = np.hstack([a, b])
            a = a.tolist()            
            dataX.append(a)
            dataY.append(price_data[i+look_back, 5]) # TODO: use the next day close price for the dependent variable
    return np.array(dataX), np.array(dataY)

look_back = 2
trainX, trainY = create_look_back_dataset(train, sentiment[0:train_size], look_back)
testX, testY = create_look_back_dataset(test, sentiment[train_size:len(scaled_prices)], look_back)

# 4 - Training the LSTM
model = Sequential()
model.add(LSTM(100, input_shape=(trainX.shape[1], trainX.shape[2]), return_sequences=True))
model.add(LSTM(100))
model.add(Dense(1))
model.compile(loss='mae', optimizer='adam')
#history = model.fit(trainX, trainY, epochs=300, batch_size=100, validation_data=(testX, testY), verbose=0, shuffle=False)
history = model.fit(trainX, trainY, epochs=50, batch_size=100, shuffle=False)

#model.save("model.h5", overwrite=True, include_optimizer=True)

# 5 - Testing the LSTM
yhat_test = model.predict(testX)

# TODO: inverse transform to get the price
#yhat_inverse = scaler.inverse_transform(yhat.reshape(-1, 1))
#testY_inverse = scaler.inverse_transform(testY.reshape(-1, 1))

rmse = sqrt(mean_squared_error(testY, yhat_test))
print('Test RMSE: %.3f' % rmse)

# 6 - Visualizing the results

yhat_train = model.predict(trainX)

plt.figure(1)
plt.subplot(2, 1, 1)
plt.plot(trainY, label='Groundtruth', color='orange')
plt.plot(yhat_train, label='Predicted', color='purple')
plt.title("Training")
plt.ylabel("Scaled Price")

plt.subplot(2, 1, 2)
plt.plot(testY, label='Groundtruth', color='orange')
plt.plot(yhat_test, label='Predicted', color='purple')
plt.title("Test")
plt.ylabel("Scaled Price")

plt.show()