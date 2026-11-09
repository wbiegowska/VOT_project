# Voicing in Polish- and Persian-accented English

Weronika Biegowska & Ala Karamkesh · M2, Université Paris Cité
Course project for SL9CE065 *Signal Processing and Computational Methods for Speech* (2026)

## Research question

Do Polish and Persian speakers carry the voicing system of their first language into English,
compared with native American English speakers? We examine the voicing contrast
(/p t k/ vs /b g/) through multiple acoustic correlates rather than VOT alone, and test how well
wav2vec2 representations capture it.

- **English and Persian** aspirate /p t k/ (long VOT).
- **Polish** does not aspirate /p t k/ (short VOT) and prevoices /b d g/ (voicing during the closure).
- If only the Polish speakers differ from the English speakers, this points to transfer from Polish
  rather than a general effect of being a non-native speaker.

## Data

- **Speech Accent Archive** (George Mason University, https://accent.gmu.edu): lossless FLAC
  recordings on OSF, https://osf.io/e2j5y. Licence: CC BY-NC-SA 4.0.
- **30 speakers**: 10 Polish, 10 Persian, 10 American English (6 women and 4 men per group).
  Polish and Persian speakers are matched on age of starting English and years in an
  English-speaking country. Full list: [`00_admin/speakers.csv`](00_admin/speakers.csv).
- Everyone reads the same paragraph ([`00_admin/paragraph.txt`](00_admin/paragraph.txt)).
- **Target words**: *peas, call, toy, kids* (voiceless) and *Bob, big, bags, go* (voiced):
  8 words × 30 speakers = **240 tokens**.
- **The audio is not stored in this repository** (see *Getting the audio*).

## Measures

| Type | Measures |
|---|---|
| Durations | VOT, closure duration |
| Voicing | proportion of voicing in the closure |
| Vowel onset | f0 and F1 at 10% vs 50% of the vowel |
| Voice quality | HNR, CPP, spectral tilt, Hammarberg index (and more from the VQ script) |
| Automatic | OpenSMILE eGeMAPS functionals (88 features), wav2vec2 layer representations |

## Repository structure

```
00_admin/               speakers.csv, paragraph.txt, annotation_log.csv
00_admin/private/       teacher's paper, feedback, course files (NOT uploaded: ignored by Git)
01_flac/                downloaded FLAC files (ignored by Git)
02_webmaus_original/    TextGrids exactly as WebMAUS made them (never edit)
03_annotated/           working folder: .wav (ignored) + annotated .TextGrid + tokens.txt
04_reliability/         re-annotated speakers for the inter-annotator check
05_python/              Python outputs (egemaps_tokens.csv; w2v2_layers.csv is ignored, too large)
06_R/                   R outputs and the R Markdown file
07_figures/             figures for the report and the slides
08_report/              lab report drafts
09_slides/              presentation
VOT_project_scripts/    all scripts (see Pipeline)
```

## Getting the audio

1. Download each speaker's FLAC file from https://osf.io/e2j5y into `01_flac/`.
2. Rename it to the `file` column of `speakers.csv`, e.g. `polish3.flac` → `PL_F_polish3.flac`
   (the scripts read the group and the sex from the file name).
3. Copy the FLAC files into `03_annotated/` and run
   `VOT_project_scripts/convert_flac_to_wav.praat` on that folder.

Audio files (`*.wav`, `*.flac`, `*.mp3`) are ignored by Git, so they stay on your computer only.

## Pipeline

1. **Forced alignment**: WebMAUS Basic, language English (US), output Praat TextGrid.
   Keep one copy in `02_webmaus_original/` and one in `03_annotated/`.
2. **Manual annotation** in Praat: an interval tier `seg` with three touching intervals per target
   word, `cl` (closure; `cl?` if its start is unclear), `rel` (burst to voicing onset) and
   `v` (vowel).
3. **Measurements**: `VOT_project_scripts/measure_tokens.praat` on `03_annotated/`
   → `tokens.txt`, plus the folders `vowels/` and `tokens/`.
4. **Voice quality**: the course script `VQ_measurements_V2.praat` (Jalal Al-Tamimi) run unchanged
   on `03_annotated/vowels/` → `VQResults2.xls`.
5. **Automatic features** (Python): `extract_egemaps.py` and `extract_w2v2_layers.py`.
6. **Statistics** (R): `analysis.R`: mixed-effects models, PCA, k-means, Random Forests
   (all cues vs VOT only, per group; wav2vec2 layers; eGeMAPS).

## Requirements

- **Praat 6.4 or newer** (the course scripts require it).
- **R** with `dplyr`, `readr`, `ggplot2`, `purrr`, `lme4`, `FactoMineR`, `factoextra`, `party`,
  `pROC` (`varImp` optional).
- **Python 3**: `pip install -r requirements.txt` (torch/torchaudio 2.7.0 as in the course tutorial).

## Working together

- **Pull** before you start working, **commit and push** when you stop.
- Each speaker's TextGrid has **one owner** (`owner` column in `speakers.csv`). Never edit the other
  person's TextGrid: this avoids merge conflicts.
- Never commit course materials (slides, the course book, the teacher's paper) or private
  feedback. Put them in `00_admin/private/`, which Git ignores.

## Credits

- Two-pass f0 estimation, voicing detection and voice-quality measures follow the course scripts by
  Jalal Al-Tamimi:
  [Praat-f0-Accurate-Estimation](https://github.com/JalalAl-Tamimi/Praat-f0-Accurate-Estimation),
  [Praat-Voicing-detection](https://github.com/JalalAl-Tamimi/Praat-Voicing-detection),
  [Praat-VQ-Measurements](https://jalalal-tamimi.github.io/Praat-VQ-Measurements/)
  (cite Al-Tamimi & Khattab 2015, 2018).
- Forced alignment: WebMAUS (BAS Web Services, LMU Munich).
- wav2vec2 features: based on the torchaudio speech-recognition tutorial (course version).
- OpenSMILE / eGeMAPS: Eyben et al. (2010, 2016).
- Statistics: Al-Tamimi (2025), *Statistics for Linguists using R*.
- Some starter scripts in `VOT_project_scripts/` were drafted with the help of an AI assistant.

## Licence

- Code: MIT (see [`LICENSE`](LICENSE)).
- Annotations and data derived from the Speech Accent Archive: CC BY-NC-SA 4.0, like the original
  recordings.
