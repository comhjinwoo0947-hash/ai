import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="Countries MBTI Visualizer", layout="wide")

st.title("🌍 국가별 MBTI 유형 비율 시각화 (Plotly)")

# 데이터 불러오기
st.sidebar.header("📁 데이터 업로드")
uploaded_file = st.sidebar.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.info("예시 데이터: countriesMBTI_16types.csv 파일을 업로드하면 작동합니다.")
    st.stop()

# 데이터 구조 확인
if "Country" not in df.columns:
    st.error("❌ 'Country' 컬럼이 없습니다. CSV 파일을 확인해주세요.")
    st.stop()

# MBTI 컬럼 자동 탐색
mbti_cols = [c for c in df.columns if c != "Country"]

# 데이터 정규화 (비율로 변환)
df_ratio = df.copy()
df_ratio[mbti_cols] = df_ratio[mbti_cols].div(df_ratio[mbti_cols].sum(axis=1), axis=0) * 100

# 국가 선택
country_list = df_ratio["Country"].sort_values().tolist()
selected_country = st.sidebar.selectbox("🌏 국가 선택", country_list, index=0)

# 선택된 국가의 데이터 추출
country_data = df_ratio[df_ratio["Country"] == selected_country][mbti_cols].melt(
    var_name="MBTI", value_name="Percentage"
)

# 내림차순 정렬
country_data = country_data.sort_values(by="Percentage", ascending=False).reset_index(drop=True)

# 색상 지정: 1등은 빨강, 나머지는 파란색 그라데이션
colors = ["#FF4B4B"] + px.colors.sequential.Blues_r[1:len(country_data)]

# Plotly 막대 그래프
fig = px.bar(
    country_data,
    x="MBTI",
    y="Percentage",
    text=country_data["Percentage"].map(lambda x: f"{x:.1f}%"),
    color=country_data.index,  # 색 인덱스로 처리
    color_continuous_scale=px.colors.sequential.Blues_r,
)

# 수동으로 1등 색 강조
fig.data[0].marker.color = colors

# 그래프 디자인 설정
fig.update_traces(textposition="outside")
fig.update_layout(
    title=f"🇨🇳 {selected_country} MBTI 유형 비율",
    xaxis_title="MBTI 유형",
    yaxis_title="비율 (%)",
    showlegend=False,
    plot_bgcolor="white",
    font=dict(size=14),
)

st.plotly_chart(fig, use_container_width=True)

# 데이터 표시
with st.expander("🔍 데이터 보기"):
    st.dataframe(country_data, use_container_width=True)
