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
6. **B4 before a weak sound (toy before f):** where the regular vowel waves stop or get clearly smaller.
7. **B4 before l (call):** where the waves change shape from jagged (vowel) to smooth and rounded (l). The waves don't really get smaller, so the shape is the better clue. Trust this more than the WebMAUS line.
8. **cl or cl?:** WebMAUS sometimes marks a short pause <p:> before a word. If the whole silence is still a normal closure length (under ~150 ms) and you can't hear a pause, keep cl. Only use cl? if the silence is clearly longer or you hear a real pause.
9. **Creaky voice:** if the voice turns creaky in the vowel (pitch line drops to about half, vertical stripes get further apart) it's still the vowel, so don't end v there. Just write it in the log because f0 can be wrong there.
10. **Previous consonant WITH a visible release (polish3 "big toy"):** put B1 right after the release (thin dark vertical line), where it goes quiet. Then it's a normal cl if it's under 150 ms. But if the release is muffled (only a low dark blob, no hiss, like the d in polish3 "red bags"), the lips were already closed for the next sound, so cl?.
11. **B4 when the vowel ends creaky (polish3 kids, bags):** the creaky part still belongs to the vowel. B4 goes where the waves stop being spiky/jagged and turn into smooth rounded humps (= voicing in the next closure), NOT where the creak starts.

## PL_F_polish3 (my own speaker, second calibration speaker)

| Word | cl | rel (VOT) | What I noticed |
|---|---|---|---|
| call | 67 ms | 47 ms | WebMAUS put a pause before call but the silence is a normal closure, so cl. VOT shorter than english109 (70 ms). Vowel ends where the waves turn smooth (l) |
| peas | 63 ms | 42 ms | again a WebMAUS pause but normal closure length. Weak p burst. VOT LONGER than english109 (28 ms), not what we expected, maybe she stressed peas more. Creaky voice at the end of the vowel |
| Bob | 80 ms | 7 ms | closure voiced (prevoiced) the whole way with smooth small waves. No clear burst spike, so B2 where the smooth closure waves change shape. Creaky end of the vowel, kept it in v. Final b audibly released |
| big | 110 ms | 12 ms | voiced almost the whole closure, voicing gets really weak just before the burst. Quite a long closure but no pause, so cl. Vowel ends where the big waves shrink (small waves after = g closure) |
| toy | 129 ms | 124 ms | the g of "big" is released (thin dark line in the spectrogram), so B1 right after it. Closure about 130 ms = under 150, so still cl even though WebMAUS put a pause. VOT super long (124 ms!), way longer than english109 (52 ms). Vowel ends where the big waves suddenly shrink before f |
| kids | 45 ms | 100 ms | k has a double burst, B2 on the first spike. Praat put 2 pulses in the hiss before the vowel but there are no waves there, so not voicing. VOT long again (english109: 51 ms). Creaky end, B4 where the waves turn smooth (= d closure) |
| bags | cl? | 11 ms | the d of "red" is released INTO the b closure (only a low dark blob, no hiss), so her lips were already closed and I can't see where the b closure starts, so cl?. b fully prevoiced. Long creaky end (about 100 ms, pitch drops to half), vowel is 298 ms but it's right before a comma |
| go | 36 ms | 25 ms | B1 where the l waves get about half as big. Voicing gets very weak just before the burst. g has a few small spikes, B2 on the first one. Vowel ends where the waves turn smooth (m), no creak this time |

Time it took me: ~35 min (much faster than english109)

## Things to discuss on the call

- B3 for voiced stops: first vowel-shaped cycle or first full-height cycle? (difference is only a few ms but we should do the same thing)
- B1 when there's no flat part at all (go after "will")
- B4 for call (vowel into l): I used the change in wave shape for polish3 (rule 7) but for english109 I used where the waves get smaller, so the vowel came out 174 ms vs 78 ms. Need one rule, then I recheck english109 call
- Do you agree with the 150 ms limit for cl? (rule 8)
- For voiced stops in polish3 (Bob, bags, go) I put B3 where the line first plunges into the first big vowel wave. Is that how you do it too?
- Rules 10 and 11 are new (from polish3), check if you agree
- polish3 has really long VOTs in toy (124 ms) and kids (100 ms), longer than the American speaker. Real or just because she restarts after small breaks? Let's see if other Polish speakers do the same
