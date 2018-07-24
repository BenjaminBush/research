import numpy as np

from lstm import LSTMNet 
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import os

os.environ['CUDA_VISIBLE_DEVICES'] = '0'

#from generator import DataGenerator

# training_generator = DataGenerator('training')
# validation_generator = DataGenerator('testing')

# lstm = LSTM()
# model = lstm.model
# model.fit_generator(generator=training_generator,
# 					validation_data=validation_generator,
# 					use_multiprocessing=True,
# 					workers=6)

def get_data(train_file, test_file, lag):
	train = pd.read_csv(train_file)
	test = pd.read_csv(test_file)

	time_feature = '5 Minutes'
	flow_feature = 'Lane 1 Flow (Veh/5 Minutes)'

	# Scale the flow between 0,1 using minmax scaler
	scaler = MinMaxScaler(feature_range=(0,1)).fit(train[flow_feature].values.reshape(-1, 1))

	flow_train = scaler.transform(train[flow_feature].values.reshape(-1,1).reshape(1, -1))[0]
	flow_test = scaler.transform(test[flow_feature].values.reshape(-1,1).reshape(1, -1))[0]

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

	return X_train, y_train, X_test, y_test, scaler

train_file = '../data/train.csv'
test_file = '../data/test.csv'
lag = 12

X_train, y_train, X_test, y_test, scaler = get_data(train_file, test_file, lag)


# Reshape to (samples, dimension, timestep)
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
y_scaled = y_test
y_test = scaler.inverse_transform(y_test.reshape(-1, 1)).reshape(1, -1)[0]

lstm = LSTMNet()
model = lstm.model

# Fit the model
model.fit(X_train, y_train, batch_size=lstm.get_batch_size(), epochs=lstm.get_epochs())

# Evaluate the model
score = model.evaluate(X_test, y_test, batch_size=lstm.get_batch_size())

print("Model score: {}".format(score))


