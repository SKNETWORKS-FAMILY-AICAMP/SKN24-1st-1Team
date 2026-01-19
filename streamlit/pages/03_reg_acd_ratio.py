import streamlit as st
import pandas as pd
import common
import numpy as np


search_map = common.search_box()
sql_reg = f"""select * 
            from TBL_VEH_CNT
            where VEH_CNT_YR like '{search_map['target_year'][0]}' 
            and VEH_CODE like '{search_map['target_veh'][0]}' """

sql_acd = f"""select * 
            from TBL_ACDNT 
            where ACDNT_YR like '{search_map['target_year'][0]}' 
            and car_code like '{search_map['target_veh'][0]}' """


area_rows = common.get_area_list()
reg_rows = common.getDataFromDb(sql_reg)
acd_rows = common.getDataFromDb(sql_acd)


area_list = []
for item in area_rows:  
    area_list.append({item[0]:item[1]})
reg_map = {};
for item in reg_rows:
    reg_map[item[3]] = item[2]
acd_list  =  []
for item in acd_rows:
    acd_list.append({item[4]: item[3]})


ratio_map = {}
for acd_item in acd_list: 
    for key, acd_val in acd_item.items(): 
        if key in reg_map.keys():
            ratio_map[key] = (int(acd_val) / int(reg_map[key]))* 100


if len(ratio_map) < 1 :
    st.success(f"**조회 결과**가 없습니다")

else :
    result_map = {}
    for item in area_list:
        for key, val in item.items(): 
            if key in ratio_map:
                result_map[val] = ratio_map[key]


    column_name = "등록 대수 대비 사고 건수"
    reg_data = {
        '지역': [item for item in result_map.keys()],
        column_name: [item for item in result_map.values()]
    }


    reg_df = pd.DataFrame(reg_data)
    sorted_data = reg_df.sort_values(by=column_name, ascending=True)

    ## ==================== chart
    title="지역별 자동차 등록 대수 대비 사고 건수"
    labels={"RegionName": "지역", "RegVegNocs": column_name}
    st.subheader(column_name + " 차트")
    common.make_chart(sorted_data, labels, char_title=title)

    ## ==================== map
    st.subheader(column_name + " 지도")
    bins = np.linspace(min(result_map.values()), max(result_map.values()), 8)
    common.make_fmap(reg_df, bins, column_name)

    st.success(f"**{column_name}**를 색상 지도로 표시합니다.")




