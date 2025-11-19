import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------------------------
# 페이지 설정
# ----------------------------------------------------
st.set_page_config(
    page_title="서울시 자치구별 일반음식점 현황",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------------------------------
# 데이터 직접 정의 (CSV 파일 대체)
# ----------------------------------------------------
# 25개 자치구의 일반음식점 수 데이터를 리스트로 직접 정의
RESTAURANT_DATA = {
    'Rank': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25],
    'District': [
        '강남구', '송파구', '영등포구', '마포구', '서초구', '중구', '강서구', '노원구', 
        '은평구', '관악구', '성북구', '종로구', '동대문구', '강동구', '광진구', '구로구', 
        '양천구', '성동구', '동작구', '용산구', '금천구', '도봉구', '중랑구', '강북구', '서대문구'
    ],
    'Count': [
        10654, 7610, 6923, 6658, 6550, 6421, 6211, 5888, 
        5618, 5479, 5456, 5223, 5091, 5022, 4960, 4942, 
        4775, 4688, 4670, 4668, 3892, 3694, 3613, 3572, 3473
    ]
}

@st.cache_data
def load_data():
    """정의된 데이터를 DataFrame으로 변환합니다."""
    df = pd.DataFrame(RESTAURANT_DATA)
    df['Count'] = df['Count'].astype(int)
    return df

# 데이터 로드
df = load_data()

# ----------------------------------------------------
# 시각화 함수 (Plotly)
# ----------------------------------------------------
def create_plotly_chart(df):
    """Plotly를 사용하여 인터랙티브한 막대 그래프를 생성합니다."""
    
    # Plotly Express를 사용하여 Count 값에 따른 그라데이션 적용
    fig = px.bar(
        df,
        x='District',          
        y='Count',             
        color='Count',         
        color_continuous_scale=px.colors.sequential.Plasma_r, 
        title="서울시 자치구별 일반음식점 수 현황",
        labels={
            "District": "자치구",
            "Count": "일반음식점 수 (개)",
            "color": "음식점 수"
        },
        height=550,
        hover_data={"Rank": True, "Count": ":,"} 
    )

    # 1등 막대(강남구) 색상만 빨간색으로 강제 변경 (오류 수정 로직 적용)
    top_district = df.iloc[0]['District']
    
    if top_district == '강남구':
        try:
            # 1. 현재 Figure의 모든 막대 색상 리스트를 가져와서 파이썬 리스트로 변환
            colors_list = list(fig.data[0].marker.color)
            
            # 2. 1위 항목(인덱스 0)의 색상을 'red'로 변경
            if len(colors_list) > 0:
                colors_list[0] = 'red'
            
            # 3. 변경된 색상 리스트를 Figure에 다시 적용
            fig.update_traces(marker_color=colors_list, selector=dict(type='bar'))
            
        except AttributeError:
             st.warning("경고: Plotly 그래프의 1위 막대 색상 변경에 실패했습니다. (내부 구조 문제)")

    # 축 레이블 및 툴팁 설정
    fig.update_xaxes(title_font=dict(size=14), tickangle=45)
    fig.update_yaxes(title_font=dict(size=14))
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
    
    # === [요청 사항 반영: 제목 변경 및 컬럼 너비 조정] ===
    st.markdown("### 📋 데이터 테이블") # "가독성 개선 버전" 문구 삭제
    
    # 1. 'Count' 컬럼에 천 단위 구분 기호 포맷 적용
    # 2. 숫자 컬럼을 오른쪽 정렬하고, 홀수 행에 배경색(스트라이프) 적용
    styled_df = df.style.format({
        'Count': '{:,.0f}'.format  # 'Count' 컬럼을 천 단위 콤마로 포맷
    }).set_properties(
        subset=['Count'], **{'text-align': 'right'} 
    ).set_table_styles([
        {'selector': 'tbody tr:nth-child(odd)', 'props': [('background-color', '#f0f2f6')]}
    ])

    # Streamlit에 스타일이 적용된 DataFrame 출력
    st.dataframe(
        styled_df, 
        hide_index=True,
        column_config={
            # Rank 컬럼 너비를 가장 좁게 설정 (very small)
            "Rank": st.column_config.Column(width="tiny"), 
            # 나머지 컬럼 너비 조정으로 상대적으로 넓게 표시
            "District": st.column_config.Column(width="medium"),
            "Count": st.column_config.Column(
                "일반음식점 수 (개)",
                width="large",
            )
        }
    )
    
    # ==================================================
    
    st.caption("※ 데이터 출처: 서울시 상권분석서비스 기반 2024년 6월 현황")
