import streamlit as st
import pandas as pd
import common
import numpy as np


search_map = common.search_box()
sql = f"""select * 
            from TBL_VEH_CNT
            where VEH_CNT_YR like '{search_map['target_year'][0]}' 
            and VEH_CODE like '{search_map['target_veh'][0]}' """

reg_rows = common.getDataFromDb(sql)
area_rows = common.get_area_list()

reg_list  =  []
reg_rows = common.getDataFromDb(sql)
for item in reg_rows:
    reg_list.append({item[3]: item[2]})

area_list = []
area_rows = common.get_area_list()
for item in area_rows:  
    area_list.append({item[0]:item[1]})


reg_map = {}
for item in reg_list: 
    for key, val in item.items(): 
        reg_map[key] = val


result_map = {}
for item in area_list:
    for key, val in item.items(): 
        if key in reg_map:
            result_map[val] = reg_map[key]

if len(result_map) < 1 :
    st.success(f"**조회 결과**가 없습니다")

else :
    reg_data = {
        '지역': [item for item in result_map.keys()],
        '등록 대수': [item for item in result_map.values()]
    }


    reg_df = pd.DataFrame(reg_data)
    sorted_data = reg_df.sort_values(by='등록 대수', ascending=True)

    ## ==================== chart
    title="지역별 자동차 등록 대수"
    labels={"RegionName": "지역", "RegVegNocs": "자동차 등록 대수"}
    st.subheader("지역별 등록 대수 시각화")
    common.make_chart(sorted_data, labels, char_title=title)

    ## ==================== map
    st.subheader("지역별 자동차 등록 대수 지도")
    bins = np.linspace(min(result_map.values()), max(result_map.values()), 8)
    common.make_fmap(reg_df, bins, "자동차 등록 대수")

    st.success(f"**지역별 자동차 등록 대수**를 색상 지도로 표시합니다.")




