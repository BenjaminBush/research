from kafka import KafkaProducer
from kafka.errors import KafkaError
import pandas as pd
import numpy as np
import rdtscp_module
import time
import random

# Variable initialization
test = '../data/pems_test.csv'
df = pd.read_csv(test, encoding='utf-8').fillna(0)
df = np.array(df)

length = 2020
index = 0
lag = 12


# Kafka setup
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
topic = 'input'

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
    message = ';'.join(str(flow) for flow in flows)

    fake_prediction = ";" + str(0)
    message += fake_prediction

    # Timestamp for latency
    ns = rdtscp_module.rdtscp()

    # Add timestamp to message
    ns_data = ';'+str(ns)
    message += ns_data

    producer.send(topic, value=str.encode(message))
    producer.flush()

    # Introduce periodic behavior by sleeping  after producing message
    time.sleep(sleep_times[index])
    
    # Increment index
    index += 1
    if index >= 2000:
        index = 0





