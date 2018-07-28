'''
Class that creates a custom Keras Data Generator
'''
import numpy as np
import pandas as pd
import os

class DataLoader(object):
	def __init__(self, data_folder='../data/', cache_folder='../dataset_caches'):
		self.data = None



