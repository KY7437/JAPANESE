import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
from gtts import gTTS
import tempfile

st.set_page_config(page_title="일본어 발음 파형 비교", layout="centered")

st.title("🎧 일본어 발음 파형 비교")
st.write("원어 음성과 학습자 음성의 **파형(waveform)** 을 비교합니다.")

# -----------------------------
# 1. 일본어 문장 입력
# -----------------------------
jp_text = st.text_area(
    "🇯🇵 일본어 문장을 입력하세요",
    "こんにちは。私は日本語を勉強しています。"
)

# -----------------------------
# 2. TTS 생성
# -----------------------------
if st.button("🔊 원어 음성 생성"):
    tts = gTTS(text=jp_text, lang="ja")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        tts.save(f.name)
        st.session_state["tts_path"] = f.name

    st.success("원어 음성 생성 완료!")

# -----------------------------
# 3. 원어 음성 파형
# -----------------------------
if "tts_path" in st.session_state:
    st.subheader("📈 원어 음성 파형")
    y_native, sr_native = sf.read(st.session_state["tts_path"])

    fig, ax = plt.subplots(facecolor="#F7F7F7")
    ax.set_facecolor("#F7F7F7")
    ax.plot(y_native, color="#4C72B0", linewidth=1.2)
    ax.set_title("Native Speaker (TTS)")
    ax.set_xlabel("Time")
    ax.set_ylabel("Amplitude")

    st.pyplot(fig)
    st.audio(st.session_state["tts_path"])

# -----------------------------
# 4. 학습자 녹음
# -----------------------------
st.subheader("🎙️ 학습자 녹음")
audio_input = st.audio_input("버튼을 눌러 녹음하세요")

# -----------------------------
# 5. 학습자 파형
# -----------------------------
if audio_input is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio_input.getvalue())
        learner_path = f.name

    y_learner, sr_learner = sf.read(learner_path)

    st.subheader("📉 학습자 음성 파형")
    fig2, ax2 = plt.subplots(facecolor="#F7F7F7")
    ax2.set_facecolor("#F7F7F7")
    ax2.plot(y_learner, color="#55A868", linewidth=1.2)
    ax2.set_title("Learner")
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Amplitude")

    st.pyplot(fig2)
    st.audio(learner_path)

    # -----------------------------
    # 6. 겹쳐진 파형 비교
    # -----------------------------
    if "tts_path" in st.session_state:
        st.subheader("🔍 원어 vs 학습자 파형 겹쳐보기")

        # 길이 맞추기 (짧은 쪽 기준)
        min_len = min(len(y_native), len(y_learner))
        y_n = y_native[:min_len]
        y_l = y_learner[:min_len]

        # 정규화 (진폭 비교용)
        y_n = y_n / np.max(np.abs(y_n))
        y_l = y_l / np.max(np.abs(y_l))

        fig3, ax3 = plt.subplots(facecolor="#F7F7F7")
        ax3.set_facecolor("#F7F7F7")

        ax3.plot(
            y_n,
            label="Native (TTS)",
            color="#4C72B0",
            alpha=0.75,
            linewidth=1.2
        )
        ax3.plot(
            y_l,
            label="Learner",
            color="#DD8452",
            alpha=0.75,
            linewidth=1.2
        )

        ax3.set_title("Overlaid Waveform Comparison")
        ax3.set_xlabel("Time")
        ax3.set_ylabel("Normalized Amplitude")
        ax3.legend()

        st.pyplot(fig3)

        st.info(
            "🔎 **해석 포인트**\n"
            "- 파형이 작으면 → 발음 에너지 부족\n"
            "- 피크 위치가 다르면 → 리듬·모라 타이밍 차이\n"
            "- 전체 모양이 다르면 → 억양/장단 차이"
        )
