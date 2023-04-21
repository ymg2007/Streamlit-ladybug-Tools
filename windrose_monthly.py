import ladybug.analysisperiod as ap
import ladybug.windrose as wr
import ladybug_charts
import plotly.graph_objects as go
import streamlit as st
from ladybug.epw import EPW
import plotly.io as pio


uploaded_file = st.file_uploader("Upload EPW file", type="epw")
if uploaded_file is not None:
    data = uploaded_file.getvalue()
    with open("new.epw", "wb") as f:
        f.write(data)
    st.success("File uploaded successfully!")
    epw = EPW("new.epw")
 else:
    epw_file = 'CHN_SH_Shanghai.epw'


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
