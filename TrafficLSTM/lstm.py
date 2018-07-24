import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Embedding, LSTM
from keras.utils.vis_utils import plot_model
import warnings

class LSTMNet(object):
	def __init__(self, dims=None, hypers=None):
		self.dims = self.default_dims() if dims is None else dims
		self.hypers = self.default_hypers() if hypers is None else hypers
		self.model = self.build_lstm()

	def build_lstm(self):
		model = Sequential()
		model.add(LSTM(self.dims['output_dim'], input_shape=(self.dims['input_dim'], 1), return_sequences=True, recurrent_initializer='glorot_uniform', kernel_initializer='glorot_uniform'))
		model.add(LSTM(self.dims['hidden_units'], recurrent_initializer='glorot_uniform', kernel_initializer='glorot_uniform'))
		model.add(Dropout(0.5))
		model.add(Dense(self.dims['dense_dim'], activation='relu', kernel_initializer='glorot_uniform'))
		model.compile(loss=self.hypers['loss'], optimizer=self.hypers['optimizer'], metrics=self.hypers['metrics'])
		model.summary()
		plot_model(model, to_file='model.png')
		return model

	def default_dims(self):
		dims = {}
		dims['input_dim'] = 12
		dims['hidden_units'] = 128
		dims['output_dim'] = dims['hidden_units']
		dims['dense_dim'] = 1
		return dims

	def default_hypers(self):
		hypers = {}
		hypers['batch_size'] = 128
		hypers['epochs'] = 600
		hypers['loss'] = 'mse'
		hypers['metrics'] = ['mape']
		hypers['optimizer'] = 'rmsprop'
		return hypers

	def get_batch_size(self):
		return self.hypers['batch_size']

	def get_epochs(self):
		return self.hypers['epochs']