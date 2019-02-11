# Benjamin Bush Master's Project Central Repository
This repository contains code related to the following
* Neural Network Training and Testing (for Traffic Flow Prediction)
* Evaluating Performance of Other Regression Methods
* Traffic Flow Data Collected from PeMS
* Producing and Consuming Records to/from Kafka
* Experimental Results

## Neural Network Training and Testing
All code related to the LSTM network is in the `TrafficPrediction` folder.

## Evaluating Performance of Other Regression Methods
Performed by `evaluate_regression.py` in the `TrafficPrediction` folder.

## Traffic Flow Data Collected from PeMS
Contained in the `data` folder

## Producing and Consuming Records to/from Kafka
Relevant code is located in `kafka_scripts`

## Results
All latencies and corresponding analysis are located in the `results` folder


*Please visit each of these folders and see their README for more information. We will provide brief overviews for the folders not listed above. Note that the following folders are either no longer useful to this experiment, or only contain helper code.*

## Other Files/Folders

### images
Stores images that are helpful visualiziations of the neural net/system architecture

### nsq_scripts
This folder is deprecated. A previous version of the experiments used NSQ instead of Kafka, and these escripts contained the NSQ equivalents of what is located in the `kafka_scripts` folder. They may be used as reference, but should be updated should you wish to use them in an experimental setting

### old_data
Contains data pertaining to detector locations that were not used in the later versions of the experiment

### report
Contains LaTeX for the written report

### sleep
Helper functions to generate periodic workloads

### utils
Random collection of utility functions



