import streamlit as st
import pandas as pd
import mysql.connector
from openai import OpenAI
from PIL import Image

st.set_page_config(
    page_title="앙금 생성 반응",
    page_icon="./image/alpaca.jpg",
    layout="wide"
)

image = Image.open("image/header2.jpg")
st.image(image)
st.subheader("")
st.title("학생 답안 제출 양식")
st.divider()
st.header("5문제의 서술형 답안을 제출하세요")

# OpenAI API 키 설정
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# MySQL 연결 설정
db_config = {
    'host': st.secrets["connections"]["mysql"]["host"],
    'user': st.secrets["connections"]["mysql"]["username"],
    'password': st.secrets["connections"]["mysql"]["password"],
    'database': st.secrets["connections"]["mysql"]["database"],
    'port': st.secrets["connections"]["mysql"]["port"]
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# 데이터 읽기 함수
def read_existing_data():
    query = "SELECT * FROM student_responses_2"
    cursor.execute(query)
    result = cursor.fetchall()
    columns = cursor.column_names
    return pd.DataFrame(result, columns=columns)

existing_data = read_existing_data()

hints = {
    "1": "힌트: (+)전하와 (-)전하의 총량을 비교해 볼까요?",
    "2": "힌트: A: 원자핵의 양전하량은 원소번호와 동일합니다. B와 C는 B+,B2+,B2- 처럼 맞게 쓰면 됩니다.",
    "3": "힌트: 설탕은 이온 상태로 나누어지지 않습니다. 전기가 통하려면 어떻게 되어야 할까요?",
    "4": "힌트: NaCl과 ? 수용액이 반응해서 맨 오른쪽 수용액이 되었습니다.",
    "5": "힌트: X 수용액과 질산 은이 반응해서 흰색 앙금을 생성하려면 X 에는 무엇이 있어야 할까요? 또, X와 탄산 칼륨의 반응으로 나온 흰색 앙금은요?"
}

example_answers = {
    "1": "(가)는 양이온, (나)는 음이온, (다)는 원자이다. 그 까닭은, (가)에서 (+)전하의 총량과 (-)전하의 총량을 더하면 (+)전하가 더 많기 때문이다. (나)에서는 (-)전하가 더 많고, (다)에서는 (+)와 (-)전하의 총량이 같기 때문이다.",
    "2": "A 이온의 이온식은 Be2+이고, 남아 있는 전자의 개수는 2개이다. 그리고 B 이온의 이온식은 B+, C의 이온식은 C2-이다.",
    "3": "전기 전도계에 불이 들어오는 수용액은 (가)이다. 왜냐하면 (가) 수용액 속에 이온이 존재하기 때문이다. 구체적으로는 +, -극에 이온화된 입자가 이동하면서 전류가 흐르기 때문이다.",
    "4": "? 수용액에 녹아 있는 물질은 질산 은(혹은 AgNO3)이다. 왜냐하면 혼합 용액에서 염화 은(혹은 AgCl)이 생성되고, 질산(혹은 NO3-) 이온이 반응에 참여하지 않고 남아 있는 것으로 보아, X 수용액에는 은과 질산 이온(혹은 Ag+, NO3-)이 들어 있는 것을 알 수 있다.",
    "5": "염화 칼슘 수용액(혹은 CaCl2 수용액)이다. 그 까닭은, 질산 은과 반응하여 흰색 앙금으로 염화 은(혹은 AgCl)이 형성되므로 X 수용액에는 염화 이온(혹은 Cl-)이 있을 것이고, 탄산 칼륨과 X 수용액이 반응하여 흰색 앙금이 생성되려면 X 수용액에는 칼슘 이온(혹은 Ca2+)이 있을 것이라 추측할 수 있다."
}

# 힌트 상태 초기화
if 'show_hints' not in st.session_state:
    st.session_state.show_hints = [False] * 5

with st.form(key="Feedback_form"):
    student_id = st.text_input("**학번을 입력하세요**", placeholder="예: 1학년 1반 5번 -> 10105, 1학년 1반 30번 -> 10130)")

    st.image("number1.jpg", caption="문제1", use_column_width=True)
    answer1 = st.text_area("**1. 그림은 원자와 이온을 모형으로 나타낸 것이다. (가)~(다)를 원자, 양이온, 음이온으로 구분하고, 그 까닭을 (+)전하의 총량과 (-)전하의 총량으로 비교하여 설명하시오.**")
    
    
    # 문제 1에 대한 힌트
    submit_button1 = st.form_submit_button(label='힌트1')
    if submit_button1:
        st.session_state.show_hints[0] = not st.session_state.show_hints[0]
    if st.session_state.show_hints[0]:
        st.write(hints["1"])

    st.image("number2.jpg", caption="문제2", use_column_width=True)
    answer2 = st.text_area("**2. 그래프는 어떤 원자 A-C가 이온이 될 때 얻거나 잃은 전자수를 나타낸 것이다(단, 그래프에 나타낸 이온은 안정하며, A-C는 임의의 원소 기호이다.). A 원자의 원자핵이 띠는 전하의 총량이 +4일 때, A 이온의 이온식을 실제 원소 기호를 이용하여 나타내고, 남아 있는 전자의 개수를 쓰시오. 그리고 B 이온과 C 이온을 이온식으로 표현하시오.**")
    
    # 문제 2에 대한 힌트
    submit_button2 = st.form_submit_button(label='힌트2')
    if submit_button2:
        st.session_state.show_hints[1] = not st.session_state.show_hints[1]
    if st.session_state.show_hints[1]:
        st.write(hints["2"])

    st.image("number3.jpg", caption="문제3", use_column_width=True)
    answer3 = st.text_area("**3. (가)와 (나) 중 간이 전기 전도계를 수용액에 각각 담갔을 때 불이 들어오는 수용액을 고르고, 그 까닭을 설명하시오.**")
    
    # 문제 3에 대한 힌트
    submit_button3 = st.form_submit_button(label='힌트3')
    if submit_button3:
        st.session_state.show_hints[2] = not st.session_state.show_hints[2]
    if st.session_state.show_hints[2]:
        st.write(hints["3"])

    st.image("number4.jpg", caption="문제4", use_column_width=True)
    answer4 = st.text_area("**4. 그림은 염화 나트륨 수용액과 미지 수용액의 반응을 모형으로 나타낸 것이다. X 수용액에 녹아 있는 물질의 이름을 쓰고, 그 까닭을 설명하시오.**")
    
    # 문제 4에 대한 힌트
    submit_button4 = st.form_submit_button(label='힌트4')
    if submit_button4:
        st.session_state.show_hints[3] = not st.session_state.show_hints[3]
    if st.session_state.show_hints[3]:
        st.write(hints["4"])

    st.image("number5.jpg", caption="문제5", use_column_width=True)
    answer5 = st.text_area("**5. 표는 미지의 수용액을 구별하기 위해 실험한 결과이다. X 수용액은 무엇인지 쓰고, 그 까닭을 서술하시오. 그리고 흰색 앙금이 생긴 후에도 실험한 수용액에 전기 전도계를 담갔을 때 전기가 통하는지 쓰고, 그 까닭을 서술하시오.**")
    
    # 문제 5에 대한 힌트
    submit_button5 = st.form_submit_button(label='힌트5')
    if submit_button5:
        st.session_state.show_hints[4] = not st.session_state.show_hints[4]
    if st.session_state.show_hints[4]:
        st.write(hints["5"])

    submit_button = st.form_submit_button(label='제출하기')

    if submit_button:
        if len(student_id) != 5 or not student_id.isdigit():
            st.error("학번은 5자리 숫자로 입력해야 합니다. 다시 시도해 주세요.")
        elif not (answer1.strip() and answer2.strip() and answer3.strip() and answer4.strip() and answer5.strip()):
            st.error("모든 문항에 답변을 입력해 주세요.")
        else:
            feedbacks = []
            for i, (answer, example_answer) in enumerate(zip([answer1, answer2, answer3, answer4, answer5], 
                                                             [example_answers["1"], example_answers["2"], example_answers["3"], 
                                                              example_answers["4"], example_answers["5"]])):
                prompt = (f"학생 답안: {answer}\n\n"
                          f"예시 답안: {example_answer}\n\n"
                          f"채점 기준: 예시 답안과 비교하여, 학생 답안이 맞는지 확인하고, 틀린 부분이 있다면 어떤 부분을 공부해야 하는지 간단히 설명해 주세요. "
                          f"학생 답안이 예시 답안과 정확히 일치하지 않더라도, 내용이 맞다면 간단히 이유를 설명해 주세요."
                          f"내용 설명은 최대 200자 이내로 요약하여 제한하고, 설명할 때 교사가 학생에게 대하듯 친절하게 설명해 주세요.")

                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that provides feedback based on given criteria."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.1,
                    max_tokens=200
                )
                feedback = response.choices[0].message.content.strip()
                feedbacks.append(feedback)

            feedback_data = pd.DataFrame(
                [
                    {
                        "student_id": student_id,
                        "number1": answer1,
                        "number2": answer2,
                        "number3": answer3,
                        "number4": answer4,
                        "number5": answer5,
                        "feedback1": feedbacks[0],
                        "feedback2": feedbacks[1],
                        "feedback3": feedbacks[2],
                        "feedback4": feedbacks[3],
                        "feedback5": feedbacks[4]
                    }
                ]
            )

            # 학생에게 피드백 보여주기
            st.subheader("제출한 답안에 대한 피드백:")
            for i in range(1, 6):
                st.write(f"문제 {i}: {feedbacks[i-1]}")

            # 기존 데이터에 새로운 데이터 추가
            for row in feedback_data.itertuples(index=False):
                cursor.execute(
                    """
                    INSERT INTO student_responses_2 (student_id, number1, number2, number3, number4, number5, feedback1, feedback2, feedback3, feedback4, feedback5)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    row
                )
            conn.commit()

            st.success("답안이 성공적으로 제출되었습니다!")

cursor.close()
conn.close()
