import streamlit as st
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import plotly.graph_objects as go
from datetime import datetime
import time 
import backend


st.set_page_config(
   page_icon= '🤸‍♂️',
   page_title= "Smart Posture Monitor",
   layout="wide",
)

# dashboard title
st.title("🤸‍♂️Smart Posture Monitor")

r, l = st.columns(2)
with l:
   end = st.date_input('End date')
with r:
   start = st.date_input('Start date')

backend.get_data()
df = backend.data_filtering(start, end)
good_pos = backend.good_posture_summary_stats(start, end)
mean_score = backend.mean_posture_score(start, end)


@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(df)


if (good_pos == None):
   st.header('No data for the selected time period. Try again.')



if (good_pos != None):

      col0, col1, col2, col3= st.columns([1, 2, 2, 1])

      good_pos = 70
      with col1:
         if good_pos >= 60:
            st.metric(label='Good Posture', value=str(good_pos) + str('%'), delta='Great, Keep going !')
         else:
            st.metric(label='Good Posture', value=str(good_pos) + str('%'), delta='-You can do better.')
      with col2:
         if mean_score >= 3:
            st.metric(label='Mean posture score', value=str(mean_score), delta="That's good posture !")
         else:
            st.metric(label='Mean posture score', value=str(mean_score), delta='-You can do better.')
      with col3:
         st.write('')
         st.download_button(
         label="Download data for time period as CSV",
         data=csv,
         file_name='posture_data_' + str(start) + '_' + str(end) + '.csv',
         mime='text/csv',

         )
      line, pie = st.columns([3, 1])
      with line:
         # timestamp to datetime
         datetime_stamp = [datetime.fromtimestamp(ts) for ts in df['timestamp']]
         fig = px.line(df, x=datetime_stamp, y="score") # TODO ADD LEGEND FOR SCORE
         fig.update_layout(xaxis_title="Time", yaxis_title="Posture score")
         fig.add_hline(y=3, line_width=2, line_dash="dash", line_color="green")
         fig.add_hline(y=2, line_width=2, line_dash="dash", line_color="red")
         st.plotly_chart(fig, use_container_width=True)
         st.write('Posture scored on a scale of 1-4, 4 begin a great posture')
      with pie:
         fig_pie = go.Figure(data=[go.Pie(labels=['Good posture', 'Bad posture'], values=[good_pos, 100-good_pos], hole=.4)])
         fig = px.pie(values=[good_pos, 100-good_pos], names=['Good posture', 'Bad posture'], hover_name=['Good posture', 'Bad posture'])
         st.plotly_chart(fig_pie, use_container_width=True)



time.sleep(5)
st.experimental_rerun()
