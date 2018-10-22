import pandas as pd
import numpy as np
import rdtscp_module
import time

# Variable initialization
test = '../data/pems_test.csv'
df = pd.read_csv(test, encoding='utf-8').fillna(0)
df = np.array(df)
length = 15

index = 0
lag = 12

messages = []

while index < length:
    # Collect flows from dataframe
    data = df[index:index+lag]
    flows = data[:,1]

    # Timestamp for latency
    ns = rdtscp_module.rdtscp()

    # Add timestamp to message
    message = '  '.join(str(flow) for flow in flows)
    ns_data = '  '+str(ns)
    message += ns_data
    
    messages.append(message)

    # Increment index
    index += 1

with open('test.txt', 'w+') as f:
    for message in messages:
        f.write("{}\n".format(message))

    f.close()
