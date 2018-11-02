'''
Generates periodic events with random periodic behavior
'''
import random 
import numpy as np
import pandas as pd

global lo
global hi

lo = 0
hi = 1
# The Star Wars seed!
seed = 456123
random.seed(seed)

global uniform_time 
uniform_time = 0.1 # 100ms



def gen_uniform_events(dataset, uniform_time):
	n = dataset.shape[0]
	sleep_times = []
	for i in range(n):
		sleep_times.append(uniform_time)
	np.savetxt('uniform_sleep_times.txt', np.asarray(sleep_times), fmt='%5f')

def gen_random_events(dataset):
	global lo
	global hi
	n = dataset.shape[0]
	sleep_times = []
	for i in range(n):
		sleep_times.append(random.uniform(lo, hi))

	np.savetxt('random_sleep_times.txt', np.asarray(sleep_times), fmt='%5f')


if __name__ == '__main__':
	test = '../data/pems_test.csv'
	df = pd.read_csv(test, encoding='utf-8').fillna(0)
	df = np.array(df)
	gen_random_events(df)
	gen_uniform_events(df, uniform_time)