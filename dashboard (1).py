import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

original_title = '<p style= "font-weight: bold; font-size: 60px; margin-bottom: 50px">Smart Posture</p>'
st.markdown(original_title, unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

standing_title = '<h3 style= "font-weight: bold;">Standing hours</h3>'
standing_hours = '<h5 style= "font-weight: thin; color:#808080; margin-bottom: 50px   ">8 hr</h5>'
sitting_title = '<h3 style= "font-weight: bold;">Sitting hours</h3>'
sitting_hours = '<h5 style= "font-weight: thin; color:#808080; margin-bottom: 50px   ">8 hr</h5>'
g_posture_title = '<h3 style= "font-weight: bold; ">Good Posture</h3>'
g_posture_hours = '<h5 style= "font-weight: thin; color:#808080; margin-bottom: 50px  ">5 hr</h5>'
b_posture_title = '<h3 style= "font-weight: bold; ">Bad Posture</h3>'
b_posture_hours = '<h5 style= "font-weight: thin; color:#808080; margin-bottom: 50px  ">4 hr</h5>'


with col1:
   st.markdown(standing_title, unsafe_allow_html=True)
   st.markdown(standing_hours, unsafe_allow_html=True)
with col2:
   st.markdown(sitting_title, unsafe_allow_html=True)
   st.markdown(sitting_hours, unsafe_allow_html=True)

with col3:
   st.markdown(g_posture_title, unsafe_allow_html=True)
   st.markdown(g_posture_hours, unsafe_allow_html=True)

with col4:
   st.markdown(b_posture_title, unsafe_allow_html=True)
   st.markdown(b_posture_hours, unsafe_allow_html=True)

#chart 1
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

#chart 2
data = np.random.randn(10, 1)

Standing_title = '<h3 style= font-weight: bold; color:Blue; font-size: 15px;">Standing</h3>'
Sitting_title = '<h3 style= font-weight: bold; color:Blue; font-size: 15px;">Sitting</h3>'

tab1, tab2 = st.tabs(["Standing", "Sitting"])

with tab1:
   st.header("Standing")
   st.line_chart(chart_data)

with tab2:
   st.header("Sitting")
   st.line_chart(data)




