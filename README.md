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
