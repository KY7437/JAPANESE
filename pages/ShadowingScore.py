import streamlit as st
import librosa
import numpy as np
import matplotlib.pyplot as plt
import parselmouth

from utils.tts import generate_tts

st.header("🎯 Shadowing Score")

st.write("""
원어민 발음을 듣고 **섀도잉**한 뒤,
리듬 · 강세 · 발음을 종합해 점수를 매깁니다.
""")

# ---------- 입력 ----------
text = st.text_input("일본어 문장을 입력하세요")

if st.button("원어민 음성 생성"):
    generate_tts(text, "native.wav")
    st.audio("native.wav")

audio = st.audio_input("섀도잉 해보세요")

if audio:
    with open("learner.wav", "wb") as f:
        f.write(audio.getbuffer())
    st.audio("learner.wav")

# ---------- 분석 함수 ----------
def duration_score(n_dur, l_dur):
    ratio = l_dur / n_dur
    return max(0, 30 - abs(1 - ratio) * 60)

def energy_score(n_y, l_y):
    n_rms = librosa.feature.rms(y=n_y)[0]
    l_rms = librosa.feature.rms(y=l_y)[0]
    min_len = min(len(n_rms), len(l_rms))
    corr = np.corrcoef(n_rms[:min_len], l_rms[:min_len])[0,1]
    return max(0, corr * 30)

def formant_score(n_wav, l_wav):
    def avg_f1f2(wav):
        snd = parselmouth.Sound(wav)
        f = snd.to_formant_burg()
        times = np.arange(0, snd.duration, 0.02)
        f1, f2 = [], []
        for t in times:
            f1.append(f.get_value_at_time(1, t))
            f2.append(f.get_value_at_time(2, t))
        return np.nanmean(f1), np.nanmean(f2)

    f1n, f2n = avg_f1f2(n_wav)
    f1l, f2l = avg_f1f2(l_wav)

    dist = abs(f1n - f1l) + abs(f2n - f2l)
    score = max(0, 40 - dist / 50)
    return score

# ---------- 점수 계산 ----------
if st.button("섀도잉 점수 계산"):
    y_n, sr = librosa.load("native.wav", sr=None)
    y_l, _ = librosa.load("learner.wav", sr=sr)

    d_score = duration_score(len(y_n)/sr, len(y_l)/sr)
    e_score = energy_score(y_n, y_l)
    f_score = formant_score("native.wav", "learner.wav")

    total = d_score + e_score + f_score

    st.subheader("📊 결과")

    st.metric("⏱️ 리듬 점수", f"{d_score:.1f} / 30")
    st.metric("🌊 강세 점수", f"{e_score:.1f} / 30")
    st.metric("📊 발음 점수", f"{f_score:.1f} / 40")

    st.markdown(f"## 🏆 총점: **{total:.1f} / 100**")

    if total >= 85:
        st.success("원어민과 매우 유사한 섀도잉입니다 👍")
    elif total >= 70:
        st.info("전반적으로 좋지만 리듬/발음을 더 다듬어보세요.")
    else:
        st.warning("속도와 모음 발음을 다시 연습해보세요.")
