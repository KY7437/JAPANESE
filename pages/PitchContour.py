import streamlit as st
import librosa
import numpy as np
import matplotlib.pyplot as plt

from utils.tts import generate_tts

st.header("📈 Pitch Contour (고저 패턴)")

st.write("""
일본어는 **고저 악센트 언어**입니다.  
피치(F0) 곡선의 **상승·하강 흐름**을 비교해보세요.
""")

# ---------- 입력 ----------
text = st.text_input("일본어 단어 또는 문장")

if st.button("원어민 음성 생성"):
    generate_tts(text, "native.wav")
    st.audio("native.wav")

audio = st.audio_input("같이 읽어보세요")

if audio:
    with open("learner.wav", "wb") as f:
        f.write(audio.getbuffer())
    st.audio("learner.wav")

# ---------- 피치 추출 ----------
def get_pitch(y, sr):
    f0 = librosa.yin(
        y,
        fmin=70,
        fmax=300,
        sr=sr
    )
    times = np.linspace(0, len(y)/sr, len(f0))
    return times, f0

# ---------- 분석 ----------
if st.button("억양 비교"):
    y_n, sr = librosa.load("native.wav", sr=None)
    y_l, _ = librosa.load("learner.wav", sr=sr)

    tn, f0n = get_pitch(y_n, sr)
    tl, f0l = get_pitch(y_l, sr)

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.plot(tn, f0n, color="#5DADE2", label="Native", alpha=0.8)
    ax.plot(tl, f0l, color="#F5B041", label="Learner", alpha=0.8)

    ax.set_title("Pitch Contour Comparison")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Pitch (Hz)")
    ax.legend()

    st.pyplot(fig)

    # 간단 피드백
    if np.nanstd(f0l) < np.nanstd(f0n) * 0.6:
        st.warning("⚠️ 억양 변화가 적습니다 (평탄한 발음)")
    else:
        st.success("✅ 억양 변화가 잘 나타납니다")
