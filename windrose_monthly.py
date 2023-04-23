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
st.write("<span style='font-family:SimHei'>这个网页底部增加一个按钮，可以下载12个月风玫瑰图的压缩包</span>", unsafe_allow_html=True)
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

uploaded_file = st.file_uploader("请上传EPW气象数据文件", type="epw")
if uploaded_file is not None:
    data = uploaded_file.getvalue()
    with open("new.epw", "wb") as f:
        f.write(data)
    st.success("File uploaded successfully!")
    epw = EPW("new.epw")
else:
    epw= EPW(epw_file)


# Python
for i in range(1,13):
    month=ap.AnalysisPeriod(st_month=i,end_month=i)
    a = epw.wind_direction.filter_by_analysis_period(month)
    b = epw.wind_speed.filter_by_analysis_period(month)
    windRose= wr.WindRose(a,b,8)
    figure = ladybug_charts.to_figure.wind_rose(windRose)
    figure.update_layout(title= str(i) +"月风玫瑰图")
    #显示12个月的风玫瑰图
    st.plotly_chart(figure, use_container_width=True)
    #保存12个月的风玫瑰图   
    pio.write_image(figure, f'{i}.jpg')  
    pio.write_image(figure, f'{i}.pdf')

#增加下载所有图片的功能
import os
import streamlit as st
from zipfile import ZipFile
import base64
# 获取当前目录下所有jpg文件
jpg_files = [f for f in os.listdir('.') if f.endswith('.jpg')]

# 打包为zip文件
with ZipFile('image.zip', 'w') as zip:
    for file in jpg_files:
        zip.write(file)

# 在streamlit中增加一个按钮，用来下载image.zip
with open('image.zip', 'rb') as f:
    bytes = f.read()
    b64 = base64.b64encode(bytes).decode()
    href = f'<a href="data:file/zip;base64,{b64}" download="image.zip">下载12个月风玫瑰图压缩包</a>'
    st.markdown(href, unsafe_allow_html=True)
