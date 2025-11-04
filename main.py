import streamlit as st
st.title('나의 첫 웹 서비스 만들기!')
st.write('안녕하세요, 만나서 반갑습니다!')
name=st.text_input('이름을 입력해주세요!')
food=st.selectbox('좋아하는 음식을 선택해주세요',['치킨','준혁이','떡볶이','바나나'])
if st.button('인사말 생성'):
  st.info(name+'님! 안녕하세요!')
  st.warning(food+'를 좋아하시나봐요!, 난 싫어요')
  st.error('반갑습니다!!!')
