import ladybug.analysisperiod as ap
import ladybug.windrose as wr
import ladybug_charts
import plotly.graph_objects as go
import streamlit as st
from ladybug.epw import EPW
#st.set_page_config(layout="wide")
st.header("This Webpage is developed in Python, using the Streamlit, Ladybug library to read EPW, and the Plotly library for visualization")
#st.subheader("这个网页底部增加一个按钮，可以下载12个月风玫瑰图的压缩包"）
#st.subheader("这个网页底部增加一个按钮，可以下载12个月风玫瑰图的压缩包"）
st.write("<span style='font-family:SimHei'>Github link:https://github.com/ymg2007/Streamlit-ladybug-Tools</span>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload EPW file", type="epw")
if uploaded_file is not None:
    data = uploaded_file.getvalue()
    with open("new.epw", "wb") as f:
        f.write(data)
    st.success("File uploaded successfully!")

#epw_file = 'C:\ladybug\zero_radiation5.epw'
epw = EPW("new.epw")

# Python
slider1 = st.slider("Start month", 1, 12,key=1)
i = slider1
slider2 = st.slider("End month", 1, 12,key=2)
j = slider2
month=ap.AnalysisPeriod(st_month=i,end_month=j)
a = epw.wind_direction.filter_by_analysis_period(month)
b = epw.wind_speed.filter_by_analysis_period(month)
windRose= wr.WindRose(a,b,8)
figure = ladybug_charts.to_figure.wind_rose(windRose)
figure.update_layout(title= str(i) +"To"+ str(j))
st.plotly_chart(figure, use_container_width=True)
