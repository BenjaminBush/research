from kafka import KafkaProducer
from kafka.errors import KafkaError
import pandas as pd
import numpy as np
import rdtscp_module
import time
import random
import re

class PeriodicProducer(object):
    def __init__(self, test_file, max_messages=20000, random_sleep=0, bootstrap_servers='localhost:9092'):
        self.test_file = test_file
        self.max_messages = max_messages
        self.random_sleep = random_sleep

        self.df = pd.read_csv(self.test_file, encoding='utf-8').fillna(0)
        self.df = np.array(self.df)

        self.length = 2000
        self.index = 0
        self.lag = 12
        self.messages_sent = 0

        self.pattern = re.compile(r"../data/(?P<city>[a-zA-Z]+?)/(?P<test_file>[a-zA-Z0-9 ]+?).csv")
        self.m = self.pattern.search(self.test_file)
        if self.m:
            self.city = self.m.group('city')
        else:
            self.city = 'el_segundo'
        # try:
        #     self.city = self.m.group('city')
        # except AttributeError as e:
        #     print(self.test_file)
        #     raise e
        # Kafka setup
        self.producer = KafkaProducer(bootstrap_servers=[bootstrap_servers])
        self.topic = str(self.city) + "-input"    


        self.sleep_times = []
        if self.random_sleep:
            self.sleep_times = np.loadtxt('../sleep/random_sleep_times.txt').tolist()
        else:
            self.sleep_times = np.loadtxt('../sleep/uniform_sleep_times.txt').tolist()

    def run(self):
        while self.messages_sent < self.max_messages:
            # Collect flows from dataframe
            data = self.df[self.index:self.index+self.lag]
            flows = data[:,2]

            # Create the message
            message = ';'.join(str(flow) for flow in flows)

            fake_prediction = ";" + str(0)
            message += fake_prediction

            # Timestamp for latency
            ns = rdtscp_module.rdtscp()

            # Add timestamp to message
            ns_data = ';'+str(ns)
            message += ns_data

            self.producer.send(self.topic, value=str.encode(message))
            self.producer.flush()

            # Introduce periodic behavior by sleeping  after producing message
            time.sleep(self.sleep_times[self.index])
            
            # Increment index
            self.index += 1
            if self.index >= 2000:
                self.index = 0





