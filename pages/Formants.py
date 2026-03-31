import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import parselmouth
from gtts import gTTS
from audio_recorder_streamlit import audio_recorder
import tempfile

st.title("🎯 Pronunciation Practice – Formants")

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

# ---------- Formant Extraction ----------
def get_formants(path):
    snd = parselmouth.Sound(path)
    formant = snd.to_formant_burg()
    times = np.linspace(0, snd.duration, 100)
    f1, f2 = [], []

    for t in times:
        f1.append(formant.get_value_at_time(1, t))
        f2.append(formant.get_value_at_time(2, t))

    return f1, f2

# ---------- Comparison ----------
if "tts_path" in st.session_state and "learner_path" in st.session_state:
    f1_t, f2_t = get_formants(st.session_state["tts_path"])
    f1_l, f2_l = get_formants(st.session_state["learner_path"])

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(f2_t, f1_t, label="Native (TTS)")
    ax.plot(f2_l, f1_l, label="Learner")

    ax.set_xlabel("F2 (Hz)")
    ax.set_ylabel("F1 (Hz)")
    ax.invert_xaxis()
    ax.invert_yaxis()
    ax.legend()
    ax.set_title("Formant Space Comparison")

    st.pyplot(fig)
