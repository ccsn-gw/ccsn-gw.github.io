#!/usr/bin/env python3
"""Rebuild the waveform explorer's data from a 6EOS_4M-style CSV.

Usage:  python tools/build_explorer_data.py path/to/6EOS_4M.csv

Writes data/signals.txt (all strain series, 16-bit, base64) and replaces the
`const DATA=...;` line in index.html (labels for every signal).
CSV layout: a header row with the time axis [ms] followed by five label names,
then one signal per row: strain samples, Mass, EOS, T/|W|, f_peak, D Delta h.
"""
import base64, json, pathlib, re, sys

import numpy as np
import pandas as pd

root = pathlib.Path(__file__).resolve().parent.parent
df = pd.read_csv(sys.argv[1])
n = df.shape[1] - 5
t = df.columns[:n].astype(float).to_numpy()
strain = df.iloc[:, :n].to_numpy(dtype=np.float64)
labels = df.iloc[:, n:].to_numpy(dtype=float)

scale = np.abs(strain).max(axis=1)
scale[scale == 0] = 1
packed = np.round(strain / scale[:, None] * 32767).astype("<i2")
(root / "data").mkdir(exist_ok=True)
(root / "data" / "signals.txt").write_text(base64.b64encode(packed.tobytes()).decode())

rows = [[int(m), int(e), round(b, 5), int(f), round(d, 1), round(a, 3)]
        for (m, e, b, f, d), a in zip(labels, scale)]
data = json.dumps({"t0": float(t[0]), "dt": float(t[1] - t[0]), "n": int(n), "rows": rows},
                  separators=(",", ":"))

page = root / "index.html"
html = page.read_text(encoding="utf-8")
html, count = re.subn(r"const DATA=\{.*?\};", lambda _: f"const DATA={data};", html, count=1, flags=re.S)
if count != 1:
    sys.exit("Could not find the `const DATA=...;` line in index.html")
page.write_text(html, encoding="utf-8")
print(f"{len(rows)} signals, {n} samples each -> data/signals.txt and index.html updated")
