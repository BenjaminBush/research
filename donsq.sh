./home/ben/go/src/github.com/nsqio/nsq/apps/nsqlookupd/nsqlookupd & 
./home/ben/go/src/github.com/nsqio/nsq/apps/nsqd/nsqd --lookupd-tcp-address=127.0.0.1:4160 &
./home/ben/go/src/github.com/nsqio/nsq/apps/nsqadmin/nsqadmin --lookupd-http-address=127.0.0.1:4161 &
./home/ben/go/src/github.com/nsqio/nsq/apps/nsq_to_file/nsq_to_file --topic=nsq-spark-in --output-dir=/tmp/spark --lookupd-http-address=127.0.01:4161 &
