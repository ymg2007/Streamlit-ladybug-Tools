import ladybug.analysisperiod as ap
import ladybug.windrose as wr
import ladybug_charts
import plotly.graph_objects as go
import streamlit as st
from ladybug.epw import EPW
import plotly.io as pio
import requests
import zipfile
import os
# -*- coding: utf-8 -*-
st.header("这个小程序是用Python开发的，用的是Streamlit网页框架，Ladybug库读取epw气象数据，Plotly库进行可视化")
st.write("<span style='font-family:SimHei'>开源代码仓库https://github.com/ymg2007/Streamlit-ladybug-Tools</span>", unsafe_allow_html=True)

url = "https://climate.onebuilding.org/WMO_Region_2_Asia/CHN_China/AH_Anhui/CHN_AH_Anqing.584240_CSWD.zip"
response = requests.get(url)

# Save the downloaded file
zip_file_path = "CHN_AH_Anqing.584240_CSWD.zip"
with open(zip_file_path, "wb") as file:
    file.write(response.content)

# Unzip the file
with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
    zip_ref.extractall("")

# Find the EPW file in the extracted directory
epw_file = None
for file in os.listdir():
    if file.endswith(".epw"):
        epw_file = file
        break

if epw_file:
    print(f"EPW file found: {epw_file}")
else:
    print("No EPW file found.")
    
# 使用侧边栏，提供2种选择
add_selectbox = st.sidebar.selectbox(
    "请选择一种生成风玫瑰图的方式",
    ("自定义起止月份", "一键生成12个月")
)

if add_selectbox == "一键生成12个月":
    st.write("<span style='font-family:SimHei'>这个网页底部增加一个按钮，可以下载12个月风玫瑰图的压缩包</span>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("请上传EPW气象数据文件", type="epw")
    if uploaded_file is not None:
        data = uploaded_file.getvalue()
        with open("new.epw", "wb") as f:
            f.write(data)
        st.success("File uploaded successfully!")
        epw = EPW("new.epw")
    else:
        epw= EPW(epw_file)

    #st.radio('生成全年风玫瑰图')
    # code for functionality 1
    for i in range(1,13):
        month=ap.AnalysisPeriod(st_month=i,end_month=i)
        a = epw.wind_direction.filter_by_analysis_period(month)
        b = epw.wind_speed.filter_by_analysis_period(month)
        windRose= wr.WindRose(a,b,8)
        figure = ladybug_charts.to_figure.wind_rose(windRose)
        figure.update_layout(title= str(i) +"月风玫瑰图")
        #显示12个月的风玫瑰图
        st.plotly_chart(figure, use_container_width=True)
        #保持12个的风玫瑰图   
        pio.write_image(figure, f'{i}.jpg')  

if add_selectbox == "自定义起止月份":
    uploaded_file = st.file_uploader("请上传EPW气象数据文件", type="epw")
    if uploaded_file is not None:
        data = uploaded_file.getvalue()
        with open("new.epw", "wb") as f:
            f.write(data)
        st.success("File uploaded successfully!")
        epw = EPW("new.epw")
    else:
        epw= EPW(epw_file)
    #st.radio('生成全年风玫瑰图')
    # Python
    slider1 = st.slider("起始月份", 1, 12,key=1)
    i = slider1
    slider2 = st.slider("终止月份", 1, 12,key=2)
    j = slider2
    month=ap.AnalysisPeriod(st_month=i,end_month=j)
    a = epw.wind_direction.filter_by_analysis_period(month)
    b = epw.wind_speed.filter_by_analysis_period(month)
    windRose= wr.WindRose(a,b,8)
    figure = ladybug_charts.to_figure.wind_rose(windRose)
    if i >j:
        case1 = str(i)+"月"+"至次年"+ str(j)+"月"
        figure.update_layout(title= case1)
    else:
        case2 = str(i)+"月"+"至"+ str(j)+"月"
        figure.update_layout(title= case2)
    st.plotly_chart(figure, use_container_width=True)
