import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense


def train_lstm_model(df):

    data = df[['Close']].values

    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(data)

    x_train = []
    y_train = []

    for i in range(60, len(scaled_data)):
        x_train.append(scaled_data[i-60:i,0])
        y_train.append(scaled_data[i,0])

    x_train, y_train = np.array(x_train), np.array(y_train)

    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    model = Sequential()

    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1],1)))
    model.add(LSTM(units=50))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mean_squared_error')

    model.fit(x_train, y_train, epochs=3, batch_size=32, verbose=0)

    return model, scaler, x_train, y_train



def predict_future_prices(model, scaler, df, days=7):

    data = df[['Close']].values

    scaled_data = scaler.transform(data)

    last_60_days = scaled_data[-60:]

    predictions = []

    current_batch = last_60_days.reshape(1,60,1)

    for i in range(days):

        pred = model.predict(current_batch, verbose=0)[0]

        predictions.append(pred[0])

        current_batch = np.append(current_batch[:,1:,:], [[pred]], axis=1)

    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1,1))

    return predictions.flatten()