import numpy as np
from sklearn.preprocessing import MinMaxScaler
from models import Model
import pandas as pd
import os
import json
from sklearn.model_selection import train_test_split
import matplotlib as mpl
import matplotlib.pyplot as plt
import keras

os.environ['CUDA_VISIBLE_DEVICES'] = '0'

def plot_results(y_true, y_preds):
    names = ['LSTM']
    d = '2016-3-4 00:00'
    x = pd.date_range(d, periods=288, freq='5min')

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(x, y_true, label='True Data')
    for name, y_pred in zip(names, y_preds):
        ax.plot(x, y_pred, label=name)

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

	scale_ = ((feature_range[1] - feature_range[0])/data_range)
	min_ = feature_range[0]-data_min*scale_

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


model_name = "lstm"
network = Model(model_name)
model = network.model

# Set the early stopping callback
callback = keras.callbacks.EarlyStopping(monitor='val_loss', patience=5)

# Fit the model
model.fit(X_train, y_train, batch_size=network.get_batch_size(), epochs=network.get_epochs(), validation_split=0.1, callbacks=[callback])

# Save the model
model.save(model_name+"_model.h5")

# Evaluate the model
score = model.evaluate(X_test, y_test, batch_size=network.get_batch_size())

print("Model score: {}".format(score))

print("Model metrics {}".format(model.metrics_names))

# Get predictions
predicted = model.predict(X_test)

# Store metadata
metadata = {}
batch_size = network.get_batch_size()
epochs = network.get_epochs()

metadata['model'] = model_name
metadata['batch_size'] = batch_size
metadata['epochs'] = epochs
metadata['scale'] = scale_
metadata['min'] = min_
metadata['score'] = score

# Store it as JSON so that Scala can read it
with open('metadata.json', 'w+') as fp:
    json.dump(metadata, fp)





