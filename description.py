import streamlit as st
import streamlit.components.v1 as components


# CSS 파일 읽기
def load_css(file_path):
    with open(file_path) as f:
        return f.read()

css_content = load_css("src/description.css")


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
        <div class="subtitle">사용자와 지인들이 챗봇과의 대화에  함께 참여하여<br>보다 객관적이고 종합적인 성향 분석 결과를 알려드립니다.</div>
    </body>
    </html>
    """
    components.html(html_code, height=350)

    st.image("src/image/description.png")

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
        <dev class="title2">다양한 관점에서 나를 바라보고, </br> 더 나은 자신을 발견해보세요.</div>
    </body>
    </html>
    """
    components.html(html_code, height=200)

    