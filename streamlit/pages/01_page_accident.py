import streamlit as st
import pandas as pd
import common
import numpy as np

search_map = common.search_box()

sql = f"""select * 
            from TBL_ACDNT 
            where ACDNT_YR like '{search_map['target_year'][0]}' 
            and car_code like '{search_map['target_veh'][0]}' """

cnt_list  =  []
cnt_rows = common.getDataFromDb(sql)
for item in cnt_rows:
    cnt_list.append({item[4]: item[3]})

area_list = []
area_rows = common.get_area_list()
for item in area_rows:  
    area_list.append({item[0]:item[1]})


cnt_map = {}
for item in cnt_list: 
    for key, val in item.items(): 
        cnt_map[key] = val


result_map = {}
for item in area_list:
    for key, val in item.items(): 
        if key in cnt_map:
            result_map[val] = cnt_map[key]

if len(result_map) < 1 :
    st.success(f"**조회 결과**가 없습니다")
else :


    data_df = {
        '지역명': result_map.keys(),
        '사고 건수': result_map.values()
    }

    accident_data = pd.DataFrame(data_df)
    
    
    ## ==================== chart
    df = pd.DataFrame(accident_data)
    sorted_data = df.sort_values(by='사고 건수', ascending=True)
    title="지역별 교통사고 건수"
    labels={"RegionName": "지역", "RegVegNocs": "교통사고 건수"}

    st.subheader("지역별 교통사고 건수 차트")
    common.make_chart(sorted_data, labels, char_title=title)


    ## ==================== map
    st.subheader("지역별 교통사고 건수 지도")
    bins = np.linspace(min(result_map.values()), max(result_map.values()), 8)
    common.make_fmap(accident_data, bins, "교통사고 건수")

    st.success(f"**지역별 교통사고 건수**를 색상 지도로 표시합니다.")






