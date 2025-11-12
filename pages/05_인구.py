import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# ------------------------
# 🔧 기본 설정
# ------------------------
st.set_page_config(page_title="연령별 인구 현황", layout="wide")
st.title("📊 행정구별 연령별 인구 현황")
st.caption("행정구를 선택하면 나이대별 인구를 꺾은선 그래프로 볼 수 있습니다.")

# ------------------------
# 📂 데이터 불러오기
# ------------------------
@st.cache_data
def load_data():
    # 인코딩 깨짐 방지
    df = pd.read_csv("202510_202510_연령별인구현황_월간.csv", encoding="cp949")
    return df

df = load_data()

# ------------------------
# 🔍 컬럼 정리
# ------------------------
# 나이 관련 컬럼만 추출 (예: 0~9세, 10~19세, ...)
age_cols = [col for col in df.columns if "세" in col or "~" in col]

# 행정구 컬럼 자동 탐색 (예: '행정구역', '행정구', 등)
region_col = [c for c in df.columns if "행정" in c or "구역" in c][0]

# ------------------------
# 🗂 행정구 선택
# ------------------------
regions = sorted(df[region_col].dropna().unique())
selected_region = st.selectbox("📍 행정구를 선택하세요", regions)

# 선택한 행정구 데이터
region_row = df[df[region_col] == selected_region].iloc[0]

# ------------------------
# 📈 그래프 데이터 준비
# ------------------------
ages = age_cols
values = [region_row[a] for a in ages]

# ------------------------
# 🎨 Plotly 꺾은선 그래프
# ------------------------
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=ages,
    y=values,
    mode="lines+markers",
    line=dict(color="white", width=3),
    marker=dict(size=7, color="deepskyblue"),
))

fig.update_layout(
    title=f"👥 {selected_region} 연령별 인구 현황",
    xaxis_title="연령대",
    yaxis_title="인구수 (명)",
    plot_bgcolor="#e0e0e0",   # 회색 배경
    paper_bgcolor="#e0e0e0",
    font=dict(size=14),
    xaxis=dict(
        tickmode="linear",
        tick0=0,
        dtick=1,           # 10살 단위로 구분
        gridcolor="white",
        showgrid=True
    ),
    yaxis=dict(
        gridcolor="white",
        dtick=100,          # 100명 단위 구분선
        showgrid=True
    ),
)

st.plotly_chart(fig, use_container_width=True)
