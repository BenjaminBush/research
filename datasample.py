# import time
# import nsq
# import tornado.ioloop
# import pandas as pd
# import numpy as np

# global index
# index = 0

# def pub_message(df):
#     global index
#     row = df[index]
#     #time = row[0]
#     flow = row[1]
#     index += 1
#     writer.pub('sample_app_1', flow, finish_pub)

# def finish_pub(conn, data):
#     print(data)


# # nsqd_tcp_address = '127.0.0.1'
# # port = 4160
# # dest = nsqd_tcp_address+':'+str(port)

# file = 'test.csv'
# attr = 'Lane 1 Flow (Veh/5 Minutes)'
# df = pd.read_csv(file, encoding='utf-8').fillna(0)
# df = np.array(df)

# index = 0

# writer = nsq.Writer(['127.0.0.1:4150'])
# tornado.ioloop.PeriodicCallback(pub_message(df), 5000).start()
# nsq.run()



import nsq
import tornado.ioloop
import time
import pandas as pd
import numpy as np

global index
global df
index = 0
file = 'test.csv'
df = pd.read_csv(file, encoding='utf-8').fillna(0)
df = np.array(df)


def pub_message():
	global index
	global df
	row = df[index]
	flow = row[1]
	index += 1
	writer.pub('sample_app_1', str(flow), finish_pub)

def finish_pub(conn, data):
    print(data)



writer = nsq.Writer(['127.0.0.1:4150'])
tornado.ioloop.PeriodicCallback(pub_message, 5000).start()
nsq.run()

