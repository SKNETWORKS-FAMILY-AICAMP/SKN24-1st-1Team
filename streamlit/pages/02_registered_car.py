import streamlit as st
import pandas as pd
import plotly.express as px
import common


search_map = common.search_box()


test_data = {
    'area': common.area_list,
    'nocs': [14524, 6001, 10000, 13334, 20001, 26667,  30000, 33334, 40000, 46667, 53334, 60000, 66667, 73334, 80000, 86667, 93334, 99999]
}


df = pd.DataFrame(test_data)
reg_data = df.sort_values(by='nocs', ascending=True)



st.subheader("지역별 등록 대수 시각화")


fig_ev_hybrid = px.bar(
    reg_data,
    x=reg_data.columns.tolist()[0],
    y=reg_data.columns.tolist()[1],
    title="지역별 자동차 등록 대수",
    labels={"RegionName": "지역", "RegVegNocs": "자동차 등록 대수"},
    color=reg_data.columns.tolist()[1],
    color_continuous_scale=px.colors.sequential.Plasma
)
st.plotly_chart(fig_ev_hybrid, use_container_width=True)