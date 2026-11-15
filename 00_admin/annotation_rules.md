# Annotation rules (shared – Weronika + Ala)

We BOTH follow these rules for all 30 speakers and for the reliability check.
They replace the rules in `calibration_notes_W.md` and `calibration_notes_A.md`.
They come from comparing our two calibration speakers (see `04_reliability/calibration_comparison.md`).

**The idea behind everything: each interval contains only one thing.**
- `cl` = only the closure of the target stop
- `rel` = only the burst + the noise/aspiration until the vowel starts
- `v` = only the vowel. This matters most, because vowel duration, f0 and F1 at 10% and 50%, HNR, CPP, tilt, Hammarberg and the OpenSMILE token are all measured on `v`.

---

## 1. Same settings for both of us

- Spectrogram settings: 0–8000 Hz, window length 0.005 s. Pulses → Show pulses.
- Zoom: about 150–300 ms on screen for B1 and B4, about 50–100 ms for B2 and B3.
- Waveform first, spectrogram to confirm. Blue pulse lines and WebMAUS lines are only hints, never the answer.
- When unsure, listen: select a part and press Tab.

## 2. Labels

- Tier `seg`. For each of the 8 target words exactly three touching intervals: `cl` (or `cl?`) – `rel` – `v`.
- Lowercase, nothing else on this tier. Empty intervals between the words are fine.
- Save: File → Save TextGrid as text file → `03_annotated` (own speakers) or `04_reliability` (reliability check), same name as the .wav.

## 3. Order for each word

1. **B2** (burst) – easiest to see, start here
2. **B3** (vowel start)
3. **B4** (vowel end)
4. **B1** (closure start) + decide `cl` or `cl?`
5. Label, play `v` on its own (you should hear ONLY the vowel, no l / m / z / g), do the quick check in section 10, save.

---

## 4. B2 – burst

- B2 = at the start of the **first spike** after the closure. In the spectrogram: a thin dark vertical line going up through many frequencies.
- Several spikes (common for k and g): take the **first** one.
- No clear spike (often b or g with a voiced closure): the point where the smooth closure waves suddenly get disturbed / irregular. There's usually a faint vertical line in the spectrogram there.
- We want the burst right before the vowel or the aspiration. A small spike earlier in the closure can be the release of the previous word's consonant (e.g. the d of "red") – that is NOT B2.

## 5. B3 – vowel start

One rule for all stops: **B3 = start of the first cycle that belongs to the vowel, even if it's still small.**

- **p t k:** the first regular wave after the hiss that keeps repeating into the vowel. Praat often draws pulse lines inside the hiss – if you can't see repeating waves there, it's not voicing yet.
- **b g with a voiced closure (prevoiced):** small smooth waves can continue through the burst – those don't count. B3 = the first cycle with the vowel's shape (bigger and jagged/spiky), i.e. the spot where the line first plunges into the first big wave. NOT the first full-size cycle (too subjective, it gave us 4–7 ms differences).
- **b g without voicing in the closure:** same as p t k.
- Spectrogram check: the dark band at the bottom and the vowel's formant bands start here.

## 6. B4 – vowel end (the most important one)

**B4 = end of the last cycle that still has the vowel's jagged / spiky shape.**

After B4 the next consonant starts, and it looks like one of these:
- smooth, rounded humps (voicing in a b / d / g closure, or l, m)
- a flat line (silent closure or pause)
- hiss / noise (z, f)

In the spectrogram the vowel's upper dark bands (F2 and higher) end or suddenly get weaker at B4.

**Don't use:**
- "where the waves get smaller" – the amplitude often fades slowly over 50+ ms. That's why our vowels differed by 40–180 ms.
- "where all voicing stops" – the voicing after the vowel belongs to the closure of the next consonant.
- one long `v` until the end of the word – `v` is only the vowel.

**Why this rule:** smooth humps = mouth already closed = consonant. Putting them in `v` would make the vowel longer and mess up F1 and the voice quality measures.

| after the vowel | what you see at B4 | target words |
|---|---|---|
| b, d, g | jagged vowel cycles → smooth rounded humps (or a flat line if the closure is silent) | Bob, big, kids, bags |
| l | jagged → smooth rounded waves. The waves don't always get smaller, so go by the shape | call |
| m | flat-topped / jagged → smooth triangle-like waves, only the bottom band stays strong | go |
| z | start of the hiss (noise in the waveform, dark fuzz high up in the spectrogram) | peas |
| f | where the big jagged waves suddenly shrink; small waves / hiss after that = f | toy |
| pause | end of the last regular cycle | – |

**Creaky voice:** if the voice gets creaky at the end (pitch line suddenly drops to about half, pulse lines twice as far apart, each wave = one sharp spike + ripples, dark vertical lines going high up in the spectrogram), it is STILL the vowel. Keep it inside `v` and put B4 where the spiky creaky waves turn into smooth humps (or stop). Write the word in the log notes (e.g. "creak: kids, bags") because f0 can be wrong there.

**Breathy end:** if the vowel fades into an "h"-like breath, B4 = end of the last regular cycle.

---

## 7. B1 – closure start

**B1 = where the previous sound ends.** Same test as for B4:
- previous sound = jagged waves, energy higher up in the spectrogram (above the very bottom strip, i.e. above ~500 Hz)
- closure = flat line OR small smooth humps, with only a dark bar at the very bottom

Voicing that continues into the closure (small smooth waves) stays INSIDE `cl` – don't wait until all voicing stops.

Everyone reads the same paragraph, so the contexts are always the same:

| word | comes after | where B1 goes |
|---|---|---|
| call | "Please" (z) | where the z hiss stops |
| peas | "snow" (vowel) | where the vowel's jagged waves end |
| Bob | "brother" (vowel) | where the vowel's jagged waves end |
| big | "a" | where the vowel's jagged waves end |
| toy | g of "big" | right after the release of the g, where it goes quiet (see section 8) |
| kids | "the" | where the vowel's jagged waves end |
| bags | d of "red" | right after the release of the d, if you can see one (see section 8) |
| go | l of "will" | where the l waves drop to about half and turn into small smooth ripples, and the energy above ~500 Hz disappears. There's often no flat part here |

**Release of a previous stop** = thin dark vertical line + small spike. If there are a few spikes close together, B1 goes after the last of them. Faint isolated specks later in the silence are just noise – ignore them.

## 8. `cl` or `cl?`

Use **`cl`** when you can clearly see where the closure starts:
- the previous sound ends clearly (vowel, l, z), or
- the previous stop has a clear release (spike + dark line going high up, with some hiss)

**AND** the closure (B1 → B2) is 150 ms or shorter, **AND** you don't hear a pause.

Use **`cl?`** when:
1. the previous stop has **no visible release** – its closure just merges into ours (often "big toy", "red bags")
2. the previous stop is released **inside** our closure – only a small low dark blob, no hiss (the lips or tongue were already closed for our stop, e.g. polish3 "red bags")
3. the silence is **longer than 150 ms**, or you hear a pause, a breath or a hesitation before the word
4. anything else where you really can't tell where the closure starts (noise, overlapping sounds)

A WebMAUS pause `<p:>` alone is NOT a reason for `cl?` – WebMAUS marks lots of normal closures as pauses. Measure the silence yourself.

**B1 for `cl?` words:** right after the last thing you can still see from the previous sound (its release blob, the end of its voicing, or the end of its hiss). If that is more than 150 ms before B2 (a real pause), put B1 **150 ms before B2** (select from B2 to the left until the bar shows 0.150).

**What `cl?` does in the analysis:** VOT and all the vowel measures are still used. R only ignores closure duration and voicing proportion for that word. So when in doubt, `cl?` is the safe choice.

---

## 9. When you're unsure between two spots

- Check in this order: (1) wave shape, (2) spectrogram, (3) listening. Amplitude alone is not enough.
- **B1:** end of the last cycle you're SURE belongs to the previous sound.
- **B4:** end of the last cycle you're SURE belongs to the vowel.
- **B2:** the earlier spike. **B3:** the first cycle you're sure is the vowel.
- Still unsure? Annotate anyway and write e.g. "kids: unsure B4" in the log notes, so the other one can have a look.

## 10. Quick check after each word

Look at the durations Praat shows under the intervals. Look again if:
- `cl` is under 10 ms, or over 150 ms (over 150 should be `cl?` anyway)
- `rel` of b / g is over 30 ms, or `rel` of p / t / k is under 10 ms
- `v` is under 50 ms or over 300 ms

These aren't automatically errors (polish3 toy has a 124 ms VOT, bags a 298 ms vowel), just a reason to look again.

## 11. Special cases

- **Accent is not a mistake.** If a Polish or Persian speaker says the word differently (no aspiration, "bags" ending in k/s, a different vowel), annotate it normally – that's exactly what we're studying.
- **Misread / missing / unusable word** (another word said, word skipped, laughing or noise on top): don't annotate it, write it in the log (`words_missing`).
- **Repeated word** ("b- Bob"): annotate the last complete version and write it in the log. Its closure is usually `cl?` because of the hesitation before it.

## 12. What to write in the log

- `minutes`, `cl?_tokens` (which words), `words_missing`
- `notes`: creaky words, unsure boundaries, anything odd (pause, noise, repeated word)

---

## 13. What to recheck now

- **Weronika – PL_F_polish3** (`03_annotated`): already follows these rules, nothing to change.
- **Ala – EN_F_english109** (`03_annotated`): recheck all B4s with section 6 (especially call: Ala's vowel is 215 ms, Weronika's 174 ms), B3 of call (10 ms apart), B1 of peas (16 ms apart), and B3 of Bob and go (section 5).
- The copies in `04_reliability/calibration_W` and `calibration_A` were only for the calibration and don't go into the analysis, so they don't need fixing.
