import gnsq
import pandas as pd
import numpy as np
import rdtscp_module
import time

# Variable initialization
test = '../data/pems_test.csv'
df = pd.read_csv(test, encoding='utf-8').fillna(0)
df = np.array(df)
length = df.shape[0]

index = 0
lag = 12

# NSQ Setup
topic = 'nsq-spark-in'
conn = gnsq.Nsqd(address='127.0.0.1', http_port='4151')

while index < length:
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

    # Increment index
    index += 1

    # Publish and sleep
    response = conn.publish(topic, message)
    if response == b'OK':
        print(index)
    time.sleep(1)