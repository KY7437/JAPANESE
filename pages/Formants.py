import librosa
import numpy as np
import matplotlib.pyplot as plt

y, sr = librosa.load("audio.wav", sr=None)

# 프레임 단위 분할
frame_length = int(0.025 * sr)
hop_length = int(0.010 * sr)

formants = []

for i in range(0, len(y) - frame_length, hop_length):
    frame = y[i:i+frame_length]

    # LPC
    lpc = librosa.lpc(frame, order=12)
    roots = np.roots(lpc)
    roots = roots[np.imag(roots) >= 0]

    angles = np.angle(roots)
    freqs = angles * (sr / (2 * np.pi))
    freqs = np.sort(freqs)

    if len(freqs) >= 2:
        formants.append(freqs[:2])  # F1, F2

formants = np.array(formants)

# 시각화
plt.plot(formants[:,0], label="F1")
plt.plot(formants[:,1], label="F2")
plt.ylabel("Frequency (Hz)")
plt.xlabel("Time frame")
plt.legend()
plt.show()
