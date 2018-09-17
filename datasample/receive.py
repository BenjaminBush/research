import nsq
import tornado.ioloop
import time

def handler(message):
    curr_ms = int(round(time.time()*1000))
    old_ms = message.body.decode("utf-8").split(";")[1]
    old_ms = int(float(old_ms))
    print("Latency is : {} ms".format(curr_ms-old_ms))
    #print("Message: {},\nTime: {}\n".format(message, ms))
    return True


r = nsq.Reader(message_handler=handler,
        lookupd_http_addresses=['http://127.0.0.1:4161'],
        topic='nsq-spark-out', channel='asdf', lookupd_poll_interval=15)
nsq.run()
