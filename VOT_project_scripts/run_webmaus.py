#!/usr/bin/env python3
"""
run_webmaus.py - Automate WebMAUS Basic forced alignment for VOT project speakers.
Calls the official BAS WebServices REST API (CLARIN-DE):
https://clarin.phonetik.uni-muenchen.de/BASWebServices/services/runMAUSBasic

For each speaker in 03_annotated:
- Reads <name>.wav and <name>.txt
- Sends request with LANGUAGE=eng-US and OUTFORMAT=TextGrid
- Saves resulting TextGrid to:
    - 02_webmaus_original/<name>.TextGrid (untouched backup)
    - 03_annotated/<name>.TextGrid (working copy for annotation)
- Updates annotation_log.csv marking webmaus_ok = yes
"""

import csv
import glob
import os
import sys
import time
import urllib.error
import urllib.request
import uuid
import xml.etree.ElementTree as ET

API_URL = "https://clarin.phonetik.uni-muenchen.de/BASWebServices/services/runMAUSBasic"

def make_multipart_body(fields, files):
    boundary = uuid.uuid4().hex
    crlf = b"\r\n"
    data = []
    for name, value in fields.items():
        data.append(f"--{boundary}".encode("utf-8"))
        data.append(f'Content-Disposition: form-data; name="{name}"'.encode("utf-8"))
        data.append(b"")
        data.append(str(value).encode("utf-8"))
    for name, (filename, file_bytes) in files.items():
        data.append(f"--{boundary}".encode("utf-8"))
        data.append(f'Content-Disposition: form-data; name="{name}"; filename="{filename}"'.encode("utf-8"))
        data.append(b"Content-Type: application/octet-stream")
        data.append(b"")
        data.append(file_bytes)
    data.append(f"--{boundary}--".encode("utf-8"))
    data.append(b"")
    body = crlf.join(data)
    content_type = f"multipart/form-data; boundary={boundary}"
    return body, content_type

def align_file(wav_path, txt_path, language="eng-US"):
    with open(wav_path, "rb") as f:
        wav_bytes = f.read()
    with open(txt_path, "rb") as f:
        txt_bytes = f.read()

    fields = {
        "LANGUAGE": language,
        "OUTFORMAT": "TextGrid",
    }
    files = {
        "SIGNAL": (os.path.basename(wav_path), wav_bytes),
        "TEXT": (os.path.basename(txt_path), txt_bytes),
    }

    body, content_type = make_multipart_body(fields, files)
    req = urllib.request.Request(API_URL, data=body, headers={"Content-Type": content_type})

    req_start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            resp_bytes = resp.read()
    except urllib.error.URLError as e:
        return False, f"Network/HTTP error: {e}"

    try:
        root = ET.fromstring(resp_bytes)
    except Exception as e:
        return False, f"XML parsing error: {e}\nResponse: {resp_bytes[:200]}"

    success_elem = root.find("success")
    success = success_elem is not None and success_elem.text.strip().lower() == "true"
    
    if not success:
        out_msg = root.find("output")
        err_msg = out_msg.text if out_msg is not None else "Unknown error"
        return False, f"WebMAUS error: {err_msg}"

    download_link_elem = root.find("downloadLink")
    if download_link_elem is None or not download_link_elem.text:
        return False, "No download link in response"

    download_url = download_link_elem.text.strip()
    try:
        with urllib.request.urlopen(download_url, timeout=60) as dl_resp:
            grid_bytes = dl_resp.read()
    except Exception as e:
        return False, f"Failed to download TextGrid: {e}"

    elapsed = time.time() - req_start
    return True, (grid_bytes, elapsed)

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    annotated_dir = os.path.join(base_dir, "03_annotated")
    original_dir = os.path.join(base_dir, "02_webmaus_original")
    admin_dir = os.path.join(base_dir, "00_admin")
    log_path = os.path.join(admin_dir, "annotation_log.csv")

    os.makedirs(original_dir, exist_ok=True)
    os.makedirs(annotated_dir, exist_ok=True)

    wav_files = sorted(glob.glob(os.path.join(annotated_dir, "*.wav")))
    if not wav_files:
        print(f"No .wav files found in {annotated_dir}")
        return

    print(f"Found {len(wav_files)} audio files to align.")
    aligned_speakers = []

    for idx, wav_path in enumerate(wav_files, 1):
        spk = os.path.splitext(os.path.basename(wav_path))[0]
        txt_path = os.path.splitext(wav_path)[0] + ".txt"
        
        orig_tg = os.path.join(original_dir, f"{spk}.TextGrid")
        annot_tg = os.path.join(annotated_dir, f"{spk}.TextGrid")

        if os.path.exists(orig_tg) and os.path.exists(annot_tg):
            print(f"[{idx}/{len(wav_files)}] Skipping {spk} (already aligned)")
            aligned_speakers.append(spk)
            continue

        if not os.path.exists(txt_path):
            print(f"[{idx}/{len(wav_files)}] ERROR: Missing text file {txt_path}")
            continue

        print(f"[{idx}/{len(wav_files)}] Aligning {spk} via WebMAUS Basic API... ", end="", flush=True)
        ok, res = align_file(wav_path, txt_path, language="eng-US")
        if ok:
            grid_bytes, elapsed = res
            with open(orig_tg, "wb") as f:
                f.write(grid_bytes)
            with open(annot_tg, "wb") as f:
                f.write(grid_bytes)
            print(f"DONE in {elapsed:.1f}s -> Saved TextGrid to 02_webmaus_original & 03_annotated")
            aligned_speakers.append(spk)
        else:
            print(f"FAILED: {res}")

    # Update annotation_log.csv
    if os.path.exists(log_path):
        rows = []
        with open(log_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for r in reader:
                if r["file"] in aligned_speakers:
                    r["webmaus_ok"] = "yes"
                rows.append(r)
        
        with open(log_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"\nUpdated {log_path} (marked webmaus_ok = yes for {len(aligned_speakers)} speakers).")

if __name__ == "__main__":
    main()
