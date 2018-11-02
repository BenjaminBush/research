import gnsq
import pandas as pd
import numpy as np
import rdtscp_module
import time
import random

# Variable initialization
test = '../data/pems_test.csv'
df = pd.read_csv(test, encoding='utf-8').fillna(0)
df = np.array(df)
#length = df.shape[0]
length = 2020

index = 0
lag = 12

# NSQ Setup
topic = 'nsq-spark-in'
conn = gnsq.Nsqd(address='192.168.0.120', http_port='4151')

num_batches = 0
# Experimental values
messages_sent = 0
max_messages = 20000

random_sleep = 0        # Binary flag for which sleep list to loat
sleep_times = []
if random_sleep:
    sleep_times = np.loadtxt('../sleep/random_sleep_times.txt').tolist()
else:
    sleep_times = np.loadtxt('../sleep/uniform_sleep_times.txt').tolist()

while messages_sent < max_messages:
    # Collect flows from dataframe
    data = df[index:index+lag]
    flows = data[:,1]

    # Create the message
    message = '  '.join(str(flow) for flow in flows)

    # Timestamp for latency
    ns = rdtscp_module.rdtscp()

    # Add timestamp to message
    ns_data = '  '+str(ns)
    message += ns_data

    # Publish and sleep
    response = conn.publish(topic, message)
    if response == b'OK':
        print(index)

    time.sleep(sleep_times[index])

    # Increment index
    index += 1
    if index >= 2000:
        index = 0

