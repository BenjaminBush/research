import gnsq
import rdtscp_module

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
address = 'localhost'
port = '4150'
reader = gnsq.Reader(topic, channel, address+':'+port)

@reader.on_message.connect
def handler(reader, message):
    # Timestamp right away
    curr_ns = rdtscp_module.rdtscp()

    global true_flows
    global predicted_flows
    global latencies
    global messages_processed

    data = message.body.decode("utf-8").split(";")
    
    predicted_flows.append(data[0])
    true_flows.append(data[1])
    old_ns = int(float(data[2]))

    latency = curr_ns - old_ns
    latencies.append(latency)

    print("Latency is {} ns".format(latency))
    messages_processed += 1



reader.start()
