# Inter-annotator agreement (reliability check, N4 / R8)

Made by `VOT_project_scripts/reliability.py` from the `seg` tiers only (no audio). Original = the owner's TextGrid in `03_annotated`; re-annotation = the other annotator's blind version in `04_reliability/calibration_A` (Ala) or `calibration_W` (Weronika). Differences are **re-annotation − original**, in ms. All 4 files follow `00_admin/annotation_rules.md`.

| file | original by | re-annotated by | tokens |
|---|---|---|---|
| EN_M_english102 | Weronika | Ala | 8 |
| FA_F_farsi10 | Weronika | Ala | 7 |
| FA_F_farsi8 | Ala | Weronika | 8 |
| PL_M_polish21 | Ala | Weronika | 8 |

**31 tokens** compared (13% of the 240 tokens).
Left out: FA_F_farsi10 *bags*: WebMAUS had put 'bags' about 1.5 s too early, on 'into'; Weronika's first version followed WebMAUS, Ala's was on the real 'bags'. Weronika's file was then corrected to Ala's word (25 Nov), so the two versions are no longer independent.

## 1. Durations (the measures that go into the analysis)

MAD = mean absolute difference; bias = mean signed difference; LoA = 95% limits of agreement (bias ± 1.96 SD); ICC = ICC(A,1), two-way random, absolute agreement, single rater, with 95% CI.

| measure | tokens | n | MAD | median AD | max AD | ≤5 ms | ≤10 ms | bias | LoA | r | ICC [95% CI] |
|---|---|---|---|---|---|---|---|---|---|---|---|
| VOT | all | 31 | 10.7 | 9.2 | 23.0 | 19% | 52% | -4.1 | -27.2 to 19.0 | 0.92 | 0.92 [0.83, 0.96] |
| VOT | voiceless (p t k) | 16 | 10.8 | 10.2 | 21.4 | 12% | 50% | -1.2 | -25.6 to 23.1 | 0.93 | 0.93 [0.81, 0.97] |
| VOT | voiced (b g) | 15 | 10.5 | 9.2 | 23.0 | 27% | 53% | -7.2 | -28.1 to 13.8 | 0.42 | 0.31 [-0.12, 0.68] |
| closure | both cl (used in R) | 21 | 18.4 | 12.6 | 75.5 | 24% | 33% | 15.1 | -28.0 to 58.1 | 0.68 | 0.59 [0.15, 0.82] |
| closure | all | 31 | 17.7 | 11.9 | 75.5 | 35% | 42% | 12.9 | -31.6 to 57.5 | 0.80 | 0.76 [0.47, 0.89] |
| vowel | all | 31 | 30.5 | 13.9 | 214.5 | 16% | 29% | -16.5 | -115.3 to 82.2 | 0.87 | 0.80 [0.63, 0.90] |
| vowel | voiceless (p t k) | 16 | 32.4 | 14.8 | 214.5 | 25% | 31% | -21.6 | -135.2 to 91.9 | 0.86 | 0.75 [0.43, 0.91] |
| vowel | voiced (b g) | 15 | 28.5 | 13.9 | 128.6 | 7% | 27% | -11.1 | -93.8 to 71.6 | 0.90 | 0.87 [0.66, 0.95] |

**Voicing proportion in the closure** (0 = silent closure, 1 = voiced all the way; measured by `measure_tokens.praat` on each annotator's boundaries, so differences come only from where B1 and B2 were put). MAD and bias are in proportion units.

| tokens | n | MAD | median AD | max AD | within 0.1 | bias | LoA | r | ICC [95% CI] |
|---|---|---|---|---|---|---|---|---|---|
| both cl (used in R) | 21 | 0.068 | 0.000 | 0.317 | 71% | 0.037 | -0.19 to 0.27 | 0.96 | 0.96 [0.90, 0.98] |
| voiceless (p t k) | 13 | 0.077 | 0.039 | 0.273 | 69% | 0.027 | -0.22 to 0.27 | 0.91 | 0.91 [0.73, 0.97] |
| voiced (b g) | 8 | 0.053 | 0.000 | 0.317 | 75% | 0.053 | -0.17 to 0.27 | 0.97 | 0.93 [0.72, 0.99] |
| all (cl and cl?) | 31 | 0.068 | 0.003 | 0.317 | 74% | 0.042 | -0.18 to 0.26 | 0.96 | 0.95 [0.90, 0.98] |

Differences larger than 0.2: FA_F_farsi10 peas (0.27 / 0.00, closure 86 / 60 ms); PL_M_polish21 bags (0.34 / 0.56, closure 83 / 120 ms); FA_F_farsi8 Bob (0.15 / 0.46, closure 75 / 130 ms); FA_F_farsi8 big (0.00 / 0.27, closure 97 / 150 ms); FA_F_farsi8 toy (0.00 / 0.26, closure 59 / 103 ms).

## 2. Boundaries

| boundary | n | MAD | median AD | max AD | ≤5 ms | ≤10 ms | ≤20 ms | bias |
|---|---|---|---|---|---|---|---|---|
| B1 closure start | 31 | 16.5 | 11.0 | 75.5 | 39% | 48% | 65% | -7.9 |
| B2 burst | 31 | 5.5 | 0.5 | 29.1 | 74% | 81% | 87% | 5.0 |
| B3 vowel start | 31 | 9.0 | 8.7 | 21.6 | 26% | 65% | 97% | 0.9 |
| B4 vowel end | 31 | 22.4 | 8.4 | 200.3 | 35% | 58% | 77% | -15.6 |

B1 for the 21 words labelled `cl` by both: MAD 16.3 ms, median 11.1 ms.

## 3. By direction

| measure | Ala re-annotates Weronika (MAD / bias) | Weronika re-annotates Ala (MAD / bias) |
|---|---|---|
| B1 | 9.3 / 8.2 | 23.2 / -23.0 |
| B2 | 8.9 / 8.7 | 2.3 / 1.6 |
| B3 | 10.2 / 10.2 | 7.8 / -7.8 |
| B4 | 38.6 / -38.3 | 7.2 / 5.7 |
| VOT | 12.0 / 1.5 | 9.4 / -9.4 |
| closure | 9.9 / 0.5 | 25.0 / 24.6 |
| vowel | 48.5 / -48.5 | 13.7 / 13.4 |

## 4. cl vs cl? labels

Agreement 24/31 = 77.4%, Cohen's kappa = 0.32.

| original \ re-annotation | cl | cl? |
|---|---|---|
| cl | 21 | 4 |
| cl? | 3 | 3 |

Disagreements: EN_M_english102 big (cl? / cl); EN_M_english102 bags (cl? / cl); FA_F_farsi10 Bob (cl? / cl); PL_M_polish21 toy (cl / cl?); PL_M_polish21 bags (cl / cl?); FA_F_farsi8 big (cl / cl?); FA_F_farsi8 bags (cl / cl?).

## 5. Every token (original / re-annotation, ms)

| file | word | label | VOT | Δ | closure | Δ | vowel | Δ | voicing prop. | ΔB1 | ΔB2 | ΔB3 | ΔB4 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EN_M_english102 | call | cl | 33.9 / 47.6 | +13.7 | 34.8 / 35.4 | +0.6 | 138.3 / 107.7 | -30.6 | 0.00 / 0.00 | +0.2 | +0.7 | +14.4 | -16.1 |
| EN_M_english102 | peas | cl | 35.9 / 27.9 | -8.0 | 64.1 / 76.0 | +11.9 | 151.1 / 73.2 | -77.9 | 0.05 / 0.00 | +4.6 | +16.6 | +8.6 | -69.2 |
| EN_M_english102 | Bob | cl | 32.5 / 9.5 | -23.0 | 62.5 / 82.4 | +19.9 | 200.0 / 146.3 | -53.7 | 1.00 / 1.00 | +4.7 | +24.6 | +1.5 | -52.2 |
| EN_M_english102 | big | **cl? / cl** | 30.3 / 22.9 | -7.4 | 34.0 / 61.7 | +27.7 | 116.2 / 90.2 | -26.0 | 0.03 / 0.11 | -2.8 | +24.9 | +17.6 | -8.4 |
| EN_M_english102 | toy | cl? | 12.1 / 30.9 | +18.8 | 149.7 / 149.4 | -0.3 | 208.3 / 174.9 | -33.4 | 0.00 / 0.00 | +0.2 | -0.1 | +18.6 | -14.8 |
| EN_M_english102 | kids | cl | 34.5 / 45.6 | +11.1 | 52.5 / 52.2 | -0.3 | 122.6 / 110.3 | -12.3 | 0.00 / 0.00 | +0.2 | -0.1 | +11.0 | -1.3 |
| EN_M_english102 | bags | **cl? / cl** | 29.5 / 10.4 | -19.1 | 85.2 / 84.5 | -0.7 | 254.4 / 198.4 | -56.0 | 0.66 / 0.59 | +29.5 | +28.8 | +9.7 | -46.3 |
| EN_M_english102 | go | cl | 12.7 / 16.0 | +3.3 | 37.3 / 36.2 | -1.1 | 106.4 / 90.0 | -16.4 | 1.00 / 1.00 | +7.5 | +6.3 | +9.6 | -6.9 |
| FA_F_farsi10 | call | cl | 50.6 / 57.0 | +6.4 | 121.4 / 114.9 | -6.5 | 180.4 / 175.9 | -4.5 | 0.13 / 0.14 | +7.3 | +0.8 | +7.1 | +2.5 |
| FA_F_farsi10 | peas | cl | 43.0 / 54.6 | +11.6 | 85.8 / 60.4 | -25.4 | 269.2 / 228.4 | -40.8 | 0.27 / 0.00 | +25.4 | -0.1 | +11.5 | -29.2 |
| FA_F_farsi10 | Bob | **cl? / cl** | 13.7 / 22.9 | +9.2 | 149.1 / 113.6 | -35.5 | 423.3 / 294.7 | -128.6 | 0.59 / 0.59 | +35.4 | -0.2 | +9.0 | -119.7 |
| FA_F_farsi10 | big | cl? | 4.0 / 8.2 | +4.2 | 149.5 / 149.0 | -0.5 | 298.6 / 291.6 | -7.0 | 0.81 / 0.81 | +0.0 | -0.5 | +3.8 | -3.2 |
| FA_F_farsi10 | toy | cl? | 109.5 / 123.9 | +14.4 | 144.1 / 149.1 | +5.0 | 508.0 / 293.5 | -214.5 | 0.00 / 0.03 | -5.2 | -0.2 | +14.2 | -200.3 |
| FA_F_farsi10 | kids | cl | 106.9 / 85.5 | -21.4 | 106.5 / 119.1 | +12.6 | 141.5 / 125.4 | -16.1 | 1.00 / 1.00 | +16.6 | +29.1 | +7.7 | -8.3 |
| FA_F_farsi10 | go | cl | 9.3 / 17.9 | +8.6 | 68.3 / 68.6 | +0.3 | 176.8 / 167.3 | -9.5 | 0.44 / 0.44 | -0.1 | +0.1 | +8.7 | -0.9 |
| PL_M_polish21 | call | cl | 34.1 / 29.2 | -4.9 | 26.9 / 38.2 | +11.3 | 64.3 / 77.8 | +13.5 | 0.00 / 0.00 | -11.1 | +0.2 | -4.7 | +8.8 |
| PL_M_polish21 | peas | cl | 35.7 / 20.6 | -15.1 | 83.0 / 100.1 | +17.1 | 212.1 / 239.8 | +27.7 | 0.00 / 0.04 | -15.9 | +1.2 | -13.8 | +13.9 |
| PL_M_polish21 | Bob | cl | 30.1 / 9.7 | -20.4 | 93.8 / 92.4 | -1.4 | 166.7 / 198.9 | +32.2 | 1.00 / 1.00 | +0.2 | -1.2 | -21.6 | +10.7 |
| PL_M_polish21 | big | cl | 13.1 / 4.6 | -8.5 | 71.7 / 94.4 | +22.7 | 77.2 / 88.2 | +11.0 | 1.00 / 1.00 | -21.8 | +1.0 | -7.5 | +3.5 |
| PL_M_polish21 | toy | **cl / cl?** | 19.6 / 20.1 | +0.5 | 89.1 / 89.2 | +0.1 | 83.4 / 83.2 | -0.2 | 0.01 / 0.01 | -0.3 | -0.2 | +0.3 | +0.1 |
| PL_M_polish21 | kids | cl | 81.4 / 74.1 | -7.3 | 55.2 / 78.8 | +23.6 | 129.7 / 150.9 | +21.2 | 0.00 / 0.09 | -23.9 | -0.4 | -7.7 | +13.6 |
| PL_M_polish21 | bags | **cl / cl?** | 16.6 / 4.1 | -12.5 | 83.1 / 119.9 | +36.8 | 206.9 / 244.2 | +37.3 | 0.34 / 0.56 | -40.8 | -4.0 | -16.5 | +20.8 |
| PL_M_polish21 | go | cl | 35.9 / 21.7 | -14.2 | 50.5 / 61.8 | +11.3 | 103.8 / 117.6 | +13.8 | 0.41 / 0.52 | -11.1 | +0.1 | -14.0 | -0.3 |
| FA_F_farsi8 | call | cl | 30.7 / 21.5 | -9.2 | 49.7 / 58.8 | +9.1 | 115.3 / 125.6 | +10.3 | 0.00 / 0.00 | -4.9 | +4.2 | -5.1 | +5.3 |
| FA_F_farsi8 | peas | cl | 63.3 / 54.4 | -8.9 | 96.9 / 118.7 | +21.8 | 175.7 / 184.8 | +9.1 | 0.00 / 0.14 | -21.6 | +0.2 | -8.7 | +0.4 |
| FA_F_farsi8 | Bob | cl | 30.0 / 13.5 | -16.5 | 75.0 / 129.6 | +54.6 | 208.3 / 222.2 | +13.9 | 0.15 / 0.46 | -38.1 | +16.6 | +0.1 | +14.0 |
| FA_F_farsi8 | big | **cl / cl?** | 8.4 / 7.8 | -0.6 | 97.0 / 150.1 | +53.1 | 97.2 / 101.7 | +4.5 | 0.00 / 0.27 | -52.8 | +0.2 | -0.3 | +4.2 |
| FA_F_farsi8 | toy | cl | 122.8 / 106.2 | -16.6 | 59.1 / 103.4 | +44.3 | 134.2 / 138.3 | +4.1 | 0.00 / 0.26 | -37.0 | +7.3 | -9.2 | -5.1 |
| FA_F_farsi8 | kids | cl | 62.9 / 57.8 | -5.1 | 56.9 / 71.8 | +14.9 | 140.1 / 138.5 | -1.6 | 0.35 / 0.48 | -15.0 | -0.1 | -5.2 | -6.7 |
| FA_F_farsi8 | bags | **cl / cl?** | 12.9 / 12.8 | -0.1 | 130.4 / 128.6 | -1.8 | 213.2 / 218.5 | +5.3 | 0.00 / 0.00 | +1.7 | -0.0 | -0.1 | +5.2 |
| FA_F_farsi8 | go | cl | 38.3 / 28.0 | -10.3 | 21.2 / 96.7 | +75.5 | 120.8 / 133.5 | +12.7 | 1.00 / 1.00 | -75.5 | +0.0 | -10.3 | +2.4 |

Tokens with a boundary more than 20 ms apart: 17 of 31.

## 6. Draft sentence for the Method section

> Each annotator re-annotated two speakers of the other annotator without seeing the first version (4 speakers, one per group plus one extra Persian speaker; 32 tokens, 13% of the data). 1 token was left out because the first annotation was on the wrong word (a forced-alignment error, corrected afterwards). For the remaining 31 tokens, the mean absolute difference between annotators was 10.7 ms for VOT (Pearson r = 0.92, ICC(A,1) = 0.92; voiceless stops ICC = 0.93, voiced stops ICC = 0.31), 18.4 ms for closure duration (tokens labelled cl by both, n = 21, ICC = 0.59) and 30.5 ms for vowel duration (ICC = 0.80), and 0.07 for the proportion of voicing in the closure (ICC = 0.96). The burst (B2) was the most consistent boundary (median difference 0.5 ms) and the vowel end (B4) the least (mean 22.4 ms). The closure label (cl vs cl?) agreed for 24 of 31 tokens (77%, Cohen's kappa = 0.32).

## Notes from the script

- FA_F_farsi10.TextGrid: token 7 (vowel 37.003-37.301 s) lies in the WebMAUS word 'we', expected 'bags' -> taken as 'bags'
- FA_F_farsi10 'go': B3 moved by the owner after the check (39.4058 -> 39.4136 s); the comparison uses the original 39.4058 s
