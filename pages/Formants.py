import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("🎤 Formants Curve Viewer")

st.markdown("F1–F2 포먼트 **곡선 형태 시각화 예시**입니다.")

# 예시 포먼트 데이터
f1 = np.array([300, 400, 500, 600, 700])
f2 = np.array([2200, 2000, 1800, 1600, 1400])

fig, ax = plt.subplots()
ax.plot(f2, f1, marker="o")
ax.invert_xaxis()
ax.invert_yaxis()

ax.set_xlabel("F2 (Hz)")
ax.set_ylabel("F1 (Hz)")
ax.set_title("Formant Curve")

st.pyplot(fig)
