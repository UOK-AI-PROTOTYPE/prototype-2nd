### 테스트 버전 ###
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

st.set_page_config(
    initial_sidebar_state="collapsed",
    page_title="UOK AI PROJECT",
    layout="centered",
)


# 예제 데이터
labels = ['A', 'B', 'C', 'D']
left_values = [68, 56, 51, 63]
right_values = [32, 44, 49, 37]
left_labels = ['A', 'B', 'C', 'D']
right_labels = ['F', 'G', 'H', 'I']
colors = ['#a8cbff', '#9ff0ce', '#ff9f9f', '#cdafff']
sub_color = '#efefef'
bar_thickness = 0.7 # 그래프 두께

# 그래프 그리기
fig1, ax = plt.subplots(figsize=(9, 2))
fig2, bx = plt.subplots(figsize=(9, 4))


# 배경색 설정
# background_color = '#efefef'
# fig1.patch.set_facecolor(background_color)
# ax.set_facecolor(background_color)
# fig2.patch.set_facecolor(background_color)
# bx.set_facecolor(background_color)


# 양쪽에 막대그래프 그리기
y = np.arange(len(labels))
ax.barh(y, left_values, height=bar_thickness, color=colors, edgecolor='none')
ax.barh(y, right_values, height=bar_thickness, left=left_values, color=sub_color, edgecolor='none')

bx.barh(y, left_values, height=bar_thickness, color=colors, edgecolor='none')
bx.barh(y, right_values, height=bar_thickness, left=left_values, color=sub_color, edgecolor='none')

# 각 항목의 값을 텍스트로 표시
for i in range(len(labels)):
    ax.text(left_values[i] - 2.5, i, f'{left_values[i]}', va='center', ha='right', color='black')
    ax.text(left_values[i] + 2.5, i, f'{right_values[i]}', va='center', ha='left', color='black')
    ax.text(-1.5, i, left_labels[i], va='center', ha='center', color='black')
    ax.text(101.5, i, right_labels[i], va='center', ha='center', color='black')

for i in range(len(labels)):
    bx.text(left_values[i] - 5, i, f'{left_values[i]}', va='center', ha='right', color='black', fontsize=20)
    bx.text(left_values[i] + 5, i, f'{right_values[i]}', va='center', ha='left', color='black', fontsize=20)
    bx.text(-3, i, left_labels[i], va='center', ha='center', color='black', fontsize=20)
    bx.text(103, i, right_labels[i], va='center', ha='center', color='black', fontsize=20)

# Y축 설정
ax.set_yticks(y)
ax.set_yticklabels(labels)

bx.set_yticks(y)
bx.set_yticklabels(labels, fontsize=20)

# 기타 설정
ax.invert_yaxis()
ax.set_title('MBTI')

bx.invert_yaxis()
bx.set_title('MBTI', fontsize=25)

# x축, y축 눈금을 숨김
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)

bx.get_xaxis().set_visible(False)
bx.get_yaxis().set_visible(False)

# 레이아웃을 조정하여 공백 제거
# plt.tight_layout() # 그래프 크기 다름
ax.set_xlim(0, 100) # 오른쪽 여백 제거

bx.set_xlim(0, 100) # 오른쪽 여백 제거

# 테두리 선을 숨김
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

bx.spines['top'].set_visible(False)
bx.spines['right'].set_visible(False)
bx.spines['left'].set_visible(False)
bx.spines['bottom'].set_visible(False)

st.title('준우님의 MBTI 분석 결과')
st.markdown("")
st.markdown("")

# Streamlit에 그래프 표시
st.pyplot(fig1)
st.markdown("")

col1, col2 = st.columns(2)

with col1:
    st.pyplot(fig2)

with col2:
    st.pyplot(fig2)

# CSS for alignment
st.markdown("""
    <style>
    div.stButton > button {
        display: block;
        margin: 0 auto;
    }
    </style>
""", unsafe_allow_html=True)

if st.button("다시 분석 하러가기", type="primary"):
    # st.session_state의 특정값들을 삭제해서 chat 페이지로 돌아갔을 때, 상태 초기화
    del st.session_state.messages
    del st.session_state['remaining_users']
    del st.session_state.participant
    del st.session_state.mbti

    st.switch_page("pages/chat.py")