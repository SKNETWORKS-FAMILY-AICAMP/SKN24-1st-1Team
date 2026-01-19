import requests
import pandas as pd


# 도시코드 mapping dict
CITY_CODE = {
    "서울": 11, "부산": 21, "대구": 22, "인천": 23, "광주": 24,
    "대전": 25, "울산": 26, "세종": 29, "경기": 31, "강원": 32,
    "충북": 33, "충남": 34, "전북": 35, "전남": 36,
    "경북": 37, "경남": 38, "제주": 39
}

# 차종코드 mapping dict
VEHICLE_CODE = {
    "Total": 0,
    "승용": 1,
    "승합": 2,
    "화물": 3,
    "특수": 4
}

url = "https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=NDZjZmZhZTEzNzhiYzgwMjU4YmMxZjdiNTI0MmUwZmM=&itmId=13103873443T4+&objL1=ALL&objL2=13102873443B.0001+&objL3=ALL&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=M&startPrdDe=202001&endPrdDe=202412&orgId=116&tblId=DT_MLTM_5498"

# API 요청
response = requests.get(url)

# 결과 출력
if response.status_code == 200:
    # for i in range(len(response.json())):
    #     # print(response.json()[i])
    #     print(type(response.json()[i]))
    print("Status code is :", response.status_code)
    
else:
    print(f"Error: {response.status_code}")



# 받는 데이터 형식
# 년월 = PRD_DE, 
# 시도명 = C1_NM_ENG, 
# 차종&총계 = C3_NM_ENG, C3_NM
# 계 = DT 각 월&지역별로 승용, 승합, 화물, 특수, 총계 총 5개의 계가 각각 있음

# 우리의 데이터 형식 (VEH_CNT)
# (CODE), YR, NOCS, CTY_CODE, VEH_CODE 로 구성

df = pd.DataFrame(response.json())
df = df[["PRD_DE", "C1_NM", "C3_NM", "DT"]] # 원하는 4개의 항목만 고르기

# 항목이름을 알아보기 쉽게 바꾸기
df = df.rename(columns={
    "PRD_DE": "yyyymm",
    "C1_NM": "region",
    "C3_NM": "vehicle",
    "DT": "count"
})
df = df[df["vehicle"] != "총계"]    # 총계는 필요 없으니 제외

# print(df)

# 년도와 계를 str 에서 int 로 형변환
df["year"] = df["yyyymm"].str[:4].astype(int)
df["count"] = df["count"].astype(int)

# yyyymm 은 이제 필요없으니 버리기
df = df.drop(columns=["yyyymm"])


# yyyy 형식 data frame 만들기
yearly_df = (
    df
    .groupby(["year", "region", "vehicle"], as_index=False)
    .agg({"count": "mean"})     # 평균으로 구하는게 포인트
)

# print(yearly_df)
# print(type(yearly_df))


# DB에 넣을 형태(튜플)로 만들어주기

insert_rows = []

for _, row in yearly_df.iterrows():
    insert_rows.append((
        int(row["year"]),                         # YR
        CITY_CODE[row["region"]],                 # CTY_CODE
        VEHICLE_CODE[row["vehicle"]],             # VEH_CODE
        int(row["count"])                         # CNT
    ))

# print(insert_rows[130:134])     # 확인용 코드


# SQL 구문 사용하여 DB에 추가

import mysql.connector

connection = mysql.connector.connect(
    host = 'localhost',         # MySQL 서버 주소 (ip)
    user = 'ohgiraffers',       # 사용자 이름
    password = 'ohgiraffers',   # 비밀번호
    database = 'roadkeeperdb'         # 사용할 DB 스키마
)

cursor = connection.cursor()

sql = """
INSERT INTO TBL_VEH_CNT (VEH_CNT_YR, CTY_CODE, VEH_CODE, VEH_CNT_NOCS)
VALUES (%s, %s, %s, %s)
"""

cursor.executemany(sql, insert_rows)
connection.commit()

print(f"@@@ {cursor.rowcount}개의 행 삽입 완료 @@@")

cursor.close()
connection.close()

    









    



