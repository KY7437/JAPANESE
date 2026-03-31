import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
from gtts import gTTS
from audio_recorder_streamlit import audio_recorder
import soundfile as sf
import tempfile

st.title("🎯 Pronunciation Practice – Spectral Shape")

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

# ---------- Spectral Curve ----------
def spectral_curve(path):
    y, sr = sf.read(path)
    f, t, Sxx = spectrogram(y, sr)
    curve = np.mean(Sxx, axis=1)
    return f, curve

# ---------- Comparison ----------
if "tts_path" in st.session_state and "learner_path" in st.session_state:
    f_t, c_t = spectral_curve(st.session_state["tts_path"])
    f_l, c_l = spectral_curve(st.session_state["learner_path"])

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(f_t, c_t, label="Native (TTS)")
    ax.plot(f_l, c_l, label="Learner")

    ax.set_xlim(0, 4000)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Energy")
    ax.legend()
    ax.set_title("Spectral Shape Comparison")

    st.pyplot(fig)
