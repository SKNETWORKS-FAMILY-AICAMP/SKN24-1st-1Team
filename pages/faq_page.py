import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from sql import faq_sql
import re
import html

# html 태그 남아있는 데이터 없애기
def clean_answer(text: str) -> str:
    if not text:
        return ""
    # 1) HTML 엔티티를 먼저 해제 ( &lt; &gt; &nbsp; 등 )
    text = html.unescape(text)
    # 2) "마지막 수정일 ..." 이하를 통째로 제거 (줄바꿈 포함)
    text = re.sub(r"\s*마지막\s*수정일.*$", "", text, flags=re.DOTALL)
    # 3) HTML 태그 제거
    text = re.sub(r"<[^>]*>", "", text)
    # 4) 혹시 남아있는 '</div>' 같은 잔재도 제거
    text = text.replace("</div>", "").replace("<div>", "")
    # 5) 공백 정리
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()

st.title("자주 묻는 질문(FAQ)")

# -----------------------------
# 상단: SELECT + 오른쪽 검색 버튼
# -----------------------------
col1, col2 = st.columns([6, 1])

with col1:
    brand = st.selectbox(
        "사이트 / 기관 선택",
        ["전체", "국토교통부 민원마당", "한국교통안전공단"]
    )

with col2:
    st.markdown('<div class="search-col">', unsafe_allow_html=True)
    search_clicked = st.button("검색", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# -----------------------------
# DB에서 조회해서 faq_list로 변환
# -----------------------------
where_dict = None
if brand != "전체":
    where_dict = {"INST_NM": brand}

rows = faq_sql.select_faq(where_dict)  # rows: [(QUESTION, ANSWER, INST_NM), ...]

faq_list = [
    (idx + 1, q, clean_answer(a))
    for idx, (q, a, inst) in enumerate(rows)
]

# -----------------------------
# 검색 버튼 눌렀을 때만 필터
# -----------------------------
if search_clicked:
    faq_list = [
        faq for faq in faq_list
    ]

# -----------------------------
# 열림 상태
# -----------------------------
if "open_q" not in st.session_state:
    st.session_state.open_q = None

# -----------------------------
# 스타일
# -----------------------------
st.markdown("""
<style>
.q-box {
    border: 1.5px solid #cfcfcf;
    border-radius: 10px;
    padding: 18px;
    margin-bottom: 8px;
    background-color: white;
    font-weight: 500;
}
.a-box {
    background-color: #dbe9ff;
    border-radius: 6px;
    padding: 18px;
    margin-bottom: 20px;
}
.search-col div.stButton > button {
    margin-top: 28px;
    height: 42px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 출력 (그대로)
# -----------------------------
for faq_id, question, answer in faq_list:

    if st.button(
        f"Q. {question}",
        key=f"q_{faq_id}",
        use_container_width=True
    ):
        st.session_state.open_q = (
            None if st.session_state.open_q == faq_id else faq_id
        )

    if st.session_state.open_q == faq_id:
        st.markdown(
            f"<div class='a-box'>A. {answer}</div>",
            unsafe_allow_html=True
        )
