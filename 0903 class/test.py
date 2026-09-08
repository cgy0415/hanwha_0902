import streamlit as st
import pandas as pd
import numpy as np
df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})

#df
st.write(df)

datframe = np.random.randn(10, 20)
st.dataframe(datframe)
st.write("반가워 스트림릿")

# #숫자 하이라이트
dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns = ('col %d' % i for i in range(20))
)
st.dataframe(dataframe.style.highlight_max(axis=0))

#line chart
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns = ['a', 'b', 'c'])


st.line_chart(chart_data)
