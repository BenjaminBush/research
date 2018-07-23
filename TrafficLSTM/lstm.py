import pandas as pd
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Embedding, LSTM
from keras.utils.visualize_util import plot
from sklearn.preprocessing import MinMaxScaler

import warnings

class LSTM(object):
	def __init__(self, dims=None, hypers=None):
		self.model = self.build_lstm()
		self.dims = dims if dims is not None else self.default_dims()
		self.hypers = hypers if hypers is not None else self.default_hypers()

	def build_lstm(self):
		model = Sequential()
		model.add(LSTM(self.dims[2], input_shape=(dims[0], 1), return_sequences=True, init='glorot_uniform', inner_init='glorot_uniform'))
		model.add(LSTM(self.dims[1], return_sequences=True, init='glorot_uniform'))
		model.Dropout(0.5)
		model.add(Dense(self.dims[3], activation='selu', init='glorot_uniform'))
		model.compile(loss=self.hypers['loss'], optimizer=self.hypers['optimizer'], metrics=self.hypers['metrics'])
		model.summary()
		plot(model, to_file='model.png')
		return model

	def default_dims(self):
		lag = 12
		input_dim = lag
		hidden_units = 128
		output_dim = hidden_units
		dense_dim = 1
		return [input_dim, hidden_units, output_dim, dense_dim]

	def default_hypers(self):
		self.hypers['batch_size'] = 128
		self.hypers['epochs'] = 100
		self.hypers['loss'] = 'mse'
		self.hypers['metrics'] = ['mape']
		self.hypers['optimizer'] = 'rmsprop'
		return