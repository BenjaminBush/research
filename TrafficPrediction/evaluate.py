from keras.models import load_model
import numpy as np
import pandas as pd
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import sklearn.metrics as metrics
import math 
import random

# Specify that we have a GPU and to use it for training/testing
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

def plot_results(day, y_true, y_preds):
    day = 22 + day
    d = '2018-3-' + str(day) + ' 00:00'
    x = pd.date_range(d, periods=288, freq='5min')
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(x, y_true, label='True Data')
    for y_pred in y_preds:
        ax.plot(x, y_pred, label='LSTM')

    plt.legend()
    plt.grid(True)
    plt.xlabel('Time of Day')
    plt.ylabel('Flow')

    date_format = mpl.dates.DateFormatter("%H:%M")
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()

    plt.show()


def get_data(train_file, test_file, lag):
    train = pd.read_csv(train_file)
    test = pd.read_csv(test_file)

    time_feature = '5 Minutes'
    flow_feature = 'Flow (Veh/5 Minutes)'

    # Scale the flow between 0 and 1 using minmax    
    feature_range = (0,1)
    data_min = np.min(train[flow_feature], axis=0)
    data_max = np.max(train[flow_feature], axis=0)
    data_range = data_max - data_min

    # Get the scale, min
    scale_ = ((feature_range[1] - feature_range[0])/data_range)
    min_ = feature_range[0]-data_min*scale_

    # Scale the training and testing data
    flow_train = train[flow_feature]
    flow_train *= scale_
    flow_train += min_

    flow_test = test[flow_feature]
    flow_test *= scale_
    flow_test += min_

    train_list, test_list = [], []

    for i in range(lag, len(flow_train)-1):
        train_list.append(flow_train[i-lag:i+1])
    for i in range(lag, len(flow_test)-1):
        test_list.append(flow_test[i-lag:i+1])

    train_list = np.asarray(train_list)
    test_list = np.asarray(test_list)

    X_train = train_list[:, :-1]
    y_train = train_list[:, -1]
    X_test = test_list[:, :-1]
    y_test = test_list[:, -1]

    scaler = (scale_, min_)

    return X_train, y_train, X_test, y_test, scaler

train_file = '../data/pems_train.csv'
test_file = '../data/pems_test.csv'
lag = 12

X_train, y_train, X_test, y_test, scaler = get_data(train_file, test_file, lag)


# Reshape to (samples, dimension, timestep)
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

scale_ = scaler[0]
min_ = scaler[1]

# Load the model
model_name = "lstm"
model = load_model(model_name + "_model.h5")

# Get predictions, truth
y_pred = model.predict(X_test)
y_true = y_test

# Get evaluation metrics
vs = metrics.explained_variance_score(y_true, y_pred)
mae = metrics.mean_absolute_error(y_true, y_pred)
mse = metrics.mean_squared_error(y_true, y_pred)
r2 = metrics.r2_score(y_true, y_pred)
print('explained_variance_score:%f' % vs)
print('mae:%f' % mae)
print('mse:%f' % mse)
print('rmse:%f' % math.sqrt(mse))
print('r2:%f' % r2)


predicted = y_pred
predicted -= min_
predicted /= scale_

y_test -= min_
y_test /= scale_

y_preds = []
random_day = random.randint(0,6)
idx = random_day*288
y_preds.append(predicted[idx:idx+288])
plot_results(random_day, y_test[idx:idx+288], y_preds)
