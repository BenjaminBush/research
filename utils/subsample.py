import numpy as np
import pandas as pd 
import random
from datetime import datetime, timedelta
from dateutil import parser

def subsample(dataset, original_granularity, new_granularity):
    df = dataset
    num_buckets = int(original_granularity/new_granularity)

    feature1 = "{} Seconds".format(new_granularity)
    feature2 = "Flow (Veh/{} Seconds)".format(new_granularity)
    cols = [feature1, feature2]
    new_df = pd.DataFrame(columns=cols)
    idx = 0
    for i in range(5):
        start_time = df[i][0]
        target_flow = df[i][1]
        dt = parser.parse(start_time)
        remaining_flow = target_flow
        
        for n in range(num_buckets-1):
            random_flow = random.randint(0, remaining_flow)
            remaining_flow -= random_flow
            td = n*timedelta(seconds=new_granularity)
            time = dt + td 
            data = pd.DataFrame({feature1: time, feature2: random_flow}, index=[idx])            
            new_df = new_df.append({feature1: time, feature2: random_flow}, ignore_index=True)
            idx += 1

        td = (num_buckets)*timedelta(seconds=new_granularity)
        time = dt + td
        random_flow = remaining_flow
        data = pd.DataFrame({feature1: time, feature2: random_flow}, index=[idx])
        new_df = new_df.append(data, ignore_index=True)
        
    return new_df