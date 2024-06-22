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

def getMBTI(E, N , F, J):
    mbti = ""
    if E > 50:
        mbti += "E"
    else:
        mbti += "I"
    if N > 50:
        mbti += "N"
    else:
        mbti += "S"
    if F > 50:
        mbti += "F"
    else:
        mbti += "T"
    if J > 50:
        mbti += "J"
    else:
        mbti += "P"
        
    return mbti

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
    # st.markdown(f"{data['name']}님의 분석결과")
    # st.markdown(f"MBTI: {mbti}")
    # st.markdown("비율:")
    # for key, value in ratios.items():
    #     st.markdown(f"{key}: {value}%")

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

total_mbti = getMBTI(total_E, total_N, total_F, total_J)
other_mbti = getMBTI(other_E, other_N, other_F, other_J)

     

labels = ['E / I', 'N / S', 'F / T', 'J / P']

# 전체 mbti 평균 결과값
total_left = [total_E, total_N, total_F, total_J]
total_right = [100 - total_E, 100 - total_N, 100 - total_F, 100 - total_J]
# 본인 mbti 결과값
self_left = [self_E, self_N, self_F, self_J]
self_right = [100 - self_E, 100 - self_N, 100 - self_F, 100 - self_J]
# 타인 mbti 평균 결과값
other_left = [other_E, other_N, other_F, other_J]
other_right = [100 - other_E, 100 - other_N, 100 - other_F, 100 - other_J]
# 왼쪽 : E, N, F, J vs 오른쪽 : I, S, T, P
left_labels= ['E', 'N', 'F', 'J']
right_labels = ['I', 'S', 'T', 'P']
colors = ['#4daf8b', '#ffaf40', '#92c657', '#d86f98']

# 그래프 그리기
total_graph, total_ax = plt.subplots(figsize=(9, 2))
self_graph, self_ax = plt.subplots(figsize=(9, 2))
other_graph, other_ax = plt.subplots(figsize=(9, 2))

# 양쪽에 막대그래프 그리기
y = np.arange(len(labels))
total_ax.barh(y, total_left, color=colors, edgecolor='none')
total_ax.barh(y, total_right, left=total_left, color='lightgrey', edgecolor='none')

self_ax.barh(y, self_left, color=colors, edgecolor='none')
self_ax.barh(y, self_right, left=self_left, color='lightgrey', edgecolor='none')

other_ax.barh(y, other_left, color=colors, edgecolor='none')
other_ax.barh(y, other_right, left=other_left, color='lightgrey', edgecolor='none')

# 각 항목의 값을 텍스트로 표시
for i in range(4):
    # 왼쪽 mbti 비중
    total_ax.text(total_left[i] - 5, i, f'{total_left[i]}%', va='center', ha='right', color='black', fontweight='bold')
    self_ax.text(self_left[i] - 5, i, f'{self_left[i]}%', va='center', ha='right', color='black', fontweight='bold')
    other_ax.text(other_left[i] - 5, i, f'{other_left[i]}%', va='center', ha='right', color='black', fontweight='bold')
    # 오른쪽 mbti 비중
    total_ax.text(total_left[i] + 5, i, f'{total_right[i]}%', va='center', ha='left', color='black', fontweight='bold')
    self_ax.text(self_left[i] + 5, i, f'{self_right[i]}%', va='center', ha='left', color='black', fontweight='bold')
    other_ax.text(other_left[i] + 5, i, f'{other_right[i]}%', va='center', ha='left', color='black', fontweight='bold')
    # 왼쪽 mbti 유형
    total_ax.text(5, i, left_labels[i], va='center', ha='center', color='black')
    self_ax.text(5, i, left_labels[i], va='center', ha='center', color='black')
    other_ax.text(5, i, left_labels[i], va='center', ha='center', color='black')
    # 오른쪽 mbti 유형
    total_ax.text(95, i, right_labels[i], va='center', ha='center', color='black')
    self_ax.text(95, i, right_labels[i], va='center', ha='center', color='black')
    other_ax.text(95, i, right_labels[i], va='center', ha='center', color='black')

# Y축 설정
total_ax.set_yticks(y)
total_ax.set_yticklabels(labels)
self_ax.set_yticks(y)
self_ax.set_yticklabels(labels)
other_ax.set_yticks(y)
other_ax.set_yticklabels(labels)

# 기타 설정
total_ax.invert_yaxis()
total_ax.set_xlabel('Percentage')
total_ax.set_title(f'TOTAL : {total_mbti}')

self_ax.invert_yaxis()
self_ax.set_xlabel('Percentage')
self_ax.set_title(f'SELF : {self_mbti["mbti"]}')

other_ax.invert_yaxis()
other_ax.set_xlabel('Percentage')
other_ax.set_title(f'OTHER : {other_mbti}')


# Streamlit에 그래프 표시
st.pyplot(total_graph)
st.pyplot(self_graph)
st.pyplot(other_graph)


if st.button("다시 분석 하러가기", type="primary"):
    # st.session_state의 특정값들을 삭제해서 chat 페이지로 돌아갔을 때, 상태 초기화
    del st.session_state.messages
    del st.session_state['remaining_users']
    del st.session_state.participant
    del st.session_state.mbti

    st.switch_page("pages/chat.py")