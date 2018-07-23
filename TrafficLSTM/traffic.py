import numpy as numpy

from lstm import LSTM 
from generator import DataGenerator

training_generator = DataGenerator()
validation_generator = DataGenerator()

lstm = LSTM()
model = lstm.model
model.fit_generator(generator=training_generator,
					validation_data=validation_generator,
					use_multiprocessing=True,
					workers=6)