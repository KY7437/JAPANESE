import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("🎤 Formants Viewer (Demo)")
st.write("실제 음성 없이 포먼트 분포 형태만 시각화한 예시입니다.")

# 예시 포먼트 데이터 (Hz)
f1 = np.array([300, 400, 500, 600, 700])
f2 = np.array([2300, 2100, 1900, 1700, 1500])

fig, ax = plt.subplots()
ax.scatter(f2, f1)
ax.plot(f2, f1)

ax.invert_xaxis()
ax.invert_yaxis()

ax.set_xlabel("F2 (Hz)")
ax.set_ylabel("F1 (Hz)")
ax.set_title("Formant Curve Example")

st.pyplot(fig)
