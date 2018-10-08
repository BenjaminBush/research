import nsq
import tornado.ioloop
import time
import rdtscp_module

global true_flows
global predicted_flows
global latencies
global messages_processed

true_flows = []
predicted_flows = []
latencies = []
messages_processed = 0

def handler(message):
    #curr_ns = int(round(time.time_ns()))
    curr_ns = rdtscp_module.rdtscp()

    global true_flows
    global predicted_flows
    global latencies
    global messages_processed

    messages_processed += 1

    data = message.body.decode("utf-8").split(";")
    predicted_flows.append(data[0])
    true_flows.append(data[1])

    old_ns = message.body.decode("utf-8").split(";")[2]
    old_ns = int(float(old_ns))
    curr_latency = curr_ns - old_ns
    latencies.append(curr_latency)

    print("Latency is : {} ns".format(curr_latency))

    if messages_processed % 100 == 0:
        with open("predicted.txt", "w+") as file:
            file.write(str(predicted_flows))
        file.close()
        predicted_flows = []

        with open("true.txt", "w+") as file:
            file.write(str(true_flows))
        file.close()
        true_flows = []

        with open("latency.txt", "w+") as file:
            file.write(str(latencies))
        file.close()
        latencies = []

    return True


r = nsq.Reader(message_handler=handler,
        lookupd_http_addresses=['http://127.0.0.1:4161'],
        topic='nsq-spark-out', channel='asdf', lookupd_poll_interval=15)
nsq.run()
