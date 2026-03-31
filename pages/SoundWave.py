import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("🔊 Sound Wave Viewer")

st.markdown("음성 신호를 **파형(curve)** 으로 시각화합니다.")

# 더미 신호 (녹음 없이도 실행되게)
sr = 22050
t = np.linspace(0, 1, sr)
wave = 0.5 * np.sin(2 * np.pi * 220 * t)

fig, ax = plt.subplots()
ax.plot(t, wave)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")

st.pyplot(fig)
