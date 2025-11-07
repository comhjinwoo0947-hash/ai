# app.py
import streamlit as st
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="Seoul Top10 (Folium)", layout="wide")

st.title("서울 인기 관광지 Top 10 — Folium 지도")
st.markdown("""
외국인 방문객들이 선호하는 서울의 주요 명소 Top 10을 지도에 표시합니다.
마커를 클릭하면 간단한 설명과 링크(있는 경우)를 볼 수 있습니다.
""")

# Top 10 장소 (이름, 위도, 경도, 간단설명)
places = [
    {
        "name": "Gyeongbokgung Palace (경복궁)",
        "lat": 37.580467, "lon": 126.976944,
        "desc": "조선 시대의 대표 궁궐. 수문장 교대식 등 볼거리 많음."
    },
    {
        "name": "Changdeokgung Palace (창덕궁) & Secret Garden",
        "lat": 37.579254, "lon": 126.992150,
        "desc": "유네스코 세계문화유산, 후원이 유명합니다."
    },
    {
        "name": "Bukchon Hanok Village (북촌 한옥마을)",
        "lat": 37.5830, "lon": 126.9869,
        "desc": "전통 한옥이 남아있는 골목마을. 사진 촬영 명소."
    },
    {
        "name": "N Seoul Tower (N서울타워) / Namsan",
        "lat": 37.551170, "lon": 126.988228,
        "desc": "서울 전경을 한눈에 볼 수 있는 전망대."
    },
    {
        "name": "Myeongdong (명동 쇼핑거리)",
        "lat": 37.5600, "lon": 126.9858,
        "desc": "쇼핑과 길거리 음식이 풍부한 대표 상업지."
    },
    {
        "name": "Insadong (인사동)",
        "lat": 37.5729, "lon": 126.9859,
        "desc": "전통 공예품과 찻집이 많은 문화거리."
    },
    {
        "name": "Hongdae (홍대/홍익대 주변)",
        "lat": 37.55528, "lon": 126.92333,
        "desc": "젊음의 거리, 스트리트 퍼포먼스와 카페·클럽이 유명."
    },
    {
        "name": "Dongdaemun Design Plaza (DDP) / 동대문",
        "lat": 37.5669, "lon": 127.0094,
        "desc": "현대적 건축물과 야시장·쇼핑이 활발한 지역."
    },
    {
        "name": "Cheonggyecheon Stream (청계천)",
        "lat": 37.5687, "lon": 127.0038,
        "desc": "복원된 도심 하천. 도심 속 산책로로 인기."
    },
    {
        "name": "Lotte World Tower / Jamsil (롯데월드타워)",
        "lat": 37.512779, "lon": 127.102570,
        "desc": "초고층 전망대(Seoul Sky)와 쇼핑몰, 아쿠아리움 등."
    }
]

# 지도 초기 중심값: 서울 중앙 근처
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

# 마커 추가
for p in places:
    popup_html = f"<b>{p['name']}</b><br>{p['desc']}"
    folium.Marker(
        location=[p['lat'], p['lon']],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=p['name'],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# 왼쪽 사이드바: 리스트와 선택 기능
st.sidebar.header("장소 목록")
selected = st.sidebar.selectbox("장소 선택 (지도 중심 이동):", ["전체 보기"] + [p["name"] for p in places])

if selected != "전체 보기":
    # 선택한 장소를 중심으로 지도 재생성 (더 크게 줌)
    sel = next(p for p in places if p["name"] == selected)
    m = folium.Map(location=[sel["lat"], sel["lon"]], zoom_start=15)
    for p in places:
        popup_html = f"<b>{p['name']}</b><br>{p['desc']}"
        folium.Marker(
            location=[p['lat'], p['lon']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=p['name'],
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

# Folium 지도 렌더링 (streamlit-folium)
st_data = st_folium(m, width=1100, height=650)

# 간단한 출처/설명
st.markdown("---")
st.markdown("**참고:** 명소 정보는 관광 안내/여행 가이드와 공공 자료를 참고하여 선정했습니다.")
