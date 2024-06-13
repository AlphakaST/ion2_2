import streamlit as st
from PIL import Image

st.set_page_config(
      page_title="앙금 생성 반응",
      page_icon="./image/alpaca.jpg",
      layout="wide"
)

image = Image.open('image/header2.jpg')
st.image(image)
st.subheader("")
st.title(":bookmark_tabs: 프로젝트명: 앙금 생성 반응 확인하기")
st.header(':ballot_box_with_check: Mission: 이온 모형으로 반응 이해하기')
st.divider()

# 먼저, 이온 개념과 모형 내용 설명하기
# 어떻게 설명하면서 수업할지 고민하기

# 1. 이온 모형 영상
st.subheader('1. 간단한 앙금 생성 반응, 모형으로 이해하기 :clipboard:')
st.divider()

# 교과서 영상 첨부
video_file = open('ion2.mp4', 'rb')
video_bytes = video_file.read()
st.video(video_bytes)
st.divider()

st.markdown('##### **다음 설명을 읽고, 영상을 이해해 봅시다.**')

# 영상 다 보고, 실험에 대한 설명 보도록 설계
password = st.text_input("비밀번호를 입력하세요", type="password", key="password1")
submit_button = st.button("제출", key="submit1")

if submit_button:
    if password == '0605':
        st.success("비밀번호가 맞습니다.")
        st.subheader("실험 결과")
        st.markdown(" 1. 염화 이온(Cl-)과 은 이온(Ag+)가 반응하여 앙금(AgCl)을 생성한다.")
        st.markdown(" 2. 나트륨 이온(Na+)과 질산 이온(NO3^-)는 반응하지 않고 그대로 존재한다.")
    else:
        st.error("비밀번호가 틀렸습니다.")

st.divider()

# 2. 앙금 생성 반응(가상 실험)
st.subheader('2. 앙금 생성 반응, 가상으로 실험하기! :test_tube:')
st.divider()

# 영상 다 보고, 실험에 대한 설명 보도록 설계
password2 = st.text_input("비밀번호를 입력하세요", type="password", key="password2")
submit_button2 = st.button("제출", key="submit2")

if submit_button2:
    if password2 == '0815':
        st.success("비밀번호가 맞습니다.")
        st.subheader("실험 링크")
        # 인터넷 링크 넣기
        st.markdown("""
<div style='text-align: center;'>
    <a href='https://www.javalab.org/precipitation_reaction/' style='font-size: 24px; text-decoration: none; color: #007BFF;'>앙금 생성 반응</a>
</div>
        """, unsafe_allow_html=True)
    else:
        st.error("비밀번호가 틀렸습니다.")

st.divider()

st.markdown("#### **지난 시간 배웠던 내용을 포함해서, 평가를 진행해 보자! :heavy_check_mark:**")
