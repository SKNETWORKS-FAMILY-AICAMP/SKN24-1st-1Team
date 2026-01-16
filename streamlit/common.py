import streamlit as st
import streamlit_antd_components as sac
import mysql.connector



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



area_rows = getDataFromDb("select * from TBL_CTY")
area_list = [x[1] for x in area_rows]


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


def search_box() :
        
    # 3개의 컬럼 생성
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        target_year = st.selectbox(
            "대상 년도",
            (2020,2021,2022,2023,2024)
        )

    with col2:
        # 체크박스 있는 select
        target_area = sac.cascader(
            label='대상 지역',
            placeholder='지역 선택',
            items=area_list,
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
            ("승용","승합","화물", "특수")
        )

    with col4:
        st.write("검색 실행")
        isBtn = st.button("조회")

    return {'target_year': target_year, 'target_area': target_area, 'target_veh': target_veh, 'is_btn': isBtn}

