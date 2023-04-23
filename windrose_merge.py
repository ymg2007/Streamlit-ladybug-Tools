import ladybug.analysisperiod as ap
import ladybug.windrose as wr
import ladybug_charts
import plotly.graph_objects as go
import streamlit as st
from ladybug.epw import EPW
import plotly.io as pio

# 使用侧边栏，提供2种选择
add_selectbox = st.sidebar.selectbox(
    "请选择一种生成风玫瑰图的方式",
    ("自定义起止月份", "一键生成12个月")
)

if add_selectbox == "自定义起止月份":
    uploaded_file = st.file_uploader("Upload EPW file", type="epw")
    if uploaded_file is not None:
        data = uploaded_file.getvalue()
        with open("new.epw", "wb") as f:
            f.write(data)
        st.success("File uploaded successfully!")
        epw = EPW("new.epw")
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

if add_selectbox == "一键生成12个月":
    uploaded_file = st.file_uploader("Upload EPW file", type="epw")
    if uploaded_file is not None:
        data = uploaded_file.getvalue()
        with open("new.epw", "wb") as f:
            f.write(data)
        st.success("File uploaded successfully!")
        epw = EPW("new.epw")
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