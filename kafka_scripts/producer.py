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

# Experimental values
num_batches = 0
max_batches = 100
burst_size = 1

# Kafka setup
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
topic = 'test-output'

while num_batches < max_batches:
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

    # Check for a new batch, potentially sleep
    if index % burst_size == 0:
        num_batches += 1
        producer.flush()

    # Increment index
    index += 1
    if index >= 2000:
        index = 0


