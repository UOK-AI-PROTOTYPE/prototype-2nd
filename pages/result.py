import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import re

def find_mbti(result):
    mbti_pattern = re.compile(r'MBTI\s*:\s*([A-Z]{4})')
    mbti_match = mbti_pattern.search(result)
    mbti = mbti_match.group(1) if mbti_match else None

    ratio_pattern = re.compile(r'([A-Z])\s*\(.*?\):\s*(\d+)%')
    ratios = {match.group(1): int(match.group(2)) for match in ratio_pattern.finditer(result)}

    return mbti, ratios

if "mbti" not in st.session_state:
    st.session_state.mbti = []

sum_E = 0
sum_N = 0
sum_F = 0
sum_J = 0

for data in st.session_state.participant:
    mbti, ratios = find_mbti(data["result"])
    if 'E' in ratios:
        E_value = ratios['E']
    else:
        E_value = 100 - ratios['I']
    if 'N' in ratios:
        N_value = ratios['N']
    else:
        N_value = 100 - ratios['S']
    if 'F' in ratios:
        F_value = ratios['F']
    else:
        F_value = 100 - ratios['T']
    if 'J' in ratios:
        J_value = ratios['J']
    else:
        J_value = 100 - ratios['P']

    st.session_state.mbti.append({"mbti": mbti, "E": E_value, "N": N_value, "F": F_value, "J": J_value})
    sum_E += E_value
    sum_N += N_value
    sum_F += F_value
    sum_J += J_value

self_mbti = st.session_state.mbti[0]

total_E = sum_E // st.session_state['num_participant']
total_N = sum_N // st.session_state['num_participant']
total_F = sum_F // st.session_state['num_participant']
total_J = sum_J // st.session_state['num_participant']

self_E = int(self_mbti['E'])
self_N = int(self_mbti['N'])
self_F = int(self_mbti['F'])
self_J = int(self_mbti['J'])

other_E = (sum_E - self_E) // (st.session_state['num_participant'] - 1)
other_N = (sum_N - self_N) // (st.session_state['num_participant'] - 1)
other_F = (sum_F - self_F) // (st.session_state['num_participant'] - 1)
other_J = (sum_J - self_J) // (st.session_state['num_participant'] - 1)

# 그래프 색상
given_color = ['#fff09e', '#9ff0ce', '#ff9f9f', '#cdafff']

def getGraph(type, E, N, F, J):
    mbti = ""
    left_colors = []
    right_colors = []
    if E >= 50:
        mbti += "E"
        left_colors.append(given_color[0])
        right_colors.append('lightgrey')
    else:
        mbti += "I"
        left_colors.append('lightgrey')
        right_colors.append(given_color[0])
    if N >= 50:
        mbti += "N"
        left_colors.append(given_color[1])
        right_colors.append('lightgrey')
    else:
        mbti += "S"
        left_colors.append('lightgrey')
        right_colors.append(given_color[1])
    if F >= 50:
        mbti += "F"
        left_colors.append(given_color[2])
        right_colors.append('lightgrey')
    else:
        mbti += "T"
        left_colors.append('lightgrey')
        right_colors.append(given_color[2])
    if J >= 50:
        mbti += "J"
        left_colors.append(given_color[3])
        right_colors.append('lightgrey')
    else:
        mbti += "P"
        left_colors.append('lightgrey')
        right_colors.append(given_color[3])

    labels = ['E / I', 'N / S', 'F / T', 'J / P']
    left_labels= ['E', 'N', 'F', 'J']
    right_labels = ['I', 'S', 'T', 'P']
    left_values = [E, N , F, J]
    right_values = [100 - E, 100 - N , 100 - F, 100 - J]

    # 그래프 그리기
    fig, ax = plt.subplots(figsize=(9, 2))

    # 양쪽에 막대그래프 그리기
    y = np.arange(len(labels))
    ax.barh(y, left_values, color=left_colors, edgecolor='none')
    ax.barh(y, right_values, left=left_values, color=right_colors, edgecolor='none')

    # 각 항목의 값을 텍스트로 표시
    for i in range(len(labels)):
        # 왼쪽 mbti 비중
        ax.text(left_values[i] - 5, i, f'{left_values[i]}%', va='center', ha='right', color='black', fontweight='bold')
        # 오른쪽 mbti 비중
        ax.text(left_values[i] + 5, i, f'{right_values[i]}%', va='center', ha='left', color='black', fontweight='bold')
        # 왼쪽 mbti 유형
        ax.text(5, i, left_labels[i], va='center', ha='center', color='black', fontweight='bold')
        # 오른쪽 mbti 유형
        ax.text(95, i, right_labels[i], va='center', ha='center', color='black', fontweight='bold')

    # Y축 설정
    ax.set_yticks(y)
    ax.set_yticklabels(labels)

    # 기타 설정
    ax.invert_yaxis()
    # ax.set_xlabel('Percentage')
    ax.set_title(f'{type} : {mbti}')

    # 레이아웃을 조정하여 공백 제거
    plt.tight_layout() # 그래프 크기 다름
    ax.set_xlim(0, 100) # 오른쪽 여백 제거

    # Streamlit에 그래프 표시
    st.pyplot(fig)

    return mbti

st.title(f"{st.session_state['target_name']}님의 분석결과")
getGraph("TOTAL", total_E, total_N, total_F, total_J)
getGraph("SELF", self_mbti['E'], self_mbti['N'], self_mbti['F'], self_mbti['J'])
getGraph("OTHER", other_E, other_N, other_F, other_J)

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







# ###################################################
# ### 테스트 버전 ###
# import streamlit as st
# import matplotlib.pyplot as plt
# import numpy as np

# # 예제 데이터
# labels = ['A', 'B', 'C', 'D']
# left_values = [68, 56, 51, 63]
# right_values = [32, 44, 49, 37]
# left_labels = ['A', 'B', 'C', 'D']
# right_labels = ['F', 'G', 'H', 'I']
# # colors = ['#4daf8b', '#ffaf40', '#92c657', '#d86f98']
# colors = ['#fff09e', '#9ff0ce', '#ff9f9f', '#cdafff']

# # 그래프 그리기
# fig, ax = plt.subplots(figsize=(9, 2))

# # 양쪽에 막대그래프 그리기
# y = np.arange(len(labels))
# ax.barh(y, left_values, color=colors, edgecolor='none')
# ax.barh(y, right_values, left=left_values, color='lightgrey', edgecolor='none')

# # 각 항목의 값을 텍스트로 표시
# for i in range(len(labels)):
#     ax.text(left_values[i] - 5, i, f'{left_values[i]}%', va='center', ha='right', color='black', fontweight='bold')
#     ax.text(left_values[i] + 5, i, f'{right_values[i]}%', va='center', ha='left', color='black', fontweight='bold')
#     ax.text(5, i, left_labels[i], va='center', ha='center', color='black', fontweight='bold')
#     ax.text(95, i, right_labels[i], va='center', ha='center', color='black', fontweight='bold')

# # Y축 설정
# ax.set_yticks(y)
# ax.set_yticklabels(labels)

# # 기타 설정
# ax.invert_yaxis()
# ax.set_title('MBTI')

# # 레이아웃을 조정하여 공백 제거
# # plt.tight_layout() # 그래프 크기 다름
# ax.set_xlim(0, 100) # 오른쪽 여백 제거

# st.title('준우님의 MBTI 분석 결과')

# # Streamlit에 그래프 표시
# st.pyplot(fig)

# # CSS for alignment
# st.markdown("""
#     <style>
#     div.stButton > button {
#         display: block;
#         margin: 0 auto;
#     }
#     </style>
# """, unsafe_allow_html=True)

# if st.button("다시 분석 하러가기", type="primary"):
#     # st.session_state의 특정값들을 삭제해서 chat 페이지로 돌아갔을 때, 상태 초기화
#     del st.session_state.messages
#     del st.session_state['remaining_users']
#     del st.session_state.participant
#     del st.session_state.mbti

#     st.switch_page("pages/chat.py")






# ###################################################
# ### st.bar_chart 사용 ###
# import streamlit as st
# import pandas as pd
# import numpy as np
# from utils.chat_background import chat_background

# chart_data = pd.DataFrame(
#    {
#        "col1": ['E / I', 'N / S', 'F / T', 'J / P'],
#        "col2": [60, 70, 80, 30],
#        "col3": ['#fff09e', '#9ff0ce', '#ff9f9f', '#cdafff']
       
#    }
# )

# st.bar_chart(chart_data, x="col1", y="col2", color = "col3", horizontal=True)
# chat_background()