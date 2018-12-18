(nsqlookupd &) &&
(nsqd --lookupd-tcp-address=127.0.0.1:4160 &) &&
(nsqadmin --lookupd-http-address=127.0.0.1:4161 &) &&
(curl -d 'hello world 1' 'http://127.0.0.1:4151/pub?topic=nsq-spark-in' &) &&
(curl -d 'hello world 1' 'http://127.0.0.1:4151/pub?topic=nsq-spark-out' &) &&
(nsq_to_file --topic=nsq-spark-in --output-dir=/tmp/spark --lookupd-http-address=127.0.0.1:4161 &) 
