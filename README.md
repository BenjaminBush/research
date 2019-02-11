# Benjamin Bush Master's Project Central Repository
This repository contains code related to the following
* Neural Network Training and Testing (for Traffic Flow Prediction)
* Evaluating Performance of Other Regression Methods
* Traffic Flow Data Collected from PeMS
* Producing and consuming records to/from Kafka

## Neural Network Training and Testing
All code related to the LSTM network is in the `TrafficPrediction` folder. Important files in here are:
* csv_concatentation_multiple.ipynb

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Concatenates data from multiple PeMS csv files into a large CSV for training/testing
* evaluate.py

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Evaluates the performance of the trained neural network</p>
* lstm_model.h5

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Stored model of the neural network
* models.py

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Defines models and hyperparameters
* train.py

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Main driver for executing neural network training


# Centralized repository for Master's Thesis Development

TrafficLSTM folder contains the source code for developing a 2-layer LSTM network for traffic prediction.

Network Architecture:


![No picture found](https://raw.githubusercontent.com/BenjaminBush/research/master/TrafficPrediction/model.png)

Predictions vs. True flow on sample day:
![No picture found](https://raw.githubusercontent.com/BenjaminBush/research/master/TrafficPrediction/plotted_preds.png)

datasample.(go/py) are scripts that will publish test data to an NSQ broker at a given time interval for simulation

See https://github.com/BenjaminBush/nsq-spark-receiver for a Spark Streaming implementation of an NSQ Receiver

Must change taskmanager.numberOfTaskSlots in flink.conf to be the same as the number of VCPUs
  - problem: need 1 for each job, yielding 8 vcpus, but do we really need this many?
