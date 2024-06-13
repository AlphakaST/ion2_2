import streamlit as st
from st_pages import Page, show_pages
from PIL import Image

st.set_page_config(
        page_title="이온을 확인할 수 있는 방법이 있을까?",
        page_icon="./alpaca.jpg",
        layout="wide"
)
image = Image.open("header2.jpg")
st.image(image)
st.subheader("")
st.title(":bookmark_tabs: 프로젝트명: 이온 확인 프로젝트")
st.header(":ballot_box_with_check: 오늘의 수업은?")

# 수업 도입 영상
video_file = open('ion1.mp4', 'rb')
video_bytes = video_file.read()
st.video(video_bytes)
st.divider()

st.subheader(':white_check_mark: 특정 이온을 알아낼 수 있는 방법은?')
with st.form(key='my_form'):
        st.markdown('##### :smile: 간단하게 체크해 보자!')
        prediction = st.radio(
        "", 
        ["불꽃반응", "앙금 생성 반응"])

        submitted = st.form_submit_button("나의 결과는?")
if submitted:
    st.write("나는 특정 이온을 알아낼 수 있는 방법이 ", prediction, "이라고 생각해!") 
st.divider()

st.subheader(":eyes: 가상 실험으로 직접 실험해 보자!")

# 다른 페이지 표시(side)
show_pages(
    [
        Page("app1_0.py", "복습하기", ":white_check_mark:"),
        Page("app1_1.py", "오늘의 수업은?", ":grey_question:"),
        Page("app1_2.py", "앙금 생성 반응", ":chart_with_upwards_trend:"),
        Page("app1_3.py", "오늘의 수업 평가", ":100:"),
        Page("app1_4.py", "교사용 대시보드", ":bookmark_tabs:"),
    ]
)