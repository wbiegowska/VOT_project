# Calibration notes – Weronika

Speaker: **EN_F_english109** (Ala's speaker, my calibration version is in `04_reliability/calibration_W`)
Time it took me: 1h (first speaker, so slower than normal)

## What I did for each word

| Word | cl | rel (VOT) | What I noticed |
|---|---|---|---|
| call | 44 ms | 70 ms | clear aspirated k, long noisy part after the burst |
| peas | 55 ms | 28 ms | VOT pretty short for an English p, probably because the stress is on SNOW in "snow peas". The small waves at the start of the closure are voicing from "snow", I kept them inside cl |
| Bob | 74 ms | 5 ms | closure voiced the whole way through (small regular waves + pulses), even though she's a native speaker. Probably because "brother" ends in a voiced sound |
| big | 87 ms | 8 ms | voicing fades out about halfway through the closure, then flat until the burst |
| toy | cl? | 52 ms | no release of the g from "big" visible, the g and t closures merge, so cl? |
| kids | 62 ms | 51 ms | normal aspirated k, easy one |
| bags | cl? | 6 ms | same as toy: d of "red" and b merge, so cl?. The b burst is really weak |
| go | 16 ms | 14 ms | closure voiced all the way after the l of "will", hard to find B1, used the point where the waves suddenly get small |

## Rules I used 

1. **B1 (closure start):** where the big waves / dark bands of the previous vowel end, NOT where all voicing stops. Small waves after that = voicing leaking into the closure, they stay inside cl.
2. **B2 (burst):** first spike after the closure. If there are several spikes (like in k), take the first one.
3. **B3 (voicing onset):** where the first big regular wave of the vowel starts in the waveform. Pulses only as a hint, because Praat sometimes puts pulses in the burst noise and they move a bit when you zoom.
4. **Voiced stops voiced all the way (Bob, go):** B3 = first cycle after the burst that looks like the vowel (bigger and more jagged than the smooth closure waves), even if it's not full height yet.
5. **Previous consonant with no visible release (big toy, red bags):** label cl? and put B1 where the closure becomes silent.
6. **B4 before a weak sound (toy before f, call before l):** where the regular vowel waves stop or get clearly smaller.

## Things to discuss on the call

- B3 for voiced stops: first vowel-shaped cycle or first full-height cycle? (difference is only a few ms but we should do the same thing)
- B1 when there's no flat part at all (go after "will")
- B4 for call (vowel into l) is a bit of a guess, how did you do it?
