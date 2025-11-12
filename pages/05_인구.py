import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# ---- 페이지 설정 ----
st.set_page_config(page_title="연령별 인구 현황", layout="wide")

st.title("📈 행정구별 연령별 인구 현황")
st.write("행정구를 선택하면 해당 지역의 연령대별 인구를 꺾은선 그래프로 확인할 수 있습니다.")

# ---- 데이터 불러오기 ----
@st.cache_data
def load_data():
    df = pd.read_csv("202510_202510_연령별인구현황_월간.csv", encoding="cp949")
    return df

df = load_data()

# ---- 컬럼 정리 ----
# 나이 관련 컬럼만 추출
age_cols = [col for col in df.columns if "~" in col or "세" in col]
region_col = df.columns[0]  # 예: '행정구역'

# ---- 행정구 선택 ----
region_list = sorted(df[region_col].unique())
selected_region = st.selectbox("행정구를 선택하세요", region_list)

# ---- 선택한 지역의 데이터 필터링 ----
region_data = df[df[region_col] == selected_region].iloc[0]

# ---- 그래프 데이터 구성 ----
ages = age_cols
values = [region_data[col] for col in ages]

# ---- Plotly 그래프 생성 ----
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=ages,
    y=values,
    mode='lines+markers',
    line=dict(color='white', width=3),
    marker=dict(size=8, color='lightblue'),
))

fig.update_layout(
    title=f"🧍 {selected_region} 연령별 인구수",
    xaxis_title="연령대",
    yaxis_title="인구수(명)",
    plot_bgcolor="lightgray",
    paper_bgcolor="lightgray",
    font=dict(size=14),
    xaxis=dict(
        tickmode='linear',
        dtick=1,  # 연령대 단위 표시
        gridcolor='white'
    ),
    yaxis=dict(
        gridcolor='white',
        dtick=100  # 100명 단위로 구분선
    )
)

# ---- 그래프 출력 ----
st.plotly_chart(fig, use_container_width=True)
