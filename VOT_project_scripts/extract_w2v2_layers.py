# extract_w2v2_layers.py  -  based on the course tutorial speech_recognition_pipeline_tutorial.py
# Run it in the folder that contains the speaker .wav files and tokens.txt
import torch, torchaudio, pandas as pd

bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H      # same model as in the course tutorial
model = bundle.get_model().eval()

tokens = pd.read_csv("tokens.txt", sep="\t")              # made by measure_tokens.praat
tokens = tokens[tokens["clLabel"] != "CHECK_LABELS"]

FRAME = 0.02                                              # wav2vec2 gives one vector every 20 ms
rows = []
for spk, tok in tokens.groupby("file"):
    waveform, sr = torchaudio.load(f"{spk}.wav")
    waveform = waveform.mean(dim=0, keepdim=True)         # make sure the sound is mono
    if sr != bundle.sample_rate:                          # the model needs 16 kHz
        waveform = torchaudio.functional.resample(waveform, sr, bundle.sample_rate)
    with torch.inference_mode():
        features, _ = model.extract_features(waveform)   # list with one tensor per layer
    for _, t in tok.iterrows():
        first = int(t["clStart"] / FRAME)                 # from the start of the closure
        last = int((t["vStart"] + 0.05) / FRAME)          # to 50 ms into the vowel
        for layer, f in enumerate(features, start=1):
            vec = f[0, first:last + 1, :].mean(dim=0)     # average over frames -> 768 numbers
            rows.append([spk, t["word"], layer] + vec.tolist())

out = pd.DataFrame(rows)
out.columns = ["file", "word", "layer"] + [f"d{i}" for i in range(1, out.shape[1] - 2)]
out.to_csv("w2v2_layers.csv", index=False)
print("Done:", out.shape)
