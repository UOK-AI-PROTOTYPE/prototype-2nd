import streamlit as st
import streamlit.components.v1 as components


# CSS 파일 읽기
def load_css(file_path):
    with open(file_path) as f:
        return f.read()

css_content = load_css("static/css/intro.css")


def set_intro():

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
        <div class="logo">UOK</div>
        <div class="slogan">당신의 성향을 찾아드립니다</div>
        <a href="#" class="scroll-down">
            <div class="arrow-down1"></div>
            <div class="arrow-down1"></div>
            <div class="arrow-down2"></div>

        </a>
    </body>
    </html>
    """

    components.html(html_code, height=800)