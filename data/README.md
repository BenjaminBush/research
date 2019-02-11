This folder contains the PeMS data from 6 detector locations in Southern California. Data were downloaded from each detector location for the entire month of March 2018 at 5 minute granularity. Data is stored as CSV files, and the original downloads are the "pems_output_x.xlsx" files (where x is an integer 0 <= x <= 4). Data collected includes traffic flow measurements and average speed, which is used for the heuristic in A* search. 

We used the `TrafficPrediction/csv_concatenate_multiple.ipynb` script to concatenate each of these files into a large dataframe, which we then split into training and testing data. 

For more information, please visit: http://pems.dot.ca.gov/
