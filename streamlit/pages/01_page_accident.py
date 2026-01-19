import requests
import streamlit as st
import folium
import pandas as pd
from streamlit_folium import st_folium
import common



search_map = common.search_box()


sql = "select * from TBL_ACDNT"
temp_rows = common.getDataFromDb(sql)


for item in temp_rows :
    print(item)

test_data = {
    'CTY_NM': common.area_list,
    'ACDNT_NOCS': [14524, 6001, 10000, 13334, 20001, 26667, 30001, 33334, 40000, 46667, 53334, 60000, 66667, 73334, 80000, 86667, 93334, 99999]
}
accident_data = pd.DataFrame(test_data)



# api 보내서 우리나라 행정구역 경계 데이터 받아옴
@st.cache_data
def get_geojson_data():
    url = 'https://raw.githubusercontent.com/southkorea/southkorea-maps/master/kostat/2013/json/skorea_provinces_geo_simple.json'
    response = requests.get(url)
    return response.json()
geojson_data = get_geojson_data()


# folium 객체
f_map = folium.Map(
    location=[36.5, 127.5], 
    zoom_start=7,
    max_bounds=[(32, 123), (40, 133)]
)


thresholds = [6000, 12000, 18000, 30000, 50000, 75000, 100000]
folium.Choropleth(
    geo_data=geojson_data, # 지역별 경계선을 나누는 데이터
    data=accident_data, # 지역별 가지고 있는 값
    columns=accident_data.columns.tolist(), # Pandas 데이터프레임에서 사용할 두 개의 열을 지정 (첫 번째 열: 지역 이름 (GeoJSON과 연결할 키) / 두 번째 열: 수치 데이터 (색상으로 표현될 값))
    key_on="feature.properties.name", # geo_data와 data를 묶어주는 공통 기준. (geo_data에서 key_on 값 추출 = data 에서 columns 값 추출) 되도록 맞춰주면 됨
    fill_color="YlOrRd",  # 색상도 더 눈에 띄는 색으로 바꿨음
    fill_opacity=0.7,
    line_opacity=1,
    bins=thresholds,
    legend_name="교통사고 건수",
    reset=True
).add_to(f_map)

st_folium(f_map, width='100%', height=600, returned_objects=[])

st.success(f"**지역별 교통사고 건수**를 색상 지도로 표시합니다.")




