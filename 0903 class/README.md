Streamlit 설치 및 사용

---

## 1. 설치

```bash
pip install streamlit
```

---

## 2. 실행 방법

```bash
streamlit run 파일명.py
```

⚠️ **주의**: `python 파일명.py`로 실행하면 안되고 반드시 `streamlit run`으로 실행해야 브라우저가 열림


```

---

## 3. 기본 뼈대 코드

```python
import streamlit as st

st.title("제목")
st.write("본문 내용")
```

---

## 4. 자주 쓰는 기본 함수

| 함수 | 용도 |
|---|---|
| `st.title("제목")` | 큰 제목 표시 |
| `st.write("내용")` | 텍스트/데이터 출력 (거의 모든 것을 다 받음) |
| `st.text_input("라벨")` | 한 줄 텍스트 입력창 |
| `st.text_area("라벨")` | 여러 줄 텍스트 입력창 |
| `st.button("버튼명")` | 버튼 (누르면 `True` 반환) |
| `st.selectbox("라벨", ["A", "B"])` | 드롭다운 선택 |
| `st.file_uploader("라벨")` | 파일 업로드 |
| `st.dataframe(df)` / `st.table(df)` | 표 형태로 데이터 보여주기 |
| `st.data_editor(df)` | 엑셀처럼 직접 수정 가능한 표 |
| `st.line_chart(df)` / `st.bar_chart(df)` | 그래프 그리기 |
| `st.sidebar` | 왼쪽 사이드바에 요소 배치 |
| `st.columns(숫자)` | 화면을 여러 칸으로 나누기 |

---

## 5. 버튼과 입력값 다루기 예시

```python
import streamlit as st

name = st.text_input("이름을 입력하세요")

if st.button("인사하기"):
    st.write(f"안녕하세요, {name}님!")
```
