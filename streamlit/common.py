import streamlit as st
import streamlit_antd_components as sac
import mysql.connector
import folium
import requests
from streamlit_folium import st_folium
import plotly.express as px


## ==================== database =================================
def getDataFromDb(sql="") :
    if sql == "":
        print("sql을 입력해주세요")
        pass
    connection = mysql.connector.connect(
        host="localhost",    # 연결한 db 주소
        user="ohgiraffers", # 사용자 이름
        password="ohgiraffers", # 사용자 비밀번호
        database="roadkeeperdb"   # 사용할 DB
    )   
    result = [];
    if connection.is_connected() :
        cursor = connection.cursor()
        cursor.execute(sql)
        result_rows = cursor.fetchall()
        for row in result_rows :
            result.append(row)
        cursor.close()
    connection.close()
    return result;



## ==================== 차종 목록 =================================
def get_car_list():
        try :
            car_rows = getDataFromDb("select * from tbl_veh_type")
            # area_list = [x[1] for x in car_rows]
            return car_rows
        except :
            return [(1, "승용"), (2, "승합"), (3, "화물"), (4, "특수")]

## ==================== 지역 목록 =================================
def get_area_list():
    try :
        area_rows = getDataFromDb("select * from TBL_CTY")
        # area_list = [x[1] for x in area_rows]
        return area_rows
    except :
        return ['제주특별자치도', '경상남도', '경상북도', '전라남도', '전라북도', '충청남도', '충청북도', '강원도', '경기도', '세종특별자치시', '울산광역시', '대전광역시', '광주광역시', '인천광역시', '대구광역시', '부산광역시', '서울특별시']
    # area_list = ['제주특별자치도', '경상남도', '경상북도', '전라남도', '전라북도', '충청남도', '충청북도', '강원도', '경기도', '세종특별자치시', '울산광역시', '대전광역시', '광주광역시', '인천광역시', '대구광역시', '부산광역시', '서울특별시']
    # 제주특별자치도
    # 경상남도
    # 경상북도
    # 전라남도
    # 전라북도
    # 충청남도
    # 충청북도
    # 강원도
    # 경기도
    # 세종특별자치시
    # 울산광역시
    # 대전광역시
    # 광주광역시
    # 인천광역시
    # 대구광역시
    # 부산광역시
    # 서울특별시


## ==================== 조회 조건 =================================
def search_box() :
        
    # 3개의 컬럼 생성
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        target_year = st.selectbox(
            "대상 년도",
            options=[(2020, "2020"),(2021, "2021"),(2022, "2022"),(2023, "2023"),(2024, "2024")],
            format_func=lambda x:x[1]
        )

    with col2:
        # 체크박스 있는 select
        target_area = sac.cascader(
            label='대상 지역',
            placeholder='지역 선택',
            items=[{"label": name, "value": code} for code, name in get_area_list()],
            multiple=True,      # 드롭박스 안에서 다중 선택(체크박스) 활성화
            clear=True,
        )
        # 기본 다중 select 
        # target_area = st.multiselect(
        #     "대상 지역",
        #     ["제주특별자치도", "경상남도", "경상북도", "전라남도", "전라북도", "충청남도", "충청북도", "강원도", "경기도", "세종특별자치시", "울산광역시", "대전광역시", "광주광역시", "인천광역시", "대구광역시", "부산광역시", "서울특별시"],
        #     ["서울특별시"] # 기본값으로 선택되어 있을 항목 (선택 사항)
        # )
        
    with col3:
        target_veh = st.selectbox(
            "차종",
            get_car_list(),
            format_func=lambda x:x[1]
        )

    with col4:
        st.write("검색 실행")
        isBtn = st.button("조회")

    return {'target_year': target_year, 'target_area': target_area, 'target_veh': target_veh, 'is_btn': isBtn}





## ==================== 지도 =================================
# api 보내서 우리나라 행정구역 경계 데이터 받아옴
@st.cache_data
def get_geojson_data():
    url = 'https://raw.githubusercontent.com/southkorea/southkorea-maps/master/kostat/2013/json/skorea_provinces_geo_simple.json'
    response = requests.get(url)
    return response.json()
geojson_data = get_geojson_data()



def make_fmap(data_df, bins=[], geo_title=""):
    # folium 객체
    f_map = folium.Map(
        location=[36.5, 127.5], 
        zoom_start=7,
        max_bounds=[(32, 123), (40, 133)]
    )

    folium.Choropleth(
        geo_data=geojson_data, # 지역별 경계선을 나누는 데이터
        data=data_df, # 지역별 가지고 있는 값
        columns=data_df.columns.tolist(), # Pandas 데이터프레임에서 사용할 두 개의 열을 지정 (첫 번째 열: 지역 이름 (GeoJSON과 연결할 키) / 두 번째 열: 수치 데이터 (색상으로 표현될 값))
        key_on="feature.properties.name", # geo_data와 data를 묶어주는 공통 기준. (geo_data에서 key_on 값 추출 = data 에서 columns 값 추출) 되도록 맞춰주면 됨
        fill_color="YlOrRd",  # 색상도 더 눈에 띄는 색으로 바꿨음
        fill_opacity=0.7,
        line_opacity=1,
        bins=bins,
        legend_name=geo_title,
        reset=True
    ).add_to(f_map)

    st_folium(f_map, width='100%', height=600, returned_objects=[])



## ==================== 차트 =================================
def make_chart(data_df, labels, char_title=""): 
    bar_chart = px.bar(
        data_df,
        x=data_df.columns.tolist()[0],
        y=data_df.columns.tolist()[1],
        title=char_title,
        labels=labels,
        color=data_df.columns.tolist()[1],
        color_continuous_scale=px.colors.sequential.Plasma
    )
    st.plotly_chart(bar_chart, use_container_width=True)