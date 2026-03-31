import streamlit as st
import parselmouth
import numpy as np
import matplotlib.pyplot as plt

from utils.tts import generate_tts

st.header("📊 Formants")

# ---------- 입력 ----------
text = st.text_input("일본어 단어 또는 문장")

if st.button("원어민 음성 생성"):
    generate_tts(text, "native.wav")
    st.audio("native.wav")

# ---------- 학습자 녹음 ----------
audio = st.audio_input("같이 읽어보세요")

if audio:
    with open("learner.wav", "wb") as f:
        f.write(audio.getbuffer())
    st.audio("learner.wav")

# ---------- Formant 함수 ----------
def extract_formants(wav):
    snd = parselmouth.Sound(wav)
    formant = snd.to_formant_burg()

    times = np.arange(0, snd.duration, 0.01)
    f1, f2, f3 = [], [], []

    for t in times:
        f1.append(formant.get_value_at_time(1, t))
        f2.append(formant.get_value_at_time(2, t))
        f3.append(formant.get_value_at_time(3, t))

    return times, f1, f2, f3

# ---------- 분석 ----------
if st.button("Formants 비교"):
    tn, f1n, f2n, f3n = extract_formants("native.wav")
    tl, f1l, f2l, f3l = extract_formants("learner.wav")

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.plot(tn, f2n, color="#5DADE2", label="Native F2")
    ax.plot(tl, f2l, color="#F5B041", label="Learner F2", alpha=0.8)

    ax.set_title("F2 Comparison (혀 위치 차이)")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Frequency (Hz)")
    ax.legend()

    st.pyplot(fig)
