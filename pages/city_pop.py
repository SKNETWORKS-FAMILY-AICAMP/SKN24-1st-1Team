import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from sql import cty_pop_sql

st.set_page_config(page_title="RoadKeeper - 도시 인구", layout="wide")

# 한글 깨짐 방지 (matplotlib)
def set_korean_font():
    plt.rcParams["font.family"] = "Malgun Gothic"
    plt.rcParams["axes.unicode_minus"] = False  # 마이너스 깨짐 방지

set_korean_font()

# =========================
# 필터용 데이터 조회
# =========================
@st.cache_data(ttl=60)
def fetch_year_list():
    conn, cur = cty_pop_sql.connect_db()
    cur.execute("SELECT DISTINCT CTY_POP_YR FROM tbl_cty_pop ORDER BY CTY_POP_YR;")
    years = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return years

@st.cache_data(ttl=60)
def fetch_city_list():
    conn, cur = cty_pop_sql.connect_db()
    cur.execute("SELECT CTY_CODE, CTY_NM FROM tbl_cty ORDER BY CTY_NM;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows  # list[tuple(code, name)]

st.title("📊 연도별 도시 인구수")

years = fetch_year_list()
cities = fetch_city_list()

if "df" not in st.session_state:
    latest_year = max(years)
    all_city_codes = [code for code, _ in cities]
    rows = cty_pop_sql.select_cty_pop(
        year=latest_year,
        cty_codes=all_city_codes
    )
    st.session_state.df = pd.DataFrame(
        rows, columns=["CTY_NM", "CTY_POP_YR", "CTY_POP"]
    )

# --- UI ---
col1, col2, col3 = st.columns([2, 6, 2])

with col1:
    selected_year = st.selectbox("연도", years, index=len(years)-1 if years else 0)

with col2:
    st.caption("지역 선택")
    selected_codes = []
    grid = st.columns(5)
    for i, (code, name) in enumerate(cities):
        with grid[i % 5]:
            if st.checkbox(name, key=f"cty_{code}"):
                selected_codes.append(int(code))

with col3:
    st.write("")
    st.write("")
    search = st.button("🔎 검색", use_container_width=True)

# --- 검색 버튼 눌렀을 때만 차트 변경 ---
if "df" not in st.session_state:
    st.session_state.df = None

if search:
    rows = cty_pop_sql.select_cty_pop(year=selected_year, cty_codes=selected_codes)
    st.session_state.df = pd.DataFrame(rows, columns=["CTY_NM", "CTY_POP_YR", "CTY_POP"])

df = st.session_state.df

if df is None:
    st.info("연도/지역을 선택하고 검색을 눌러주세요.")
elif df.empty:
    st.warning("조건에 맞는 데이터가 없어요.")
else:
    st.subheader(f"✅ {selected_year}년 도시별 인구")

    fig, ax = plt.subplots()
    ax.bar(df["CTY_NM"], df["CTY_POP"])
    ax.set_xlabel("도시")
    ax.set_ylabel("인구")
    ax.set_title("도시별 인구 (막대그래프)")
    plt.xticks(rotation=45, ha="right")

    st.pyplot(fig, clear_figure=True)
    st.dataframe(df, use_container_width=True)
