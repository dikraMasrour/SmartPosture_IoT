import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
from datetime import datetime
import time 
import json
import csv
import os


def get_data():
    path_posture = 'posture_data.csv'
    if (os.path.exists(path_posture)):
        with open('posture_data.csv', 'r', newline='') as csvfile:
            posture_df = pd.read_csv(csvfile)
            return posture_df

def good_posture_summary_stats(start='2020-1-1', end='2023-1-1', freq=3):
    posture_df = get_data()
    posture_df['datetime'] = pd.Series([datetime.fromtimestamp(ts) for ts in posture_df['timestamp']])
    posture_df = posture_df.set_index(['datetime'])
    select_posture = posture_df.loc[start:end]['posture']
    return good_posture_prop(select_posture)


def good_posture_prop(selected_df):
    if selected_df.shape[0] > 0:
        return round((sum(selected_df) / selected_df.shape[0]) * 100) 
    else:
        return None


def time_unit(sitting_time):
    if sitting_time <= 60:
        return ('s',sitting_time)
    elif sitting_time > 60:
        return('min',sitting_time//60)
    elif sitting_time > 3600:
        return('h',sitting_time//3600)


def data_filtering(start='2020-1-1', end='2023-1-1', freq=3):
    posture_df = get_data()
    posture_df['datetime'] = pd.Series([datetime.fromtimestamp(ts) for ts in posture_df['timestamp']])
    posture_df = posture_df.set_index(['datetime'])
    select_pitch = posture_df.loc[start:end][['timestamp','score']]
    return select_pitch


def mean_posture_score(start='2020-1-1', end='2023-1-1', freq=3):
    posture_df = get_data()
    posture_df['datetime'] = pd.Series([datetime.fromtimestamp(ts) for ts in posture_df['timestamp']])
    posture_df = posture_df.set_index(['datetime'])
    select_score = posture_df.loc[start:end]['score']
    return mean_score(select_score)

def mean_score(selected_df):
    if selected_df.shape[0] > 0:
        return round(np.mean(selected_df))
    else:
        return None

# print(mean_posture_score())