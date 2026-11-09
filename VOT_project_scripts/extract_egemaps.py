# extract_egemaps.py - eGeMAPS functionals for every token (based on the course OpenSMILE material)
# Run it in the folder that contains the "tokens" folder made by measure_tokens.praat
import glob
import opensmile

smile = opensmile.Smile(
    feature_set=opensmile.FeatureSet.eGeMAPSv02,
    feature_level=opensmile.FeatureLevel.Functionals,
)
files = sorted(glob.glob("tokens/*.wav"))
features = smile.process_files(files).reset_index()
# "tokens/PL_F_polish3_peas.wav" -> "PL_F_polish3_peas" (same key as in the R script)
features["key"] = features["file"].str.replace(r".*/|\.wav$", "", regex=True)
features = features.drop(columns=["file", "start", "end"])
features.to_csv("egemaps_tokens.csv", index=False)
print("Done:", features.shape)
