This folder contains python scripts used for the experiment. 

# Description of Files
* consumer.py - Creates a KafkaConsumer and subscribes to the output topic. Performs latency calculation.
* producer.py - Deprecated. Used when we only had one detector location. Please see periodic_producer.py 
* periodic_producer.py - Defines a generic periodic producer class. This producer sends records every 100ms. A record includes the detctor flows, average speed, detector location (city), current timestamp (used for latency calculation), and "fake" prediction.
* run_producers.py - Creates a periodic producer for each detector location, pins the producer task to a CPU, and executes.

# How to Run Experiment
1. Start zookeeper
2. Start a kafka broker
3. Start the consumer
`python consumer.py`
4. Start the Flink Application (see <https://github.com/BenjaminBush/flinkits>)
5. Start the producers
`python run_producers.py`
