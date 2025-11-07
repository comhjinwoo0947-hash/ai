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
    },# app.py
import streamlit as st
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="서울 인기 관광지 Top10", layout="wide")

st.title("🏙️ 서울 인기 관광지 Top 10 지도")
st.markdown("""
외국인들이 가장 많이 방문하는 서울의 대표 명소 10곳을 보여줍니다.  
각 명소는 왜 유명한지, 그리고 **가장 가까운 지하철역**도 함께 안내합니다.
""")

# 관광지 데이터
places = [
    {
        "name": "경복궁 (Gyeongbokgung Palace)",
        "lat": 37.580467, "lon": 126.976944,
        "desc": "조선시대의 법궁이자 가장 큰 궁궐로, 수문장 교대식이 인기 있는 관광 포인트입니다.",
        "nearest_station": "경복궁역 (3호선)"
    },
    {
        "name": "창덕궁 (Changdeokgung Palace)",
        "lat": 37.579254, "lon": 126.992150,
        "desc": "유네스코 세계문화유산으로 지정된 궁궐. 후원(비원)이 특히 아름답기로 유명합니다.",
        "nearest_station": "안국역 (3호선)"
    },
    {
        "name": "북촌 한옥마을 (Bukchon Hanok Village)",
        "lat": 37.5830, "lon": 126.9869,
        "desc": "전통 한옥이 고스란히 보존된 마을로, 한국 전통과 현대가 공존하는 감성 명소입니다.",
        "nearest_station": "안국역 (3호선)"
    },
    {
        "name": "N서울타워 (N Seoul Tower)",
        "lat": 37.551170, "lon": 126.988228,
        "desc": "남산 정상에 위치한 서울의 대표 전망대. '사랑의 자물쇠'로도 유명합니다.",
        "nearest_station": "명동역 (4호선)"
    },
    {
        "name": "명동 쇼핑거리 (Myeongdong)",
        "lat": 37.5600, "lon": 126.9858,
        "desc": "패션, 화장품, 길거리 음식 등 외국인 관광객이 가장 많이 찾는 쇼핑 거리입니다.",
        "nearest_station": "명동역 (4호선)"
    },
    {
        "name": "인사동 (Insadong)",
        "lat": 37.5729, "lon": 126.9859,
        "desc": "전통 공예품, 찻집, 골동품 상점이 즐비한 거리로 한국 문화체험에 제격입니다.",
        "nearest_station": "종각역 (1호선) / 안국역 (3호선)"
    },
    {
        "name": "홍대 (Hongdae)",
        "lat": 37.55528, "lon": 126.92333,
        "desc": "젊음의 거리로, 라이브 공연·거리예술·카페문화가 발달해 있습니다.",
        "nearest_station": "홍대입구역 (2호선)"
    },
    {
        "name": "동대문디자인플라자 (DDP)",
        "lat": 37.5669, "lon": 127.0094,
        "desc": "자하 하디드의 미래형 건축물로, 야시장과 패션몰이 어우러진 복합문화공간입니다.",
        "nearest_station": "동대문역사문화공원역 (2·4·5호선)"
    },
    {
        "name": "청계천 (Cheonggyecheon Stream)",
        "lat": 37.5687, "lon": 127.0038,
        "desc": "도심 속 복원된 하천으로, 낮에는 산책로·밤에는 조명이 아름다운 명소입니다.",
        "nearest_station": "종각역 (1호선)"
    },
    {
        "name": "롯데월드타워 (Lotte World Tower)",
        "lat": 37.512779, "lon": 127.102570,
        "desc": "123층 초고층 빌딩으로, 전망대 ‘Seoul Sky’와 쇼핑몰, 아쿠아리움이 함께 있습니다.",
        "nearest_station": "잠실역 (2·8호선)"
    }
]

# 지도 생성 (중심은 서울 시청 근처)
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12, tiles="CartoDB positron")

# 마커 스타일: 색상/아이콘 변경
for p in places:
    popup_html = f"""
    <div style='width:230px'>
        <h4 style='margin-bottom:5px;'>{p['name']}</h4>
        <p style='font-size:13px;'>{p['desc']}</p>
        <b>🚇 가장 가까운 역:</b> {p['nearest_station']}
    </div>
    """
    folium.Marker(
        location=[p['lat'], p['lon']],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=p['name'],
        icon=folium.Icon(color="red", icon="star")
    ).add_to(m)

# Folium 지도 렌더링
st_data = st_folium(m, width=1100, height=650)

# 지도 아래 설명
st.markdown("---")
st.subheader("📖 명소별 상세 설명")
for i, p in enumerate(places, start=1):
    st.markdown(f"""
    **{i}. {p['name']}**  
    {p['desc']}  
    🚇 **가장 가까운 지하철역:** {p['nearest_station']}
    """)
