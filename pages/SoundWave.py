import streamlit as st
import numpy as np
import librosa
import matplotlib.pyplot as plt
from gtts import gTTS
import soundfile as sf
from audio_recorder_streamlit import audio_recorder
import tempfile

st.title("🔊 Pronunciation Practice – Soundwave")

text = st.text_input("일본어 발음 연습 문장 입력", "こんにちは")

# ---------- TTS ----------
if st.button("원어민 발음 생성 (TTS)"):
    tts = gTTS(text=text, lang="ja")
    tts_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    tts.save(tts_file.name)
    st.audio(tts_file.name)

    st.session_state["tts_path"] = tts_file.name

# ---------- Recording ----------
st.markdown("### 🎙️ 학습자 녹음")
audio_bytes = audio_recorder(text="녹음 시작 / 중지")

if audio_bytes:
    learner_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    with open(learner_file.name, "wb") as f:
        f.write(audio_bytes)

    st.audio(learner_file.name)
    st.session_state["learner_path"] = learner_file.name

# ---------- Comparison ----------
if "tts_path" in st.session_state and "learner_path" in st.session_state:
    y_t, sr_t = librosa.load(st.session_state["tts_path"], sr=None)
    y_l, sr_l = librosa.load(st.session_state["learner_path"], sr=None)

    fig, ax = plt.subplots(figsize=(10, 4))
    t1 = np.linspace(0, len(y_t) / sr_t, len(y_t))
    t2 = np.linspace(0, len(y_l) / sr_l, len(y_l))

    ax.plot(t1, y_t, label="Native (TTS)", alpha=0.7)
    ax.plot(t2, y_l, label="Learner", alpha=0.7)

    ax.set_title("Soundwave Comparison")
    ax.legend()
    st.pyplot(fig)
