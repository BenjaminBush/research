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
checkpoint_size = 10
max_received = 20000

# Kafka Setup
consumer = KafkaConsumer('output', bootstrap_servers=['localhost:9092'])

for message in consumer:
	# Timestamp right away
	curr_ns = rdtscp_module.rdtscp()

	# Decode the raw bytes
	data = message.value.decode('utf-8')

	#print(data)

	# Split the data
	data = data.split(";")

	i = 0

	# Get the location
	city = data[i]
	i += 1

	# Get the averge speed
	avg_speed = data[i]
	i += 1

	# Populate the actual flows array
	actual_flows = []
	while i < (lag+2):
		actual_flows.append(data[i])
		i += 1
	true_flows.append(actual_flows)

	# Get the predicted flow, append
	pred_flow = data[i]
	predicted_flows.append(pred_flow)
	i += 1

	# Calculate the latency
	old_ns = int(float(data[i]))
	latency = curr_ns - old_ns
	latencies.append(latency)	
	i += 1

	# Get the graph path
	graph_path = data[i:][0]

	# Bookkeeping
	messages_processed += 1
	if messages_processed % checkpoint_size == 0:
		print("City : {}".format(city))
		print("Actual_flows : {}".format(actual_flows))
		print("Predicted_flows : {}".format(pred_flow))
		print("Latency : {}".format(latency))
		print(messages_processed)

	if messages_processed % max_received == 0:
		np.savetxt('latency.txt', np.asarray(latencies), fmt='%d')
		sys.exit(0)