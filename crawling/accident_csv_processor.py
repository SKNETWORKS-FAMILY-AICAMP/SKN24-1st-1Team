import pandas as pd
import mysql.connector

# MultiIndex 컬럼을 단일 문자열 컬럼명으로 변환
def flatten_columns(columns):
    new_cols = []
    for col in columns:
        if col[0] == col[1] or col[1] == '':
            new_cols.append(col[0])
        else:
            new_cols.append(f"{col[0]}_{col[1]}")
    return new_cols

# 사고 지표명 매핑
ACDNT_TYPE_MAP = {
    '사고[건]': '사고',
    '사망[명]': '사망',
    '부상[명]': '부상',
    '(중상자[명])': '중상'
}

# 코드 매핑 딕셔너리
CITY_CODE_MAP = {
    '전국': 0, '서울특별시': 11, '부산광역시': 21, '대구광역시': 22, '인천광역시': 23,
    '광주광역시': 24, '대전광역시': 25, '울산광역시': 26, '세종특별자치시': 29, '경기도': 31,
    '강원도': 32, '충청북도': 33, '충청남도': 34, '전라북도': 35, '전라남도': 36,
    '경상북도': 37, '경상남도': 38, '제주특별자치도': 39
}

CAR_CODE_MAP = {'승용': 1, '승합': 2, '화물': 3, '특수': 4}

csv_path = 'accident.csv'
DB_CONFIG = {
    'host': 'localhost',
    'user': 'ohgiraffers',
    'password': 'ohgiraffers',
    'database': 'roadkeeperdb',
    'charset': 'utf8mb4'
}

# CSV 파일 읽기 및 컬럼명 변환
df = pd.read_csv(csv_path, header=[0,1], encoding='utf-8')
df.columns = flatten_columns(df.columns)

# 긴 형식(long format) 변환 ('시도'와 '연도'를 고유 식별자로 사용)
# '합계' 컬럼 제거
if '합계' in df.columns:
    df.drop(columns=['합계'], inplace=True)

id_vars = ['시도', '연도']
value_vars = [col for col in df.columns if col not in id_vars and '_' in col]
df_long = df.melt(id_vars=id_vars, value_vars=value_vars,
                  var_name='연도_차종_그룹', value_name='사고_수치_값')

df_long[['ACDNT_YR_RAW', 'CAR_TYPE_RAW']] = df_long['연도_차종_그룹'].str.split('_', expand=True)

df_long = df_long.drop(columns=['연도_차종_그룹'])


df_long['ACDNT_YR'] = pd.to_numeric(df_long['ACDNT_YR_RAW'], errors='coerce')
df_long.dropna(subset=['ACDNT_YR'], inplace=True)
df_long['ACDNT_YR'] = df_long['ACDNT_YR'].astype(int)


df_long['사고_수치_값'] = df_long['사고_수치_값'].astype(str).str.replace(',', '')
df_long['사고_수치_값'] = pd.to_numeric(df_long['사고_수치_값'], errors='coerce')


df_long.dropna(subset=['사고_수치_값'], inplace=True)


# '시도' 컬럼에서 지역명 추출 (ffill 적용)
df_long['지역명'] = df_long['시도'].ffill()


# '연도' 컬럼에서 사고 유형 추출 
df_long['ACDNT_TYPE_RAW'] = df_long['연도'].apply(lambda x: x if x in ACDNT_TYPE_MAP else None)

# 불필요한 행 필터링
df_final = df_long[
    df_long['지역명'].notna() &
    df_long['ACDNT_TYPE_RAW'].notna() &
    (df_long['CAR_TYPE_RAW'] != '합계')
].copy()

# ACDNT_TYPE (최종 이름) 매핑
df_final['ACDNT_TYPE'] = df_final['ACDNT_TYPE_RAW'].map(ACDNT_TYPE_MAP)
df_final.dropna(subset=['ACDNT_TYPE'], inplace=True)


# ACDNT_NOCS (사고 수치) 설정
df_final['ACDNT_NOCS'] = df_final['사고_수치_값'].astype(int)

df_final = df_final[df_final['ACDNT_NOCS'] > 0].copy()


# 지역명, 차종명 → 코드 매핑
df_final['지역명'] = df_final['지역명'].astype(str).str.strip()
region_short_to_full = {
    '서울': '서울특별시', '부산': '부산광역시', '대구': '대구광역시', '인천': '인천광역시',
    '광주': '광주광역시', '대전': '대전광역시', '울산': '울산광역시', '세종': '세종특별자치시',
    '경기': '경기도', '강원': '강원도', '충북': '충청북도', '충남': '충청남도',
    '전북': '전라북도', '전남': '전라남도', '경북': '경상북도', '경남': '경상남도',
    '제주': '제주특별자치도',
    '합계': '전국'
}
df_final['지역명'] = df_final['지역명'].replace(region_short_to_full)


df_final['CAR_TYPE_RAW_CLEAN'] = df_final['CAR_TYPE_RAW'].astype(str).str.replace('차', '').str.strip()



df_final['CTY_CODE'] = df_final['지역명'].map(CITY_CODE_MAP)
df_final['CAR_CODE'] = df_final['CAR_TYPE_RAW_CLEAN'].map(CAR_CODE_MAP)

#  데이터 필터링
df_final.dropna(subset=['CTY_CODE', 'CAR_CODE', 'ACDNT_TYPE', 'ACDNT_NOCS'], inplace=True)

df_final['CTY_CODE'] = df_final['CTY_CODE'].astype(int)
df_final['CAR_CODE'] = df_final['CAR_CODE'].astype(int)

# ACDNT_CODE 생성
df_final = df_final.reset_index(drop=True)
df_final['ACDNT_CODE'] = df_final.index + 1


# 컬럼 순서 및 이름에 맞게 최종 데이터프레임 구성
df_to_db = df_final[['ACDNT_CODE', 'ACDNT_YR', 'ACDNT_TYPE', 'ACDNT_NOCS', 'CTY_CODE', 'CAR_CODE']]

# MySQL DB 연결 및 쿼리
conn = None
cursor = None

try:
    if df_to_db.empty:
        print("Empty DataFrame")
    else:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("DB 연결 성공!")

        insert_query = """
        INSERT INTO TBL_ACDNT (ACDNT_CODE, ACDNT_YR, ACDNT_TYPE, ACDNT_NOCS, CTY_CODE, CAR_CODE)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        data_to_insert = [tuple(row) for row in df_to_db.values]
        cursor.executemany(insert_query, data_to_insert)

        conn.commit()

except mysql.connector.Error as err:
    print(f"데이터베이스 오류 발생: {err}")
    if conn:
        conn.rollback()
        print("트랜잭션이 롤백되었습니다.")

except Exception as e:
    print(f"알 수 없는 오류 발생: {e}")
    if conn:
        conn.rollback()
        print("트랜잭션이 롤백되었습니다.")

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()