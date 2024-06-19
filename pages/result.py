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

# if "mbti" not in st.session_state:
#     st.session_state.mbti = []

# for data in st.session_state.participant:
#     mbti, ratios = find_mbti(data["result"])
#     # if 'E' in ratios:
#     #     E_value = ratios['E']
#     #     I_value = 100 - E_value
#     # else:
#     #     I_value = ratios['I']
#     #     E_value = 100 - I_value
#     # if 'S' in ratios:
#     #     S_value = ratios['S']
#     #     N_value = 100 - S_value
#     # else:
#     #     N_value = ratios['N']
#     #     S_value = 100 - N_value
#     # if 'T' in ratios:
#     #     T_value = ratios['T']
#     #     F_value = 100 - T_value
#     # else:
#     #     F_value = ratios['F']
#     #     T_value = 100 - F_value
#     # if 'P' in ratios:
#     #     P_value = ratios['P']
#     #     J_value = 100 - P_value
#     # else:
#     #     J_value = ratios['J']
#     #     P_value = 100 - J_value

#     st.session_state.mbti.append()
#     st.markdown(f"{data['name']}님의 분석결과")
#     st.markdown(f"MBTI: {mbti}")
#     st.markdown("비율:")
#     for key, value in ratios.items():
#         st.markdown(f"{key}: {value}%")

     
#### 임시 ####
# 예제 데이터
labels = ['E / I', 'S / N', 'T / F', 'P / J']
left_values = [68, 56, 51, 63]
right_values = [32, 44, 49, 37]
left_labels= ['I', 'S', 'F', 'P']
right_labels = ['E', 'N', 'T', 'J']
colors = ['#4daf8b', '#ffaf40', '#92c657', '#d86f98']

# 그래프 그리기
fig, ax = plt.subplots(figsize=(9, 2))

# 양쪽에 막대그래프 그리기
y = np.arange(len(labels))
ax.barh(y, left_values, color=colors, edgecolor='none')
ax.barh(y, right_values, left=left_values, color='lightgrey', edgecolor='none')

# 각 항목의 값을 텍스트로 표시
# 1번 예시
for i in range(len(labels)):
    # 메인 mbti 비중
    ax.text(left_values[i] - 5, i, f'{left_values[i]}%', va='center', ha='right', color='black', fontweight='bold')
    # 서브 mbti 비중
    ax.text(left_values[i] + right_values[i] - 5, i, f'{right_values[i]}%', va='center', ha='left', color='black', fontweight='bold')
    # 메인 mbti 유형
    # ax.text(left_values[i] / 2, i, left_labels[i], va='center', ha='center', color='black')
    # 서브 mbti 유형
    # ax.text(left_values[i] + right_values[i] / 2, i, right_labels[i], va='center', ha='center', color='black')

# Y축 설정
ax.set_yticks(y)
ax.set_yticklabels(labels)

# 기타 설정
ax.invert_yaxis()
ax.set_xlabel('Percentage')
ax.set_title('MBTI')

# Streamlit에 그래프 표시
st.pyplot(fig)


if st.button("다시 분석 하러가기", type="primary"):
    # st.session_state의 특정값들을 삭제해서 chat 페이지로 돌아갔을 때, 상태 초기화
    del st.session_state.messages
    del st.session_state['remaining_users']
    del st.session_state.participant
    del st.session_state.mbti

    st.switch_page("pages/chat.py")