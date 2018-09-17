import nsq
import tornado.ioloop
import time
import pandas as pd
import numpy as np

# Declare and initialize global variables
global index
global df

index = 0
test = '../data/pems_test.csv'
df = pd.read_csv(test, encoding='utf-8').fillna(0)
df = np.array(df)

# Publishes messages to NSQ by reading from csv file
def pub_message():
    global index
    global df
    data = df[index:index+12]
    flows = data[:, 1]
    message = '  '.join(str(el) for el in flows)
    ms = int(time.time()*1000)
    ms_data = " " + str(ms)
    message += ms_data
    index += 1
    writer.pub('nsq-spark-in', message.encode(), finish_pub)

# Callback function
def finish_pub(conn, data):
    print(data)



#writer = nsq.Writer(['192.168.0.105:4150'])
writer=nsq.Writer(['127.0.0.1:4150'])
tornado.ioloop.PeriodicCallback(pub_message, 1).start()
nsq.run()

