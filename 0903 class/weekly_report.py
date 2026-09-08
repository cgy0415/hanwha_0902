"""
주간 보고자료 틀 (Streamlit 기본 기능만 사용, API 비용 없음)
------------------------------------------------------------
- AI API를 전혀 호출하지 않고, Streamlit + pandas만으로
  표와 그래프가 들어간 주간 보고서 화면을 만듭니다.
- st.data_editor로 표를 엑셀처럼 직접 수정할 수 있고,
  입력한 데이터가 그대로 그래프에 반영됩니다.

실행 방법:
    1. 터미널에서 라이브러리를 설치하세요. (모두 무료, API 키 불필요)
       pip install streamlit pandas openpyxl

    2. 앱을 실행하세요.
       streamlit run weekly_report.py
"""

import io
from datetime import date

import pandas as pd
import streamlit as st


# -----------------------------
# 1. 페이지 기본 설정
# -----------------------------
st.set_page_config(page_title="주간 보고자료", page_icon="📊", layout="wide")
st.title("📊 주간 업무 보고서")


# -----------------------------
# 2. 상단 기본 정보 입력
# -----------------------------
col1, col2, col3 = st.columns(3)
with col1:
    author = st.text_input("작성자", value="홍길동")
with col2:
    team = st.text_input("소속팀", value="전략기획팀")
with col3:
    report_date = st.date_input("작성일", value=date.today())

st.divider()


# -----------------------------
# 3. 이번 주 핵심 지표 (숫자 카드)
# -----------------------------
st.subheader("1️⃣ 이번 주 핵심 지표")

kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
# st.metric은 숫자와 함께 지난주 대비 증감(delta)을 화살표로 보여줍니다.
kpi_col1.metric("진행 중 프로젝트", "8건", "+1건")
kpi_col2.metric("이번 주 완료 업무", "23건", "+5건")
kpi_col3.metric("신규 이슈", "3건", "-2건")
kpi_col4.metric("평균 진행률", "67%", "+4%p")

st.caption("※ 위 숫자는 예시입니다. 아래 표를 실제 데이터로 수정하면 이 카드도 함께 연동되도록 확장할 수 있어요.")

st.divider()


# -----------------------------
# 4. 프로젝트별 진행 현황 (편집 가능한 표 + 막대그래프)
# -----------------------------
st.subheader("2️⃣ 프로젝트별 진행 현황")

# 기본 예시 데이터. 표에서 직접 수정/추가/삭제가 가능합니다.
if "project_df" not in st.session_state:
    st.session_state.project_df = pd.DataFrame(
        {
            "프로젝트명": ["A사 ERP 구축", "B공단 IT아웃소싱", "C그룹 클라우드 전환", "D사 스마트팩토리"],
            "담당자": ["김철수", "이영희", "박민수", "정지훈"],
            "진행률(%)": [80, 45, 60, 30],
            "상태": ["정상", "지연", "정상", "정상"],
        }
    )

# st.data_editor: 엑셀처럼 셀을 클릭해서 직접 값을 수정할 수 있는 표입니다.
edited_df = st.data_editor(
    st.session_state.project_df,
    num_rows="dynamic",  # 행 추가/삭제 가능
    use_container_width=True,
    column_config={
        "진행률(%)": st.column_config.NumberColumn(
            "진행률(%)", min_value=0, max_value=100, format="%d%%"
        ),
    },
)
st.session_state.project_df = edited_df

# 표에 입력된 데이터를 그대로 막대그래프로 시각화
st.bar_chart(edited_df.set_index("프로젝트명")["진행률(%)"])

st.divider()


# -----------------------------
# 5. 주간 실적 추이 (라인 그래프)
# -----------------------------
st.subheader("3️⃣ 주간 실적 추이 (최근 4주)")

if "trend_df" not in st.session_state:
    st.session_state.trend_df = pd.DataFrame(
        {
            "주차": ["1주차", "2주차", "3주차", "4주차"],
            "완료 업무 수": [15, 18, 20, 23],
            "신규 이슈 수": [5, 4, 6, 3],
        }
    )

trend_edited = st.data_editor(
    st.session_state.trend_df, use_container_width=True, num_rows="dynamic"
)
st.session_state.trend_df = trend_edited

# 여러 열을 동시에 라인그래프로 그리면 자동으로 범례가 생깁니다.
st.line_chart(trend_edited.set_index("주차"))

st.divider()


# -----------------------------
# 6. 이슈 및 리스크 현황
# -----------------------------
st.subheader("4️⃣ 이슈 및 리스크 현황")

if "issue_df" not in st.session_state:
    st.session_state.issue_df = pd.DataFrame(
        {
            "이슈명": ["일정 지연 우려", "인력 부족", "고객 요구사항 변경"],
            "관련 프로젝트": ["B공단 IT아웃소싱", "C그룹 클라우드 전환", "A사 ERP 구축"],
            "심각도": ["높음", "중간", "낮음"],
            "대응 현황": ["증원 검토 중", "채용 진행 중", "요구사항 재협의 완료"],
        }
    )

issue_edited = st.data_editor(
    st.session_state.issue_df, use_container_width=True, num_rows="dynamic"
)
st.session_state.issue_df = issue_edited

st.divider()


# -----------------------------
# 7. 특이사항 / 다음 주 계획 (자유 서술)
# -----------------------------
st.subheader("5️⃣ 특이사항 및 다음 주 계획")
notes = st.text_area(
    "자유롭게 작성하세요",
    value="- 다음 주 A사 ERP 구축 중간보고 예정\n- B공단 인력 증원 승인 필요",
    height=120,
)

st.divider()


# -----------------------------
# 8. 엑셀 파일로 다운로드 (API 없이, 로컬에서만 처리)
# -----------------------------
st.subheader("📥 보고서 다운로드")


def build_excel_file(author_name: str) -> bytes:
    """작성된 표들을 하나의 엑셀 파일(여러 시트)로 합쳐서 반환합니다."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as excel_writer:
        edited_df.to_excel(excel_writer, sheet_name="프로젝트 현황", index=False)
        trend_edited.to_excel(excel_writer, sheet_name="주간 실적 추이", index=False)
        issue_edited.to_excel(excel_writer, sheet_name="이슈 현황", index=False)
        pd.DataFrame(
            {"항목": ["작성자", "소속팀", "작성일", "특이사항"], "내용": [author_name, team, str(report_date), notes]}
        ).to_excel(excel_writer, sheet_name="기본정보", index=False)
    return output.getvalue()


excel_bytes = build_excel_file(author)
st.download_button(
    "📊 엑셀 파일로 다운로드",
    data=excel_bytes,
    file_name=f"주간보고_{report_date}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)