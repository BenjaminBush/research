import nsq
import tornado.ioloop
import time
import pandas as pd
import numpy as np

# Declare and initialize global variables
global index
global df

index = 0
test = 'test.csv'
df = pd.read_csv(test, encoding='utf-8').fillna(0)
df = np.array(df)

# Publishes messages to NSQ by reading from csv file
def pub_message():
	global index
	global df
        #row_index = df[index]
        #flow_index = row_index[1]
        data = df[index:index+12]
        flows = data[:, 1]
        #time = row[0].decode('utf-8')
        #message = str(flow) + ' ' + str(time)
        #print(message)
        message = '  '.join(str(el) for el in flows)
	index += 1
	writer.pub('nsq-spark-in', message, finish_pub)

# Callback function
def finish_pub(conn, data):
    print(data)



writer = nsq.Writer(['127.0.0.1:4150'])
tornado.ioloop.PeriodicCallback(pub_message, 1000).start()
nsq.run()
