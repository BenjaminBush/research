import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Embedding, LSTM
from keras.utils.vis_utils import plot_model
import warnings
import sys

class Model(object):
	def __init__(self, model="lstm", dims=None, hypers=None):
		self.dims = self.default_dims() if dims is None else dims
		self.hypers = self.default_hypers() if hypers is None else hypers

		if model == "lstm":
			print("Loading LSTM model.")
			self.model = self.build_lstm()
		elif model == "gru":
			print("Loading GRU model.")
			self.model = self.build_lstm() 	# Todo: Implement build_gru()
		elif model == "rnn":
			print("Loading RNN model.")
			self.model = self.build_lstm()	# Todo: Implement build_rnn()
		else:
			print("Unknown network")
			sys.exit()

	def default_dims(self):
		dims = {}
		dims['input_dim'] = 12
		dims['lstm_dim1'] = 256
		dims['lstm_dim2'] = 128
		dims['dense_dim1'] = 64
		dims['dense_dim2'] = 1
		return dims

	def default_hypers(self):
		hypers = {}
		hypers['batch_size'] = 128
		hypers['epochs'] = 10
		hypers['loss'] = 'mse'
		hypers['metrics'] = ['mape', 'mae']
		hypers['optimizer'] = 'rmsprop'
		return hypers

	def get_batch_size(self):
		return self.hypers['batch_size']

	def get_epochs(self):
		return self.hypers['epochs']

	def build_lstm(self):
		model = Sequential()
		model.add(LSTM(self.dims['lstm_dim1'], input_shape=(self.dims['input_dim'], 1), return_sequences=True, recurrent_initializer='glorot_uniform', kernel_initializer='glorot_uniform'))
		model.add(LSTM(self.dims['lstm_dim2'], recurrent_initializer='glorot_uniform', kernel_initializer='glorot_uniform'))
		model.add(Dropout(0.4))
		model.add(Dense(self.dims['dense_dim1'], activation='relu', kernel_initializer='glorot_uniform'))
		model.add(Dropout(0.5))
		model.add(Dense(self.dims['dense_dim2'], activation='relu', kernel_initializer='glorot_uniform'))
		model.compile(loss=self.hypers['loss'], optimizer=self.hypers['optimizer'], metrics=self.hypers['metrics'])
		model.summary()
		plot_model(model, to_file='model.png')
		return model

