import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------------------------
# 페이지 설정 (Streamlit 설정은 항상 최상단에 위치해야 합니다)
# ----------------------------------------------------
st.set_page_config(
    page_title="서울시 자치구별 일반음식점 현황",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------------------------------
# 데이터 로드
# ----------------------------------------------------
@st.cache_data
def load_data():
    """CSV 파일에서 데이터를 로드하고 정리합니다."""
    # Streamlit Cloud 환경에서 파일 경로를 'data/restaurant_data.csv'로 가정
    try:
        df = pd.read_csv('data/restaurant_data.csv')
        # 컬럼명 정리
        df.columns = ['Rank', 'District', 'Count']
        # 'Count'를 숫자로 변환
        df['Count'] = df['Count'].astype(int)
        return df
    except FileNotFoundError:
        st.error("데이터 파일을 찾을 수 없습니다. 'data/restaurant_data.csv' 경로를 확인해주세요.")
        return pd.DataFrame()

# 데이터 로드
df = load_data()

# ----------------------------------------------------
# 시각화 함수 (Plotly)
# ----------------------------------------------------
def create_plotly_chart(df):
    """Plotly를 사용하여 인터랙티브한 막대 그래프를 생성합니다."""
    if df.empty:
        return None

    # 1. 막대 색상 설정: 1등(강남구)는 빨간색, 나머지는 그라데이션
    # 가장 높은 값에 빨간색(#FF0000)을 지정하고, 나머지 값에 대해서는 'Viridis'와 같은
    # 연속적인 컬러 스케일을 적용하여 그라데이션 효과를 냅니다.
    
    # Plotly Express의 color 속성을 Count 값에 매핑하여 자동으로 그라데이션 적용
    fig = px.bar(
        df,
        x='District',          # x축: 자치구
        y='Count',             # y축: 일반음식점 수
        color='Count',         # Count 값에 따라 색상(그라데이션) 적용
        color_continuous_scale=px.colors.sequential.Plasma_r, # Viridis_r, Plasma_r 등 다양한 스케일 사용 가능
        title="서울시 자치구별 일반음식점 수 현황",
        labels={
            "District": "자치구",
            "Count": "일반음식점 수 (개)",
            "color": "음식점 수"
        },
        height=550,
        hover_data={"Rank": True, "Count": ":,"} # 툴팁에 순위와 포맷된 수량 표시
    )

    # 2. 1등 막대(강남구) 색상만 빨간색으로 강제 변경
    # 강남구의 인덱스 확인 (가장 첫 번째 데이터라고 가정)
    top_district = df.iloc[0]['District']
    
    # Plotly Figure의 layout.uniformtext를 설정하여 텍스트 가독성 높이기
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

    # 1등 막대만 빨간색으로 강조하는 작업
    # Plotly bar trace의 marker color 리스트를 조작
    
    # 기본 색상(그라데이션)을 Plotly Express가 자동으로 생성한 후,
    # 1위(강남구)의 색상을 수동으로 덮어씁니다.
    # Plotly Express는 하나의 Trace만 생성하므로, data[0]의 색상을 변경합니다.
    if top_district == '강남구':
        # Plotly Figure의 모든 막대 색상을 가져와 리스트로 저장 (Color Scale에 의해 자동 생성된 색상)
        colors = fig.data[0]['marker']['color']
        
        # 첫 번째 항목 (1위)의 색상을 빨간색으로 변경
        colors[0] = 'red'
        
        # 변경된 색상 리스트를 다시 적용
        fig.update_traces(marker_color=colors, selector=dict(type='bar'))
    
    # 축 레이블 한글 설정
    fig.update_xaxes(title_font=dict(size=14), tickangle=45)
    fig.update_yaxes(title_font=dict(size=14))
    
    # 툴팁 설정
    fig.update_traces(hovertemplate='<b>%{x}</b><br>음식점 수: %{y:,}개<extra></extra>')

    return fig

# ----------------------------------------------------
# Streamlit UI 구성
# ----------------------------------------------------
st.title("서울시 자치구별 일반음식점 수 분석 🗺️")
st.markdown("---")

if not df.empty:
    st.subheader("📈 일반음식점 수 시각화 (Plotly Bar Chart)")
    
    # Plotly 그래프 생성 및 표시
    fig = create_plotly_chart(df)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### 📋 데이터 테이블")
    st.dataframe(df, hide_index=True)
    
    st.caption("※ 데이터 출처: 서울시 상권분석서비스 기반 2024년 6월 현황")
