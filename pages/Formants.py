import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import parselmouth

st.title("🎯 Formants Comparison (F1 / F2)")

native_file = st.file_uploader("원어민 발음 업로드", type=["wav"], key="native_f")
learner_file = st.file_uploader("학습자 발음 업로드", type=["wav"], key="learner_f")

def extract_formants(file):
    snd = parselmouth.Sound(file)
    formant = snd.to_formant_burg()

    times = np.linspace(0, snd.duration, 100)
    f1, f2 = [], []

    for t in times:
        f1.append(formant.get_value_at_time(1, t))
        f2.append(formant.get_value_at_time(2, t))

    return times, f1, f2

if native_file and learner_file:
    t_n, f1_n, f2_n = extract_formants(native_file)
    t_l, f1_l, f2_l = extract_formants(learner_file)

    fig, ax = plt.subplots(figsize=(6, 6))

    ax.plot(f2_n, f1_n, label="Native", alpha=0.8)
    ax.plot(f2_l, f1_l, label="Learner", alpha=0.8)

    ax.set_xlabel("F2 (Hz)")
    ax.set_ylabel("F1 (Hz)")
    ax.invert_xaxis()
    ax.invert_yaxis()
    ax.legend()
    ax.set_title("Formant Space Comparison")

    st.pyplot(fig)
else:
    st.info("원어민과 학습자 음성을 모두 업로드하세요.")
