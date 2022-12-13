import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
from datetime import datetime
import time 
import json
import csv
import os

# TAKE DATE RANGE AS PARAM


def summary_stats(start, end):
    path_posture = 'posture_data.csv'
    path_sitting = 'sitting_standing_data.csv'


    if (os.path.exists(path_posture)):
        with open('posture_data.csv', 'r', newline='') as csvfile:
            posture_df = pd.read_csv(csvfile)

    if (os.path.exists(path_sitting)):
        with open('sitting_standing_data.csv', 'r', newline='') as csvfile:
            sitting_df = pd.read_csv(csvfile)

    posture_df['datetime'] = pd.Series([datetime.fromtimestamp(ts) for ts in posture_df['timestamp']])
    sitting_df['datetime'] = pd.Series([datetime.fromtimestamp(ts) for ts in sitting_df['timestamp']])

    posture_df = posture_df.set_index(['datetime'])
    sitting_df = sitting_df.set_index(['datetime'])

    select_posture = posture_df.loc[start:end]['posture']
    select_sitting = sitting_df.loc[start:end]['State']

    print(sitting_time(select_sitting))
    # print(good_posture_prop(select_posture), '%')


def good_posture_prop(selected_df):
    print(sum(selected_df), selected_df.shape[0])
    return round((sum(selected_df) / selected_df.shape[0]) * 100) 

def sitting_time(selected_df):
    (selected_df.index[-1] - selected_df.index[0]).seconds

summary_stats('2020-1-1', '2022-12-30')