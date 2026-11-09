## measure_tokens.praat  (starter script for the Biegowska & Karamkesh project)
## Built from the commands and settings in the course scripts:
##   - two-pass f0 method: f0ComputationsSmoothingCC_v3.praat / VUV_Computations_v6.praat
##   - voicing detection (To TextGrid (vuv)): VUV_Computations_v6.praat
##   - HNR (cc): VQ_measurements_V2.praat
##   - formant settings (Burg, 5 formants, 5000 Hz male / 5500 Hz female, 25 ms window,
##     50 Hz pre-emphasis): Week 3 slides
## Requires Praat 6.4 or above (same as the course scripts).
##
## What it expects in the folder:
##   one .wav + one .TextGrid per speaker, with the SAME name,
##   e.g. PL_F_polish3.wav + PL_F_polish3.TextGrid
##   name pattern: GROUP_SEX_archiveID  (GROUP = PL, FA or EN; SEX = F or M)
##   the TextGrid must contain the WebMAUS word tier (default name ORT-MAU)
##   and our hand-made interval tier "seg" with three intervals per target word: cl, rel, v
##
## What it writes:
##   tokens.txt (tab-separated, one row per target word) in the same folder
##   folder "vowels": one .wav + .TextGrid per vowel (to run VQ_measurements_V2.praat on, unchanged)
##   folder "tokens": one .wav per token, from closure start to vowel end (for OpenSMILE)

beginPause: "Measure tokens - VOT project"
	comment: "Folder with the speaker .wav and .TextGrid files (leave empty to browse)"
	sentence: "directory", ""
	comment: "Name of the WebMAUS word tier"
	sentence: "word_tier_name", "ORT-MAU"
	comment: "Name of our segment tier"
	sentence: "seg_tier_name", "seg"
	comment: "Results file name"
	sentence: "results", "tokens"
	boolean: "export_audio", 1
clicked = endPause: "OK", 1

if directory$ = ""
	directory$ = chooseDirectory$: "Select the folder with your .wav and .TextGrid files"
endif

outFile$ = directory$ + "/" + results$ + ".txt"
if fileReadable (outFile$)
	deleteFile: outFile$
endif
appendFileLine: outFile$, "file", tab$, "group", tab$, "sex", tab$, "word", tab$, "clLabel", tab$,
... "clStart", tab$, "relStart", tab$, "vStart", tab$, "vEnd", tab$,
... "clDur_ms", tab$, "VOT_ms", tab$, "vDur_ms", tab$, "voicedInCl_ms", tab$, "voicingProp", tab$,
... "f0_10", tab$, "f0_50", tab$, "F1_10", tab$, "F1_50", tab$, "HNR_v"

if export_audio
	createDirectory: directory$ + "/vowels"
	createDirectory: directory$ + "/tokens"
endif

Create Strings as file list: "fileList", directory$ + "/*.wav"
nbFiles = Get number of strings

for i from 1 to nbFiles
	selectObject: "Strings fileList"
	fileName$ = Get string: i
	sound = Read from file: directory$ + "/" + fileName$
	name$ = selected$ ("Sound")
	grid = Read from file: directory$ + "/" + name$ + ".TextGrid"
	group$ = left$ (name$, 2)
	sex$ = mid$ (name$, 4, 1)

	# find the two tiers by their names
	selectObject: grid
	nbTiers = Get number of tiers
	wordTier = 0
	segTier = 0
	for t from 1 to nbTiers
		tierName$ = Get tier name: t
		if tierName$ = word_tier_name$
			wordTier = t
		endif
		if tierName$ = seg_tier_name$
			segTier = t
		endif
	endfor
	if wordTier = 0 or segTier = 0
		exitScript: "Tier missing in ", name$, ".TextGrid (check the tier names)"
	endif

	# two-pass f0 (as in the course scripts)
	selectObject: sound
	noprogress To Pitch (raw cross-correlation): 0.005, 50, 800, 15, "yes", 0.03, 0.45, 0.01, 0.35, 0.14
	q1 = Get quantile: 0, 0, 0.25, "Hertz"
	q3 = Get quantile: 0, 0, 0.75, "Hertz"
	minPitch = q1 * 0.75
	maxPitch = q3 * 1.5
	Remove
	selectObject: sound
	pitch = noprogress To Pitch (raw cross-correlation): 0.005, minPitch, maxPitch, 15, "yes",
	... 0.03, 0.45, 0.01, 0.35, 0.14

	# voicing detection (as in VUV_Computations_v6.praat)
	selectObject: sound
	soundFiltered = Filter (pass Hann band): 0, 500, 20
	noprogress To Pitch (raw cross-correlation): 0.005, 50, 800, 15, "yes", 0.03, 0.45, 0.01, 0.35, 0.14
	fq1 = Get quantile: 0, 0, 0.25, "Hertz"
	fq3 = Get quantile: 0, 0, 0.75, "Hertz"
	Remove
	selectObject: soundFiltered
	pitchFiltered = noprogress To Pitch (raw cross-correlation): 0.005, fq1 * 0.75, fq3 * 1.5,
	... 15, "yes", 0.03, 0.45, 0.01, 0.35, 0.14
	selectObject: soundFiltered
	plusObject: pitchFiltered
	pointProcess = noprogress To PointProcess (cc)
	meanPeriod = Get mean period: 0, 0, 0.0001, 0.02, 1.3
	vuv = To TextGrid (vuv): 0.02, meanPeriod
	nbVuv = Get number of intervals: 1

	# formants (Week 3 settings) and harmonicity (VQ script settings)
	if sex$ = "M"
		maxFormant = 5000
	else
		maxFormant = 5500
	endif
	selectObject: sound
	formant = noprogress To Formant (burg): 0.005, 5, maxFormant, 0.025, 50
	selectObject: sound
	harmonicity = noprogress To Harmonicity (cc): 0.005, minPitch, 0.1, 1

	# loop over the "v" intervals of our segment tier
	selectObject: grid
	nbSeg = Get number of intervals: segTier
	for j from 3 to nbSeg
		selectObject: grid
		vLabel$ = Get label of interval: segTier, j
		if vLabel$ = "v"
			relLabel$ = Get label of interval: segTier, j - 1
			clLabel$ = Get label of interval: segTier, j - 2
			vStart = Get starting point: segTier, j
			vEnd = Get end point: segTier, j
			relStart = Get starting point: segTier, j - 1
			clStart = Get starting point: segTier, j - 2
			vDur = vEnd - vStart
			wordInterval = Get interval at time: wordTier, vStart + vDur / 2
			word$ = Get label of interval: wordTier, wordInterval

			if relLabel$ = "rel" and left$ (clLabel$, 2) = "cl"
				clDur = relStart - clStart
				vot = vStart - relStart

				# voiced time inside the closure (sum of "V" stretches from the vuv TextGrid)
				voiced = 0
				selectObject: vuv
				for k from 1 to nbVuv
					lab$ = Get label of interval: 1, k
					if lab$ = "V"
						a = Get starting point: 1, k
						b = Get end point: 1, k
						overlap = min (b, relStart) - max (a, clStart)
						if overlap > 0
							voiced = voiced + overlap
						endif
					endif
				endfor
				voicingProp = voiced / clDur

				# f0, F1 at 10% (onset) and 50% (midpoint) of the vowel; HNR over the vowel
				t10 = vStart + 0.1 * vDur
				t50 = vStart + 0.5 * vDur
				selectObject: pitch
				f0_10 = Get value at time: t10, "Hertz", "linear"
				f0_50 = Get value at time: t50, "Hertz", "linear"
				selectObject: formant
				f1_10 = Get value at time: 1, t10, "hertz", "linear"
				f1_50 = Get value at time: 1, t50, "hertz", "linear"
				selectObject: harmonicity
				hnr = Get mean: vStart, vEnd

				appendFileLine: outFile$, name$, tab$, group$, tab$, sex$, tab$, word$, tab$,
				... clLabel$, tab$, fixed$ (clStart, 4), tab$, fixed$ (relStart, 4), tab$,
				... fixed$ (vStart, 4), tab$, fixed$ (vEnd, 4), tab$,
				... fixed$ (clDur * 1000, 1), tab$, fixed$ (vot * 1000, 1), tab$,
				... fixed$ (vDur * 1000, 1), tab$, fixed$ (voiced * 1000, 1), tab$,
				... fixed$ (voicingProp, 3), tab$, fixed$ (f0_10, 1), tab$, fixed$ (f0_50, 1), tab$,
				... fixed$ (f1_10, 0), tab$, fixed$ (f1_50, 0), tab$, fixed$ (hnr, 2)

				if export_audio
					selectObject: sound
					vPart = Extract part: vStart, vEnd, "rectangular", 1, "no"
					Save as WAV file: directory$ + "/vowels/" + name$ + "_" + word$ + ".wav"
					vGrid = To TextGrid: "vq", ""
					Save as text file: directory$ + "/vowels/" + name$ + "_" + word$ + ".TextGrid"
					removeObject: vPart, vGrid
					selectObject: sound
					tPart = Extract part: clStart, vEnd, "rectangular", 1, "no"
					Save as WAV file: directory$ + "/tokens/" + name$ + "_" + word$ + ".wav"
					removeObject: tPart
				endif
			else
				appendFileLine: outFile$, name$, tab$, group$, tab$, sex$, tab$, word$, tab$,
				... "CHECK_LABELS"
			endif
		endif
	endfor

	removeObject: sound, grid, pitch, soundFiltered, pitchFiltered, pointProcess, vuv
	removeObject: formant, harmonicity
endfor
removeObject: "Strings fileList"
writeInfoLine: "Finished! Results are in ", outFile$
