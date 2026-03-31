import streamlit as st
import librosa
import librosa.display
import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np

from utils.tts import generate_tts

st.header("🌊 SoundWaves")

# ---------- 입력 ----------
text = st.text_input("일본어 문장을 입력하세요")

if st.button("원어민 음성 생성"):
    generate_tts(text, "native.wav")
    st.audio("native.wav")

# ---------- 학습자 녹음 ----------
audio = st.audio_input("같은 문장을 읽어보세요")

if audio:
    with open("learner.wav", "wb") as f:
        f.write(audio.getbuffer())
    st.audio("learner.wav")

# ---------- 분석 ----------
if st.button("파동 분석"):
    y_n, sr = librosa.load("native.wav", sr=None)
    y_l, _ = librosa.load("learner.wav", sr=sr)

    # 원어민
    st.subheader("원어민 파동")
    fig, ax = plt.subplots(figsize=(10, 3))
    librosa.display.waveshow(y_n, sr=sr, ax=ax, color="#5DADE2")
    ax.set_xticks([])
    ax.set_yticks([])
    st.pyplot(fig)

    # 학습자
    st.subheader("학습자 파동")
    fig, ax = plt.subplots(figsize=(10, 3))
    librosa.display.waveshow(y_l, sr=sr, ax=ax, color="#F5B041")
    ax.set_xticks([])
    ax.set_yticks([])
    st.pyplot(fig)

    # 겹치기
    st.subheader("겹친 파동 (비교)")
    fig, ax = plt.subplots(figsize=(10, 3))
    librosa.display.waveshow(y_n, sr=sr, ax=ax, color="#5DADE2", alpha=0.7, label="Native")
    librosa.display.waveshow(y_l, sr=sr, ax=ax, color="#F5B041", alpha=0.7, label="Learner")
    ax.legend()
    ax.set_xticks([])
    ax.set_yticks([])
    st.pyplot(fig)
