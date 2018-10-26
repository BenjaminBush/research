import gnsq
import rdtscp_module
import numpy as np
import sys

# Variable Initialization
global true_flows
global predicted_flows
global latencies
global messages_processed

true_flows = []
predicted_flows = []
latencies = []
messages_processed = 0

# NSQ Setup
topic = 'nsq-spark-out'
channel = 'asdf'
address = '192.168.0.120'
port = '4150'
reader = gnsq.Reader(topic, channel, address+':'+port, max_in_flight=1000, lookupd_poll_interval=1)

@reader.on_message.connect
def handler(reader, message):
    # Timestamp right away
    curr_ns = rdtscp_module.rdtscp()

    global true_flows
    global predicted_flows
    global latencies
    global messages_processed
    #print(message.body.decode("utf-8"))

    data = message.body.decode("utf-8").split(";")
    
    predicted_flows.append(data[0])
    true_flows.append(data[1])
    old_ns = int(float(data[2]))

    #print("Messages {} initiated at time {} and received at time {}".format(messages_processed, old_ns, curr_ns))
    #print(messages_processed)

    latency = curr_ns - old_ns
    latencies.append(latency)

    # print("Latency is {} ns".format(latency))

    messages_processed += 1

    if messages_processed % 200 == 0:
        print(messages_processed)

    if messages_processed % 20000 == 0:
        np.savetxt('latency.txt', np.asarray(latencies), fmt='%d')
        #np.savetxt('predicted.txt', np.asarray(predicted_flows), fmt='%d')
        #np.savetxt('true.txt', np.asarray(true_flows), fmt='%d')
        sys.exit(0)
reader.start()
