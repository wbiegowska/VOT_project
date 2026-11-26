# Results notes (Weronika: R2, R3, R4)

Working notes for the Results section. Numbers come from `VOT_project_scripts/analysis.R`
run on `06_R/tokens.txt` + `06_R/VQResults2.xls` (26 Nov 2026).

## R2 - Look at the data

Figures: `07_figures/R2_VOT_by_group.png`, `07_figures/R2_voicingProp_by_group.png`.

> In all three groups, VOT clearly separated voiced from voiceless stops: /b g/ had short-lag VOT
> (medians 11-16 ms) and /p t k/ long-lag VOT. Contrary to our prediction, the Polish speakers'
> /p t k/ were not shorter than the English speakers' (median 60 vs 59 ms), while the Persian
> speakers had the longest VOT (median 72 ms). Closures of /b g/ were mostly voiced in every group,
> and /p t k/ closures were mostly voiceless (medians 0-0.08). The Polish /b g/ show the most fully
> voiced closures (median 1.00) but also the widest spread, so some Polish tokens are fully
> prevoiced and others are not.

| group | VOT /b g/ median (ms) | VOT /p t k/ median (ms) | voicing prop. /b g/ median (mean) | voicing prop. /p t k/ median |
|---|---|---|---|---|
| EN | 14.5 | 58.6 | 0.88 (0.76) | 0.05 |
| PL | 11.4 | 60.0 | 1.00 (0.66) | 0.00 |
| FA | 15.8 | 72.2 | 0.77 (0.57) | 0.08 |

Voicing proportion: words labelled `cl` only (`cl?` words have no closure measures).

## R3 - Mixed-effects models

Models (book ch. 3.3): `measure ~ group + (1 | file) + (1 | word)`, maximum likelihood;
the group effect is tested by comparing with `measure ~ 1 + (1 | file) + (1 | word)` (`anova(m0, m1)`).
English = reference group, so the PL and FA estimates are differences from the English speakers.

| measure (tokens) | n (speakers) | model comparison | EN intercept (SE) | PL - EN (SE, t) | FA - EN (SE, t) |
|---|---|---|---|---|---|
| VOT of /p t k/ (ms) | 120 (30) | chi2(2) = 5.48, p = .065 | 59.3 (7.3) | +4.4 (6.8, t = 0.66) | +16.1 (6.8, t = 2.38) |
| voicing proportion of /b g/ (0-1) | 90 (30) | chi2(2) = 1.84, p = .40 | 0.74 (0.11) | -0.07 (0.15, t = -0.51) | -0.20 (0.15, t = -1.36) |

Random effects (SD): VOT: speaker 10.4 ms, word 11.1 ms, residual 22.1 ms.
Voicing proportion: speaker 0.30, word 0.07, residual 0.23.

Draft text:

> Adding speaker group did not significantly improve the model for the VOT of /p t k/
> (chi2(2) = 5.48, p = .065). Polish speakers' VOT did not differ from the English speakers'
> (+4.4 ms, SE 6.8), whereas Persian speakers' VOT was on average 16.1 ms longer (SE 6.8, t = 2.38).
> For /b g/, the proportion of voicing in the closure did not differ between groups
> (chi2(2) = 1.84, p = .40; PL -0.07, FA -0.20 relative to English, 0.74). Variation between
> speakers was large (SD 0.30), larger than variation between words (SD 0.07).

Notes for the Discussion:
- The predicted transfer from Polish (shorter /p t k/ VOT, more voicing in /b g/ closures) does not
  show up as a group difference in this sample; the Polish speakers aspirate their /p t k/ like the
  English speakers.
- The marginal group effect for VOT comes from the Persian speakers (longer VOT than English).
- Voicing proportion is a bounded proportion with many values at 1 (ceiling); the linear model is a
  simple first step (plan R3 "Watch out").

## R4 - PCA and k-means

Cues (7, scaled): VOT, closure duration, voicing proportion, f0rel, F1rel, HNR, CPP.
175 tokens with all cues (EN 58, PL 63, FA 54); `cl?` words, missing f0 and the 4 short vowels
are left out, and f0 jumps over 6 semitones count as missing (2 tokens).
Figures: `07_figures/R4_scree.png`, `R4_biplot.png`, `R4_pca_groups.png`, `R4_kmeans.png`.

| dimension | eigenvalue | % variance | cumulative % |
|---|---|---|---|
| 1 | 1.7 | 23.7 | 23.7 |
| 2 | 1.5 | 20.8 | 44.6 |
| 3 | 1.0 | 14.9 | 59.4 |
| 4 | 1.0 | 13.9 | 73.3 |
| 5 | 0.7 | 10.5 | 83.8 |

Correlations of the cues with the first two dimensions:

| cue | Dim 1 | Dim 2 |
|---|---|---|
| VOT | 0.75 | -0.35 |
| closure duration | -0.33 | 0.31 |
| voicing proportion | -0.66 | 0.24 |
| f0rel | -0.06 | -0.77 |
| F1rel | 0.39 | 0.04 |
| HNR | 0.52 | 0.46 |
| CPP | 0.36 | 0.61 |

k-means, 2 clusters (cluster 1 = mostly voiced, cluster 2 = mostly voiceless):

| group | voiced in cluster 1 | voiceless in cluster 2 | match with voicing |
|---|---|---|---|
| EN | 27 of 30 | 27 of 28 | 54/58 = 93% |
| PL | 21 of 27 | 29 of 36 | 50/63 = 79% |
| FA | 18 of 23 | 26 of 31 | 44/54 = 81% |
| all | 66 of 80 | 82 of 95 | 148/175 = 85% |

Draft text:

> The first two principal components explained 44.6% of the variance, and four components had an
> eigenvalue of at least 1, so the cues carry partly independent information rather than one
> redundant voicing measure. Dimension 1 opposed VOT (r = 0.75) to the proportion of voicing in the
> closure (r = -0.66); dimension 2 was mainly f0 at vowel onset relative to the midpoint (f0rel,
> r = -0.77), together with CPP and HNR (0.61, 0.46). In the biplot, voiced and voiceless tokens
> separate along the diagonal between these two dimensions: voiced tokens have more closure voicing,
> voiceless tokens longer VOT and a higher f0 at vowel onset. CPP and HNR point at right angles to
> this direction, so voice quality contributes little to the contrast. The three speaker groups
> overlap completely in the PCA space. Without knowing the labels, k-means with two clusters
> recovered the voicing category for 85% of the tokens: 93% for the English speakers but only 79%
> for the Polish and 81% for the Persian speakers, so the contrast is less clearly separated in the
> non-native speakers' productions.

Notes for the Discussion:
- f0rel behaves as expected for an onset f0 cue (higher f0 after voiceless stops), and it is
  largely independent of VOT (it loads on dimension 2).
- The k-means differences are descriptive (no test); the numbers per group are small.
