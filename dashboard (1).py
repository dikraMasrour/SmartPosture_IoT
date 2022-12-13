import streamlit as st
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
from datetime import datetime
import time 

st.set_page_config(
    page_title="Smart Posture Monitor",
    layout="wide",
)

# TODO get data after backend processing
def get_data() -> pd.DataFrame:
    return pd.read_csv('posture_data.csv', delimiter=',')

df = get_data()


# dashboard title
st.title("Smart Posture Monitor")

#chart 1
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

#chart 2
data = np.random.randn(10, 1)

tab1, tab2 = st.tabs(["Standing data", "Sitting data"])


with tab1:
   r, l = st.columns(2)
   col0, col1, col2, col3= st.columns([1, 2, 2, 2])

   st.header('Your standing stats')
   with l:
      st.date_input('End date')
   with r:
      st.date_input('Start date')
   
   with col1:
      st.metric(label='Standing time', value='35min', delta='good')
   with col2:
      st.metric(label='Good Posture', value='60%', delta='15%')
   with col3:
      st.metric(label='Bad Posture', value='40%', delta='-1%')

   # timestamp to datetime
   datetime_stamp = [datetime.fromtimestamp(ts) for ts in df['timestamp']]
   fig = px.line(df, x=datetime_stamp, y="pitch")
   fig.update_layout(xaxis_title="Time", yaxis_title="Posture pitch")
   st.plotly_chart(fig, use_container_width=True)


with tab2:
   r, l = st.columns(2)
   col0, col1, col2, col3= st.columns([1, 2, 2, 2])

   st.header('Your sitting stats')
   with l:
      st.date_input('End date', key='sit_start')
   with r:
      st.date_input('Start date', key='sit_end')
   with col1:
      st.metric(label='Sitting time', value='1h', delta='too much', delta_color='inverse')
   with col2:
      st.metric(label='Good Posture', value='60%', delta='15%')
   with col3:
      st.metric(label='Bad Posture', value='40%', delta='-1%')


   # timestamp to datetime
   datetime_stamp = [datetime.fromtimestamp(ts) for ts in df['timestamp']]
   fig = px.line(df, x=datetime_stamp, y="pitch")
   fig.update_layout(xaxis_title="Time", yaxis_title="Posture pitch")

   st.plotly_chart(fig, use_container_width=True)


# TODO how to run cold path seperately : implement counter that runs function after x runs
# time.sleep(5)
# st.experimental_rerun()
