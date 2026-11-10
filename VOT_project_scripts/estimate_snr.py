# estimate_snr.py - rough signal-to-noise ratio of each recording (for the Method section and as a covariate)
# Run it in the folder with the .wav files:  python3 estimate_snr.py
# It cuts each file into 25 ms frames and compares the loudest frames (95th percentile, speech)
# with the quietest frames (5th percentile, background noise in the pauses). Higher = cleaner recording.
import glob
import wave

import numpy as np

print("file,noise_floor_dB,speech_dB,snr_dB")
for f in sorted(glob.glob("*.wav")):
    w = wave.open(f)
    sr, n = w.getframerate(), w.getnframes()
    x = np.frombuffer(w.readframes(n), dtype=np.int16).astype(float) / 32768
    w.close()
    hop = int(0.025 * sr)
    frames = x[: len(x) // hop * hop].reshape(-1, hop)
    db = 10 * np.log10((frames ** 2).mean(axis=1) + 1e-12)
    noise, speech = np.percentile(db, 5), np.percentile(db, 95)
    print(f"{f[:-4]},{noise:.1f},{speech:.1f},{speech - noise:.1f}")
