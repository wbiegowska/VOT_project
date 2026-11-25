"""
reliability.py - inter-annotator agreement for the VOT project (plan step R8 / N4).

Compares the re-annotated TextGrids in 04_reliability/calibration_A and calibration_W
with the owner's version in 03_annotated, word by word, straight from the "seg" tier
(no audio needed):
  - the 4 boundaries B1 (closure start), B2 (burst), B3 (vowel start), B4 (vowel end)
  - closure duration (B2-B1), VOT (B3-B2), vowel duration (B4-B3)
  - the closure label (cl vs cl?)

Writes (LF line endings) into 04_reliability/:
  reliability_tokens.csv   one row per word: both versions + differences (re-annotation - original, ms)
  reliability_summary.csv  one row per measure and subset: bias, MAD, limits of agreement, r, ICC
  reliability_results.md   readable summary for the Method section

Run from the project folder:  python3 VOT_project_scripts/reliability.py
Needs numpy and pandas; scipy is optional (only used for the ICC confidence intervals).
"""
import csv
import os
import re
import sys

import numpy as np
import pandas as pd

try:
    from scipy import stats
except ImportError:  # the ICC itself does not need scipy, only its 95% CI
    stats = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANN = os.path.join(ROOT, "03_annotated")
REL = os.path.join(ROOT, "04_reliability")

# re-annotated file -> who re-annotated it (the original owner comes from speakers.csv)
PAIRS = [
    ("calibration_A/EN_M_english102", "Ala"),
    ("calibration_A/FA_F_farsi10", "Ala"),
    ("calibration_W/PL_M_polish21", "Weronika"),
    ("calibration_W/FA_F_farsi8", "Weronika"),
]
WORDS = ["call", "peas", "Bob", "big", "toy", "kids", "bags", "go"]  # order in the paragraph
# tokens that cannot count as an independent comparison
EXCLUDE = {
    ("FA_F_farsi10", "bags"): "WebMAUS had put 'bags' about 1.5 s too early, on 'into'; Weronika's first "
                              "version followed WebMAUS, Ala's was on the real 'bags'. Weronika's file was "
                              "then corrected to Ala's word (25 Nov), so the two versions are no longer "
                              "independent",
}
VOICED = {"Bob", "big", "bags", "go"}


def read_textgrid(path):
    """Minimal reader for Praat long-format text TextGrids -> {tier name: [(xmin, xmax, text)]}."""
    with open(path, "rb") as fh:
        raw = fh.read()
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
        txt = raw.decode("utf-16")
    else:
        txt = raw.decode("utf-8-sig")
    tiers = {}
    pattern = r'item \[\d+\]:\s*class = "(\w+)"\s*name = "([^"]*)"(.*?)(?=item \[\d+\]:|\Z)'
    for cls, name, body in re.findall(pattern, txt, re.S):
        ivs = re.findall(r'xmin = ([-\d.eE+]+)\s*xmax = ([-\d.eE+]+)\s*text = "((?:[^"]|"")*)"', body)
        tiers[name] = [(float(a), float(b), t.strip()) for a, b, t in ivs]
    return tiers


def tokens_from_grid(path):
    """Return {word: dict(label, B1..B4)} from the seg tier, plus a list of problems."""
    tiers = read_textgrid(path)
    seg, words = tiers.get("seg"), tiers.get("ORT-MAU")
    problems = []
    if seg is None:
        return {}, [f"{path}: no seg tier"]
    trip = []
    for j in range(2, len(seg)):
        if seg[j][2] == "v":
            cl, rel, v = seg[j - 2], seg[j - 1], seg[j]
            if rel[2] != "rel" or not cl[2].startswith("cl"):
                problems.append(f"{os.path.basename(path)}: labels before v at {v[0]:.3f} are "
                                f"'{cl[2]}' '{rel[2]}' (CHECK_LABELS)")
                continue
            trip.append({"label": cl[2], "B1": cl[0], "B2": rel[0], "B3": v[0], "B4": v[1]})
    out = {}
    for k, t in enumerate(trip):
        # word = WebMAUS word at the vowel midpoint (same as measure_tokens.praat) ...
        mid = (t["B3"] + t["B4"]) / 2
        maus = next((w[2] for w in (words or []) if w[0] <= mid < w[1]), "")
        # ... checked against the paragraph order
        expected = WORDS[k] if len(trip) == 8 else None
        word = next((w for w in WORDS if w.lower() == maus.lower()), expected)
        t["maus_word"] = maus
        if expected and maus.lower() != expected.lower():
            problems.append(f"{os.path.basename(path)}: token {k + 1} (vowel {t['B3']:.3f}-{t['B4']:.3f} s) "
                            f"lies in the WebMAUS word '{maus}', expected '{expected}' -> taken as '{word}'")
        if word in out:
            problems.append(f"{os.path.basename(path)}: '{word}' annotated twice")
        out[word] = t
    for w in WORDS:
        if w not in out:
            problems.append(f"{os.path.basename(path)}: '{w}' missing")
    return out, problems


def icc_a1(x, y, alpha=0.05):
    """ICC(A,1): two-way random effects, absolute agreement, single rater (McGraw & Wong 1996),
    the same formula and CI as irr::icc(model='twoway', type='agreement', unit='single')."""
    m = np.column_stack([x, y]).astype(float)
    m = m[~np.isnan(m).any(axis=1)]
    n, k = m.shape
    if n < 3:
        return np.nan, np.nan, np.nan
    grand = m.mean()
    ss_r = k * ((m.mean(axis=1) - grand) ** 2).sum()
    ss_c = n * ((m.mean(axis=0) - grand) ** 2).sum()
    ss_e = ((m - grand) ** 2).sum() - ss_r - ss_c
    ms_r, ms_c, ms_e = ss_r / (n - 1), ss_c / (k - 1), ss_e / ((n - 1) * (k - 1))
    r = (ms_r - ms_e) / (ms_r + (k - 1) * ms_e + k / n * (ms_c - ms_e))
    if stats is None or not (0 < r < 1):
        return r, np.nan, np.nan
    a = k * r / (n * (1 - r))
    b = 1 + k * r * (n - 1) / (n * (1 - r))
    v = (a * ms_c + b * ms_e) ** 2 / ((a * ms_c) ** 2 / (k - 1) + (b * ms_e) ** 2 / ((n - 1) * (k - 1)))
    fl = stats.f.ppf(1 - alpha / 2, n - 1, v)
    fu = stats.f.ppf(1 - alpha / 2, v, n - 1)
    lo = n * (ms_r - fl * ms_e) / (fl * (k * ms_c + (k * n - k - n) * ms_e) + n * ms_r)
    hi = n * (fu * ms_r - ms_e) / (k * ms_c + (k * n - k - n) * ms_e + n * fu * ms_r)
    return r, lo, hi


def summarise(df, measure, subset):
    o, c = df[f"{measure}_orig"].to_numpy(float), df[f"{measure}_check"].to_numpy(float)
    d = c - o
    ad = np.abs(d)
    n = len(d)
    r = np.corrcoef(o, c)[0, 1] if n > 2 and np.std(o) > 0 and np.std(c) > 0 else np.nan
    icc, lo, hi = icc_a1(o, c)
    sd = d.std(ddof=1) if n > 1 else np.nan
    return {
        "measure": measure, "subset": subset, "n": n,
        "mean_orig_ms": o.mean(), "mean_check_ms": c.mean(),
        "bias_ms": d.mean(), "sd_diff_ms": sd,
        "loa_low_ms": d.mean() - 1.96 * sd, "loa_high_ms": d.mean() + 1.96 * sd,
        "MAD_ms": ad.mean(), "median_AD_ms": np.median(ad), "max_AD_ms": ad.max(),
        "pct_within_5ms": 100 * (ad <= 5).mean(), "pct_within_10ms": 100 * (ad <= 10).mean(),
        "pct_within_20ms": 100 * (ad <= 20).mean(),
        "pearson_r": r, "ICC_A1": icc, "ICC_CI_low": lo, "ICC_CI_high": hi,
    }


def main():
    owners = pd.read_csv(os.path.join(ROOT, "00_admin", "speakers.csv")).set_index("file")["owner"]
    rows, problems = [], []
    for rel_name, checker in PAIRS:
        name = os.path.basename(rel_name)
        orig, p1 = tokens_from_grid(os.path.join(ANN, name + ".TextGrid"))
        check, p2 = tokens_from_grid(os.path.join(REL, rel_name + ".TextGrid"))
        problems += p1 + p2
        for w in WORDS:
            if w not in orig or w not in check:
                continue
            o, c = orig[w], check[w]
            # same stretch of audio? (the two tokens must overlap in time)
            same = int(min(o["B4"], c["B4"]) > max(o["B1"], c["B1"]))
            reason = EXCLUDE.get((name, w), "")
            if not same and not reason:
                problems.append(f"{name} '{w}': the two versions do not overlap (original "
                                f"{o['B1']:.3f}-{o['B4']:.3f} s, re-annotation {c['B1']:.3f}-{c['B4']:.3f} s): "
                                f"different tokens, left out of all statistics")
            row = {"file": name, "group": name[:2], "owner": owners.get(name, ""), "checker": checker,
                   "word": w, "voicing": "voiced" if w in VOICED else "voiceless", "same_token": same,
                   "excluded": reason if reason else ("different tokens" if not same else ""),
                   "label_orig": o["label"], "label_check": c["label"],
                   "label_agree": int(o["label"] == c["label"])}
            for b in ["B1", "B2", "B3", "B4"]:
                row[f"{b}_orig_s"] = round(o[b], 4)
                row[f"{b}_check_s"] = round(c[b], 4)
            for b in ["B1", "B2", "B3", "B4"]:
                row[f"{b}_diff_ms"] = round((c[b] - o[b]) * 1000, 1)
            for meas, (s, e) in {"clDur": ("B1", "B2"), "VOT": ("B2", "B3"), "vDur": ("B3", "B4")}.items():
                row[f"{meas}_orig"] = round((o[e] - o[s]) * 1000, 1)
                row[f"{meas}_check"] = round((c[e] - c[s]) * 1000, 1)
                row[f"{meas}_diff"] = round(row[f"{meas}_check"] - row[f"{meas}_orig"], 1)
            rows.append(row)
    tok = pd.DataFrame(rows)
    tok.to_csv(os.path.join(REL, "reliability_tokens.csv"), index=False, lineterminator="\n")
    excluded = tok[tok.excluded != ""]
    tok = tok[tok.excluded == ""].copy()

    # boundaries are compared as times; express them in ms so the summary is in one unit
    for b in ["B1", "B2", "B3", "B4"]:
        tok[f"{b}_orig"] = tok[f"{b}_orig_s"] * 1000
        tok[f"{b}_check"] = tok[f"{b}_check_s"] * 1000

    both_cl = tok[(tok.label_orig == "cl") & (tok.label_check == "cl")]
    subsets = {
        "all": tok,
        "voiceless (p t k)": tok[tok.voicing == "voiceless"],
        "voiced (b g)": tok[tok.voicing == "voiced"],
        "Ala checks Weronika": tok[tok.checker == "Ala"],
        "Weronika checks Ala": tok[tok.checker == "Weronika"],
    }
    summ = []
    for meas in ["B1", "B2", "B3", "B4", "clDur", "VOT", "vDur"]:
        for sname, sdf in subsets.items():
            summ.append(summarise(sdf, meas, sname))
        if meas in ("B1", "clDur"):
            summ.append(summarise(both_cl, meas, "both cl (used in R)"))
    summ = pd.DataFrame(summ)
    # boundaries: correlation/ICC of absolute times are meaningless (they span the whole file)
    summ.loc[summ.measure.str.startswith("B"), ["mean_orig_ms", "mean_check_ms", "pearson_r", "ICC_A1",
                                                 "ICC_CI_low", "ICC_CI_high"]] = np.nan
    summ = summ.round(3)
    summ.to_csv(os.path.join(REL, "reliability_summary.csv"), index=False, lineterminator="\n")

    # label agreement (cl vs cl?) + Cohen's kappa
    tab = pd.crosstab(tok.label_orig, tok.label_check)
    po = tok.label_agree.mean()
    labs = sorted(set(tok.label_orig) | set(tok.label_check))
    pe = sum((tok.label_orig == l).mean() * (tok.label_check == l).mean() for l in labs)
    kappa = (po - pe) / (1 - pe) if pe < 1 else np.nan

    write_markdown(tok, summ, tab, po, kappa, problems, excluded)
    make_figure(tok, summ)
    print(f"{len(tok)} tokens compared; label agreement {100 * po:.1f}% (kappa {kappa:.2f})")
    for p in problems:
        print("NOTE:", p)


def fmt(x, nd=1):
    return "–" if pd.isna(x) else f"{x:.{nd}f}"


def write_markdown(tok, summ, tab, po, kappa, problems, excluded):
    L = []
    L.append("# Inter-annotator agreement (reliability check, N4 / R8)\n")
    L.append("Made by `VOT_project_scripts/reliability.py` from the `seg` tiers only (no audio). "
             "Original = the owner's TextGrid in `03_annotated`; re-annotation = the other annotator's "
             "blind version in `04_reliability/calibration_A` (Ala) or `calibration_W` (Weronika). "
             "Differences are **re-annotation − original**, in ms. All 4 files follow "
             "`00_admin/annotation_rules.md`.\n")
    files = tok.groupby(["file", "owner", "checker"]).size().reset_index(name="tokens")
    L.append("| file | original by | re-annotated by | tokens |\n|---|---|---|---|")
    for _, r in files.iterrows():
        L.append(f"| {r.file} | {r.owner} | {r.checker} | {r.tokens} |")
    L.append(f"\n**{len(tok)} tokens** compared ({len(tok) / 240 * 100:.0f}% of the 240 tokens).")
    for _, r in excluded.iterrows():
        L.append(f"Left out: {r.file} *{r.word}*: {r.excluded}.")
    L.append("")

    L.append("## 1. Durations (the measures that go into the analysis)\n")
    L.append("MAD = mean absolute difference; bias = mean signed difference; LoA = 95% limits of "
             "agreement (bias ± 1.96 SD); ICC = ICC(A,1), two-way random, absolute agreement, single "
             "rater, with 95% CI.\n")
    L.append("| measure | tokens | n | MAD | median AD | max AD | ≤5 ms | ≤10 ms | bias | LoA | r | ICC [95% CI] |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
    order = [("VOT", "all"), ("VOT", "voiceless (p t k)"), ("VOT", "voiced (b g)"),
             ("clDur", "both cl (used in R)"), ("clDur", "all"), ("vDur", "all"),
             ("vDur", "voiceless (p t k)"), ("vDur", "voiced (b g)")]
    names = {"VOT": "VOT", "clDur": "closure", "vDur": "vowel"}
    for m, s in order:
        r = summ[(summ.measure == m) & (summ.subset == s)].iloc[0]
        ci = "" if pd.isna(r.ICC_CI_low) else f" [{r.ICC_CI_low:.2f}, {r.ICC_CI_high:.2f}]"
        L.append(f"| {names[m]} | {s} | {int(r.n)} | {fmt(r.MAD_ms)} | {fmt(r.median_AD_ms)} | "
                 f"{fmt(r.max_AD_ms)} | {fmt(r.pct_within_5ms, 0)}% | {fmt(r.pct_within_10ms, 0)}% | "
                 f"{fmt(r.bias_ms)} | {fmt(r.loa_low_ms)} to {fmt(r.loa_high_ms)} | {fmt(r.pearson_r, 2)} | "
                 f"{fmt(r.ICC_A1, 2)}{ci} |")

    L.append("\n## 2. Boundaries\n")
    L.append("| boundary | n | MAD | median AD | max AD | ≤5 ms | ≤10 ms | ≤20 ms | bias |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for b, lab in [("B1", "B1 closure start"), ("B2", "B2 burst"), ("B3", "B3 vowel start"), ("B4", "B4 vowel end")]:
        r = summ[(summ.measure == b) & (summ.subset == "all")].iloc[0]
        L.append(f"| {lab} | {int(r.n)} | {fmt(r.MAD_ms)} | {fmt(r.median_AD_ms)} | {fmt(r.max_AD_ms)} | "
                 f"{fmt(r.pct_within_5ms, 0)}% | {fmt(r.pct_within_10ms, 0)}% | {fmt(r.pct_within_20ms, 0)}% | "
                 f"{fmt(r.bias_ms)} |")
    r = summ[(summ.measure == "B1") & (summ.subset == "both cl (used in R)")].iloc[0]
    L.append(f"\nB1 for the {int(r.n)} words labelled `cl` by both: MAD {fmt(r.MAD_ms)} ms, "
             f"median {fmt(r.median_AD_ms)} ms.\n")

    L.append("## 3. By direction\n")
    L.append("| measure | Ala re-annotates Weronika (MAD / bias) | Weronika re-annotates Ala (MAD / bias) |")
    L.append("|---|---|---|")
    for m in ["B1", "B2", "B3", "B4", "VOT", "clDur", "vDur"]:
        a = summ[(summ.measure == m) & (summ.subset == "Ala checks Weronika")].iloc[0]
        w = summ[(summ.measure == m) & (summ.subset == "Weronika checks Ala")].iloc[0]
        L.append(f"| {names.get(m, m)} | {fmt(a.MAD_ms)} / {fmt(a.bias_ms)} | {fmt(w.MAD_ms)} / {fmt(w.bias_ms)} |")

    L.append("\n## 4. cl vs cl? labels\n")
    L.append(f"Agreement {int(tok.label_agree.sum())}/{len(tok)} = {100 * po:.1f}%, Cohen's kappa = {kappa:.2f}.\n")
    L.append("| original \\ re-annotation | " + " | ".join(tab.columns) + " |")
    L.append("|---|" + "---|" * len(tab.columns))
    for idx, r in tab.iterrows():
        L.append(f"| {idx} | " + " | ".join(str(v) for v in r.values) + " |")
    dis = tok[tok.label_agree == 0]
    if len(dis):
        L.append("\nDisagreements: " + "; ".join(f"{r.file} {r.word} ({r.label_orig} / {r.label_check})"
                                               for _, r in dis.iterrows()) + ".\n")

    L.append("## 5. Every token (original / re-annotation, ms)\n")
    L.append("| file | word | label | VOT | Δ | closure | Δ | vowel | Δ | ΔB1 | ΔB2 | ΔB3 | ΔB4 |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for _, r in tok.iterrows():
        lab = r.label_orig if r.label_agree else f"**{r.label_orig} / {r.label_check}**"
        L.append(f"| {r.file} | {r.word} | {lab} | {r.VOT_orig:.1f} / {r.VOT_check:.1f} | {r.VOT_diff:+.1f} | "
                 f"{r.clDur_orig:.1f} / {r.clDur_check:.1f} | {r.clDur_diff:+.1f} | "
                 f"{r.vDur_orig:.1f} / {r.vDur_check:.1f} | {r.vDur_diff:+.1f} | {r.B1_diff_ms:+.1f} | "
                 f"{r.B2_diff_ms:+.1f} | {r.B3_diff_ms:+.1f} | {r.B4_diff_ms:+.1f} |")
    big = tok.assign(maxd=tok[["B1_diff_ms", "B2_diff_ms", "B3_diff_ms", "B4_diff_ms"]].abs().max(axis=1))
    L.append(f"\nTokens with a boundary more than 20 ms apart: {int((big.maxd > 20).sum())} of {len(tok)}.\n")
    def g(m, sub):
        return summ[(summ.measure == m) & (summ.subset == sub)].iloc[0]
    v, vl, vv, c, w = g("VOT", "all"), g("VOT", "voiceless (p t k)"), g("VOT", "voiced (b g)"), \
        g("clDur", "both cl (used in R)"), g("vDur", "all")
    L.append("## 6. Draft sentence for the Method section\n")
    L.append(f"> Each annotator re-annotated two speakers of the other annotator without seeing the first "
             f"version (4 speakers, one per group plus one extra Persian speaker; 32 tokens, 13% of the data). "
             f"{len(excluded)} token was left out because the first annotation was on the wrong word (a "
             f"forced-alignment error, corrected afterwards). For the remaining {len(tok)} tokens, the mean absolute difference between annotators was "
             f"{v.MAD_ms:.1f} ms for VOT (Pearson r = {v.pearson_r:.2f}, ICC(A,1) = {v.ICC_A1:.2f}; voiceless "
             f"stops ICC = {vl.ICC_A1:.2f}, voiced stops ICC = {vv.ICC_A1:.2f}), {c.MAD_ms:.1f} ms for closure "
             f"duration (tokens labelled cl by both, n = {int(c.n)}, ICC = {c.ICC_A1:.2f}) and {w.MAD_ms:.1f} ms "
             f"for vowel duration (ICC = {w.ICC_A1:.2f}). The burst (B2) was the most consistent boundary "
             f"(median difference {g('B2', 'all').median_AD_ms:.1f} ms) and the vowel end (B4) the least "
             f"(mean {g('B4', 'all').MAD_ms:.1f} ms). The closure label (cl vs cl?) agreed for "
             f"{int(tok.label_agree.sum())} of {len(tok)} tokens ({100 * po:.0f}%, Cohen's kappa = {kappa:.2f}).\n")
    if problems:
        L.append("## Notes from the script\n")
        L += [f"- {p}" for p in problems]
    with open(os.path.join(REL, "reliability_results.md"), "w", newline="\n") as fh:
        fh.write("\n".join(L) + "\n")


def make_figure(tok, summ):
    """07_figures/reliability_scatter.png: original vs re-annotation for VOT, closure, vowel."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.lines import Line2D
    except ImportError:
        print("matplotlib not installed: no figure")
        return
    blue, orange, ink, ink2, grid = "#257de0", "#f47230", "#1f1f1f", "#6b6b6b", "#e6e6e6"
    style = {"Ala": (blue, "o"), "Weronika": (orange, "s")}  # key = who re-annotated
    panels = [("VOT", "all", "VOT"),
              ("clDur", "both cl (used in R)", "Closure duration (cl in both versions)"),
              ("vDur", "all", "Vowel duration")]
    fig, axes = plt.subplots(1, 3, figsize=(13, 5.4), layout="constrained")
    for ax, (m, subset, title) in zip(axes, panels):
        d = tok if subset == "all" else tok[(tok.label_orig == "cl") & (tok.label_check == "cl")]
        lim = max(d[f"{m}_orig"].max(), d[f"{m}_check"].max()) * 1.06
        ax.plot([0, lim], [0, lim], ls="--", lw=1, color=ink2, zorder=1)
        for checker, (col, mk) in style.items():
            for voicing, face in [("voiceless", col), ("voiced", "white")]:
                dd = d[(d.checker == checker) & (d.voicing == voicing)]
                ax.scatter(dd[f"{m}_orig"], dd[f"{m}_check"], s=42, marker=mk, facecolors=face,
                           edgecolors=col, linewidths=2, zorder=3)
        r = summ[(summ.measure == m) & (summ.subset == subset)].iloc[0]
        ax.set_title(f"{title}\nn = {int(r.n)}, MAD = {r.MAD_ms:.1f} ms, ICC = {r.ICC_A1:.2f}",
                     fontsize=10, color=ink, loc="left")
        ax.set_xlim(0, lim); ax.set_ylim(0, lim); ax.set_aspect("equal")
        ax.set_xlabel("Owner's annotation (ms)", color=ink2); ax.set_ylabel("Re-annotation (ms)", color=ink2)
        ax.grid(color=grid, lw=0.8); ax.set_axisbelow(True)
        for sp in ["top", "right"]:
            ax.spines[sp].set_visible(False)
        for sp in ["left", "bottom"]:
            ax.spines[sp].set_color("#bdbdbd")
        ax.tick_params(colors=ink2, labelsize=8)
    handles = [Line2D([], [], marker="o", ls="", mec=blue, mfc=blue, mew=2, label="Ala re-annotates Weronika's files"),
               Line2D([], [], marker="s", ls="", mec=orange, mfc=orange, mew=2, label="Weronika re-annotates Ala's files"),
               Line2D([], [], marker="o", ls="", mec=ink2, mfc=ink2, mew=2, label="voiceless (filled)"),
               Line2D([], [], marker="o", ls="", mec=ink2, mfc="white", mew=2, label="voiced (hollow)"),
               Line2D([], [], ls="--", color=ink2, label="perfect agreement")]
    fig.legend(handles=handles, loc="outside lower center", ncol=5, frameon=False, fontsize=9)
    out = os.path.join(ROOT, "07_figures", "reliability_scatter.png")
    fig.savefig(out, dpi=200)
    print("figure:", out)


if __name__ == "__main__":
    sys.exit(main())
