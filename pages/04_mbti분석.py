import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="Countries MBTI Visualizer", layout="wide")

st.title("🌍 국가별 MBTI 유형 비율 시각화 (Plotly)")

# --- 데이터 업로드 ---
st.sidebar.header("📁 데이터 업로드")
uploaded_file = st.sidebar.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.info("예시 데이터: countriesMBTI_16types.csv 파일을 업로드하면 작동합니다.")
    st.stop()

# --- 컬럼 구조 확인 ---
if "Country" not in df.columns:
    st.error("❌ 'Country' 컬럼이 없습니다. CSV 파일을 확인해주세요.")
    st.stop()

mbti_cols = [c for c in df.columns if c != "Country"]

# --- 비율로 변환 ---
df_ratio = df.copy()
df_ratio[mbti_cols] = df_ratio[mbti_cols].div(df_ratio[mbti_cols].sum(axis=1), axis=0) * 100

# --- 국가 선택 ---
st.sidebar.subheader("🌏 국가별 보기")
country_list = df_ratio["Country"].sort_values().tolist()
selected_country = st.sidebar.selectbox("국가를 선택하세요", country_list, index=0)

# --- 선택 국가의 MBTI 분포 ---
country_data = df_ratio[df_ratio["Country"] == selected_country][mbti_cols].melt(
    var_name="MBTI", value_name="Percentage"
)
country_data = country_data.sort_values(by="Percentage", ascending=False).reset_index(drop=True)

# 색상 지정: 1등은 빨강, 나머지는 파란색 그라데이션
colors = ["#FF4B4B"] + px.colors.sequential.Blues_r[1:len(country_data)]

fig_country = px.bar(
    country_data,
    x="MBTI",
    y="Percentage",
    text=country_data["Percentage"].map(lambda x: f"{x:.1f}%"),
    color=country_data.index,
    color_continuous_scale=px.colors.sequential.Blues_r,
)

fig_country.data[0].marker.color = colors
fig_country.update_traces(textposition="outside")
fig_country.update_layout(
    title=f"🇰🇷 {selected_country} MBTI 유형 비율",
    xaxis_title="MBTI 유형",
    yaxis_title="비율 (%)",
    showlegend=False,
    plot_bgcolor="white",
    font=dict(size=14),
)

st.plotly_chart(fig_country, use_container_width=True)

with st.expander("🔍 국가 데이터 보기"):
    st.dataframe(country_data, use_container_width=True)


# --- 하단: MBTI 유형별 상위 국가 그래프 ---
st.markdown("---")
st.subheader("📊 MBTI 유형별 상위 국가 순위")

selected_mbti = st.selectbox("MBTI 유형을 선택하세요", mbti_cols, index=0)

mbti_rank = df_ratio[["Country", selected_mbti]].sort_values(
    by=selected_mbti, ascending=False
).reset_index(drop=True)

# 색상 설정: 1등은 빨강, 나머지는 회색, 한국은 파란색
colors_rank = []
for i, row in mbti_rank.iterrows():
    if row["Country"].lower() in ["south korea", "korea", "republic of korea", "대한민국"]:
        colors_rank.append("#1877F2")  # 한국: 파란색
    elif i == 0:
        colors_rank.append("#FF4B4B")  # 1등: 빨간색
    else:
        colors_rank.append("#CCCCCC")  # 나머지: 회색

fig_mbti = px.bar(
    mbti_rank,
    x="Country",
    y=selected_mbti,
    text=mbti_rank[selected_mbti].map(lambda x: f"{x:.1f}%"),
)

fig_mbti.update_traces(marker_color=colors_rank, textposition="outside")
fig_mbti.update_layout(
    title=f"💡 {selected_mbti} 유형이 가장 높은 국가 순위",
    xaxis_title="국가",
    yaxis_title="비율 (%)",
    plot_bgcolor="white",
    font=dict(size=13),
    xaxis_tickangle=-45,
)

st.plotly_chart(fig_mbti, use_container_width=True)

with st.expander("🔍 MBTI 유형별 국가 데이터 보기"):
    st.dataframe(mbti_rank, use_container_width=True)
