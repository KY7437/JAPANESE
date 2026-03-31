import streamlit as st
import librosa
import numpy as np

from utils.tts import generate_tts

st.header("⏱️ Japanese Rhythm Checker")

st.write("""
일본어는 **모라 타이밍 언어**입니다.  
전체 길이가 아니라 **모라 하나당 걸리는 시간**을 비교합니다.
""")

# ---------- 입력 ----------
text = st.text_input("일본어 문장을 입력하세요 (히라가나 권장)")

if st.button("원어민 음성 생성"):
    generate_tts(text, "native.wav")
    st.audio("native.wav")

audio = st.audio_input("같이 읽어보세요")

if audio:
    with open("learner.wav", "wb") as f:
        f.write(audio.getbuffer())
    st.audio("learner.wav")

# ---------- 모라 수 추정 ----------
def count_mora(text):
    small = "ゃゅょぁぃぅぇぉ"
    mora = 0
    for ch in text:
        if ch in small:
            continue
        mora += 1
    return mora

# ---------- 분석 ----------
if st.button("리듬 분석"):
    y_n, sr = librosa.load("native.wav", sr=None)
    y_l, _ = librosa.load("learner.wav", sr=sr)

    mora = count_mora(text)

    dur_n = len(y_n) / sr
    dur_l = len(y_l) / sr

    mora_time_n = dur_n / mora * 1000
    mora_time_l = dur_l / mora * 1000

    diff = mora_time_l - mora_time_n

    st.subheader("📊 결과")

    st.metric("원어민 모라당 시간", f"{mora_time_n:.0f} ms")
    st.metric("학습자 모라당 시간", f"{mora_time_l:.0f} ms")

    if abs(diff) < 30:
        st.success("✅ 일본어다운 리듬입니다!")
    elif diff > 0:
        st.warning("⏳ 모라가 늘어집니다 → 발화가 느립니다")
    else:
        st.warning("⚡ 모라가 짧습니다 → 발화가 빠릅니다")
