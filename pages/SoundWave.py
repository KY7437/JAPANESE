import streamlit as st
import librosa
import numpy as np
import matplotlib.pyplot as plt

st.title("🔊 Soundwave Comparison")

native_file = st.file_uploader("원어민 발음 업로드", type=["wav"], key="native")
learner_file = st.file_uploader("학습자 발음 업로드", type=["wav"], key="learner")

def plot_wave(y, sr, label):
    t = np.linspace(0, len(y) / sr, len(y))
    plt.plot(t, y, label=label, alpha=0.8)

if native_file and learner_file:
    y_n, sr_n = librosa.load(native_file, sr=None)
    y_l, sr_l = librosa.load(learner_file, sr=None)

    fig, ax = plt.subplots(figsize=(10, 4))
    plot_wave(y_n, sr_n, "Native")
    plot_wave(y_l, sr_l, "Learner")

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.legend()
    ax.set_title("Soundwave Comparison")

    st.pyplot(fig)
else:
    st.info("원어민과 학습자 음성 파일을 모두 업로드하세요.")
