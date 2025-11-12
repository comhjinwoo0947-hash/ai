import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# ------------------------
# ⚙️ 기본 설정
# ------------------------
st.set_page_config(page_title="연령별 인구 현황", layout="wide")
st.title("📊 행정구별 연령별 인구 현황")
st.caption("행정구를 선택하면 연령대별 인구수를 꺾은선 그래프로 볼 수 있습니다.")

# ------------------------
# 📂 데이터 불러오기
# ------------------------
@st.cache_data
def load_data():
    # CSV 파일 읽기 (한글 깨짐 방지)
    df = pd.read_csv("202510_202510_연령별인구현황_월간.csv", encoding="cp949")
    return df

df = load_data()

# ------------------------
# 🔍 컬럼 정리
# ------------------------
# 행정구 컬럼 찾기
region_col = [c for c in df.columns if "행정" in c or "구역" in c][0]

# 나이 관련 컬럼 찾기 (예: 0~9세, 10~19세, ...)
age_cols = [c for c in df.columns if "세" in c or "~" in c]

# ------------------------
# 🏙️ 행정구 선택
# ------------------------
regions = sorted(df[region_col].dropna().unique())
selected_region = st.selectbox("📍 행정구를 선택하세요", regions)

# 선택된 행정구 데이터 1행 추출
row = df[df[region_col] == selected_region].iloc[0]

# ------------------------
# 📊 데이터 준비
# ------------------------
x = age_cols
y = [row[a] for a in age_cols]

# ------------------------
# 🎨 Plotly 그래프
# ------------------------
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=x,
    y=y,
    mode="lines+markers",
    line=dict(color="white", width=3),
    marker=dict(size=7, color="deepskyblue")
))

fig.update_layout(
    title=f"👥 {selected_region} 연령별 인구 현황",
    xaxis_title="연령대",
    yaxis_title="인구수(명)",
    plot_bgcolor="#d9d9d9",   # 회색 바탕
    paper_bgcolor="#d9d9d9",
    font=dict(size=14),
    xaxis=dict(
        tickmode="linear",
        tick0=0,
        dtick=1,             # 가로축 10살 단위 구분선
        gridcolor="white",
        showgrid=True
    ),
    yaxis=dict(
        dtick=100,           # 세로축 100명 단위 구분선
        gridcolor="white",
        showgrid=True
    )
)

st.plotly_chart(fig, use_container_width=True)
