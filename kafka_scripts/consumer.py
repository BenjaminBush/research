from kafka import KafkaConsumer
import rdtscp_module
import numpy as np
import sys

# Variable Initialization
true_flows = []
predicted_flows = []
latencies = []
messages_processed = 0
lag = 12

# Experimental values
burst_size = 200
max_received = 20000

# Kafka Setup
consumer = KafkaConsumer('output',
						bootstrap_servers=['localhost:9092'])

for message in consumer:
	# Timestamp right away
	curr_ns = rdtscp_module.rdtscp()

	# Decode the raw bytes
	data = message.value.decode('utf-8')

	# Split the data
	data = data.split(";")

	# Calculate the latency
	old_ns = int(float(data[-1]))
	latency = curr_ns - old_ns
	latencies.append(latency)	

	# Get the predicted flow, append
	predicted_flows.append(data[-2])

	# Populate the actual flows array
	actual_flows = []
	i = 0
	while i < lag:
		actual_flows.append(data[i])
		i += 1

	# Append to true flows
	true_flows.append(actual_flows)



	# Bookkeeping
	messages_processed += 1
	if messages_processed % burst_size == 0:
		print("Actual_flows : {}".format(actual_flows))
		print("Predicted_flows : {}".format(data[-2]))
		print("Latency : {}".format(latency))
		print(messages_processed)

	if messages_processed % max_received == 0:
		np.savetxt('latency.txt', np.asarray(latencies), fmt='%d')
		sys.exit(0)
