import streamlit as st
import common


search_map = common.search_box()
print(search_map)




# # --- 사이드바 UI 구성 ---
with st.sidebar:
    # st.header("🗺️ 메뉴 선택")
    
    st.info("이 페이지는 공공데이터를 활용하여 제작하였습니다.", icon="ℹ️")
