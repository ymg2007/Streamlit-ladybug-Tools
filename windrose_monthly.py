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

uploaded_file = st.file_uploader("Upload EPW file", type="epw")
if uploaded_file is not None:
    data = uploaded_file.getvalue()
    with open("new.epw", "wb") as f:
        f.write(data)
    st.success("File uploaded successfully!")
    epw = EPW("new.epw")
else:
    epw= epw_file


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
    #保持12个的风玫瑰图   
    pio.write_image(figure, f'{i}.jpg')  
    pio.write_image(figure, f'{i}.pdf')

import os
import shutil
if not os.path.exists('Image'):
    os.makedirs('Image')
if not os.path.exists('PDF'):
    os.makedirs('pdf')
for i in range(1,13):         
    shutil.move(f'{i}.jpg', 'Image/')
    shutil.move(f'{i}.pdf', 'PDF/')
