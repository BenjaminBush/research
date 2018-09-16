import nsq
import tornado.ioloop
import time

def handler(message):
    ms = int(round(time.time()*1000))
    print("Message body: {},\nMessage Time: {} \n".format(message.body.decode("utf-8"), message.timestamp))
    #print("Message: {},\nTime: {}\n".format(message, ms))
    return True


r = nsq.Reader(message_handler=handler,
        lookupd_http_addresses=['http://127.0.0.1:4161'],
        topic='nsq-spark-out', channel='asdf', lookupd_poll_interval=15)
nsq.run()
