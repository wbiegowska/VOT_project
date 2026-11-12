# Calibration notes – Ala

Speaker: **EN_F_english109** (My speaker, calibration version in `04_reliability/calibration_A`)
Time it took me: ~45m (first speaker, working carefully through each word)

## What I did for each word

| Word | cl | rel (VOT) | What I noticed |
|---|---|---|---|
| call | 44 ms | 60 ms | Clear aspirated k with long frication/aspiration after the burst; B4 placed at the end of regular vowel cycles before l |
| peas | ~55 ms | ~22 ms | Short VOT for English p (unstressed relative to "snow"); kept low-amplitude voicing ripples from "snow" inside cl |
| Bob | ~74 ms | ~10 ms | Continuous prevoicing running through the entire closure after "brother"; B3 placed at the first larger, jagged vowel cycle |
| big | ~87 ms | ~8 ms | Voicing fades out about halfway through the closure, then goes flat before a short burst |
| toy | cl? | ~45 ms | No visible release for the g of "big" — g and t closures merge into silence, so labeled cl? |
| kids | ~62 ms | ~57 ms | Clean, standard aspirated k with clear burst and vowel onset |
| bags | cl? | ~6 ms | Same merged pattern as "toy": d of "red" has no release and merges with b, so labeled cl?; very weak b burst |
| go | ~16 ms | ~14 ms | Closure voiced continuously after l of "will" with no silent flat part; placed B1 where larger l waves drop into low closure ripples |

## Rules I used

1. **B1 (closure start):** Where the high-amplitude waves and dark formant bands of the preceding vowel/sonorant drop off, NOT where all voicing stops. Low-amplitude voicing leaking into the closure stays inside `cl`.
2. **B2 (burst):** First sharp spike after the closure (taking the first spike if multiple spikes appear).
3. **B3 (voicing onset):** Start of the first regular vowel cycle in the waveform.
4. **Fully prevoiced stops (Bob, go):** B3 placed at the first cycle after the burst that shows vowel-like shape/complexity (larger and more jagged than smooth closure ripples).
5. **Merged closures without release (big toy, red bags):** Label `cl?` and place B1 where the merged closure becomes silent.
6. **B4 before weak/sonorant segments (toy before f, call before l):** Where the regular vowel cycles and upper formants end or drop sharply in amplitude.

## Things to discuss on the call

- **B3 for voiced stops (`Bob`, `go`):** Confirming whether we align on the first vowel-shaped cycle vs. the first full-amplitude cycle.
- **B1 when there is no silent closure (`go` after "will"):** Checking our exact amplitude-drop threshold after `[l]`.
- **B4 in `call` (`[O:]` into `[l]`):** Comparing where we each cut the vowel before the lateral transition.
