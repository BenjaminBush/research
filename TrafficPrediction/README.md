This folder contains code and files related to the development, training, and testing of traffic prediction methods. Although the experiment is primarily concerned with the use of LSTM neural networks for traffic flow prediction, we also evaluate other regression methods. 

# Description of Files
* aggregate_flows.ipynb - Deprecated. Used to aggregate flows across all traffic lanes, but a new version of PeMS does this for you when you download the data. 
* csv_concatenation.ipynb - Concatenates multiple csvs for a single city into one large CSV, which is then split into trainng and testing csvs based on a predefined train/test split.
* csv_concatenation_multiple.ipynb - Same as csv_concatentation.ipynb, but concates aforementioned information across multiple cities/detector locations
* evaluate.py - Main class to evaluate the performance of the neural network
* evaluate_regression.py - Main class to evaluate the performance of other ergression methods
* lstm_model.h5 - Stored weights of a trained LSTM neural network
* metadata.json - Stores metadata related to the architecture of the neural network.
* model.png - Visualization of the LSTM network architecture
* models.py - Defines networks and their hyperparameters. Constructs and compiles the networks
* plotted_preds.png - Visualization of LSTM predictions vs. True Data
* train.py - Main class to train a neural network

# How to Train Neural Network
1. Edit the models.py class to reflect the model architecture and hyperparameters you wish to use. Note that the network is implemented using Keras and Tensorflow. 
2. run `python train.py`

# How to Test Neural Network
1. run `python evaluate.py`
