import streamlit as st
import streamlit.components.v1 as components


# CSS 파일 읽기
def load_css(file_path):
    with open(file_path) as f:
        return f.read()

css_content = load_css("static/css/description.css")


def set_description():
    html_code = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
        {css_content}
        </style>
    </head>
    <body>
        <div class="title1">나도 몰랐던 나를 발견하는 시간, </br> 지인과 함께 찾아가는 당신의 성향.</div>
        <div class="subtitle2">사용자와 지인들이 챗봇과의 대화에  함께 참여하여<br>보다 객관적이고 종합적인 성향 분석 결과를 알려드립니다.</div>
    </body>
    </html>
    """
    components.html(html_code, height=700)

    # st.image("assets/image/description.png", width=700)

    html_code = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
        {css_content}
        </style>
    </head>
    <body>
        <div class="title1">다양한 관점에서 나를 바라보고, </br> 더 나은 자신을 발견해보세요.</div>
        <div class="subtitle2"> 분석할 대상자의 이름과 대화에 참여할 인원 수를 작성한 뒤, </br>사용자 본인이 가장 먼저 대화에 참여하고 이후에 지인들이 차례로 대화에 참여합니다.</div>
        <div class="subtitle2"> 답변이 자세할 수록 분석에 좋습니다. </div>
    </html>
    """
    components.html(html_code, height=500)

    