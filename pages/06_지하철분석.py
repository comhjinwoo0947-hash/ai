import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="지하철 분석", layout="wide")

st.title("🚇 서울 지하철 승하차 분석 (2055년 10월)")

# 📌 CSV 로드 (프로젝트 최상위 폴더)
@st.cache_data
def load_data():
    return pd.read_csv("subway.csv", encoding="cp949")   # 🔥 여기 고정!

df = load_data()

# 날짜 포맷
df["사용일자"] = df["사용일자"].astype(str)

# 날짜 선택
unique_dates = sorted(df["사용일자"].unique())
selected_date = st.selectbox("날짜 선택", unique_dates)

# 호선 선택
unique_lines = sorted(df["노선명"].unique())
selected_line = st.selectbox("호선 선택", unique_lines)

# 필터링
filtered = df[(df["사용일자"] == selected_date) & (df["노선명"] == selected_line)].copy()

# 승하차 합
filtered["총승하차"] = filtered["승차총승객수"] + filtered["하차총승객수"]

# 정렬
filtered = filtered.sort_values("총승하차", ascending=False)

# 색상 설정
colors = ["red"]  # 1등 빨강
others = px.colors.sequential.Blues[::-1]

while len(colors) < len(filtered):
    colors.append(others[min(len(colors) - 1, len(others) - 1)])

# Plotly 그래프
fig = px.bar(
    filtered,
    x="역명",
    y="총승하차",
    color=filtered["역명"],
    color_discrete_sequence=colors,
    title=f"{selected_line} {selected_date} 승하차 TOP 역",
)

fig.update_layout(
    xaxis_title="역명",
    yaxis_title="총 승하차(명)",
    showlegend=False,
    bargap=0.2,
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📄 데이터 테이블")
st.dataframe(filtered)
