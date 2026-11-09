## convert_flac_to_wav.praat - saves every .flac file in a folder as a .wav file
## (FLAC is lossless, so nothing changes in the sound)
directory$ = chooseDirectory$: "Select the folder with your .flac files"
Create Strings as file list: "flacList", directory$ + "/*.flac"
n = Get number of strings
for i from 1 to n
	selectObject: "Strings flacList"
	fileName$ = Get string: i
	sound = Read from file: directory$ + "/" + fileName$
	name$ = selected$ ("Sound")
	Save as WAV file: directory$ + "/" + name$ + ".wav"
	removeObject: sound
endfor
removeObject: "Strings flacList"
writeInfoLine: "Converted ", n, " files."
