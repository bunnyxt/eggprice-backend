import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Activation
import pyeemd
import os


def get_data(data, timestep, train_size):
    # get dataset for train and test from data with given timestep and train size
    train_X, train_Y, test_X, test_Y = [], [], [], []
    for i in range(0, train_size - timestep):
        train_X.append(data[i:i + timestep].tolist())
        train_Y.append(data[i + timestep:i + timestep + 1].tolist())
    for i in range(train_size - timestep, data.shape[0] - timestep):
        test_X.append(data[i:i + timestep].tolist())
        test_Y.append(data[i + timestep:i + timestep + 1].tolist())
    train_X, train_Y = np.array(train_X), np.array(train_Y)
    train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
    train_Y = train_Y.reshape((train_Y.shape[0], train_Y.shape[1]))
    test_X, test_Y = np.array(test_X), np.array(test_Y)
    test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
    test_Y = test_Y.reshape((test_Y.shape[0], test_Y.shape[1]))
    return train_X, train_Y, test_X, test_Y


def get_model(unit_num, timestep):
    # create model
    model = Sequential()
    model.add(LSTM(units=unit_num, input_shape=(
        1, timestep), return_sequences=True))
    model.add(LSTM(units=unit_num))
    model.add(Dense(units=1))
    model.add(Activation('tanh'))
    model.compile(loss='mse', optimizer='adam')
    return model


def calc_RMSE(test_Y, prediction_Y):
    RMSE = 0
    for i in range(test_Y.size):
        RMSE += math.pow(prediction_Y[i][0] - test_Y[i][0], 2)
    RMSE /= test_Y.size
    RMSE = math.sqrt(RMSE)
    return RMSE


def calc_MAPE(test_Y, prediction_Y):
    MAPE = 0
    for i in range(test_Y.size):
        MAPE += (math.fabs((prediction_Y[i][0] - test_Y[i][0]) / test_Y[i][0]))
    MAPE /= test_Y.size
    return MAPE


if __name__ == "__main__":
    # os settings
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

    # load data from csv file
    data = pd.read_csv('data.csv', index_col='date', parse_dates=['date'])

    # normalize data
    data_max = data.max()
    data_min = data.min()
    data = (data - data_min) / (data_max - data_min)

    # get imfs via eemd
    imfs = pyeemd.eemd(data.values.reshape(-1))

    # plot imfs
    # i = 1
    # plt.figure(2)
    # for imf in imfs:
    #     plt.subplot(len(imfs), 1, i)
    #     plt.plot(imf)
    #     i += 1
    # plt.show()

    timestep = 10
    train_size = int(len(data) * 0.9)

    i = 1
    imfs_prediction = []
    for imf in imfs:
        # prepare train data and test data
        train_X, train_Y, test_X, test_Y = get_data(imf, timestep, train_size)

        # get model
        model = get_model(32, timestep)

        # fit network
        history = model.fit(train_X, train_Y, epochs=50, batch_size=24,
                            validation_data=(test_X, test_Y), verbose=2, shuffle=False)

        # make prediction
        prediction_Y = model.predict(test_X)

        # compare validation and prediction
        plt.subplot(len(imfs), 1, i)
        plt.plot(test_Y)
        plt.plot(prediction_Y)
        i += 1
        imfs_prediction.append(prediction_Y)

    plt.show()

    validation = data.values[train_size:]

    # compare
    prediction = [0 for i in range(len(validation))]
    for i in range(len(validation)):
        t = 0
        for imf_prediction in imfs_prediction:
            t += imf_prediction[i][0]
        prediction[i] = t

    plt.figure(4)
    plt.plot(validation)
    plt.plot(prediction)
    plt.show()

    RMSE = 0
    for i in range(len(validation)):
        RMSE += math.pow(prediction[i] - validation[i], 2)
    RMSE /= len(validation)
    RMSE = math.sqrt(RMSE)

    MAPE = 0
    for i in range(len(validation)):
        MAPE += (math.fabs((prediction[i] - validation[i]) / validation[i]))
    MAPE /= len(validation)

    print("RMSE %f\tMAPE %f" % (RMSE, MAPE * 100) + "%")