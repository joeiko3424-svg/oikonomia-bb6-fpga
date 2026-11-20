#!/usr/bin/env python3
import re
import urllib.request

WORK_DIR = "/home/ubuntu/bb6_fpga_frontier"
URL = "https://wiki.bbchallenge.org/w/images/5/5e/BB6_holdouts_608.txt"
HALF_RE = r"(?:[01][LR][A-FZ\-]|---)"
TM_REGEX = re.compile(rf"^({HALF_RE}{{2}}_{HALF_RE}{{2}}_{HALF_RE}{{2}}_{HALF_RE}{{2}}_{HALF_RE}{{2}}_{HALF_RE}{{2}})$")

req = urllib.request.Request(URL, headers={"User-Agent": "Oikonomia-BB6-Audit/1.0"})
lines = [l.strip() for l in urllib.request.urlopen(req, timeout=20).read().decode("utf-8", errors="ignore").splitlines() if l.strip()]

records = []
skipped = []
for line in lines:
    parts = line.split()
    if len(parts) >= 2 and TM_REGEX.match(parts[1]):
        records.append((f"BB6_SEED_{parts[0]}", parts[1], "bb6_holdouts_608"))
    elif len(parts) == 1 and TM_REGEX.match(parts[0]):
        records.append((f"BB6_HOLDOUT_{len(records)+1:04d}", parts[0], "bb6_holdouts_608"))
    else:
        skipped.append(line)

out_tsv = f"{WORK_DIR}/bb6_holdouts_corpus.tsv"
with open(out_tsv, "w") as f:
    f.write("machine_id\tbbchallenge_code\tprovenance\n")
    for mid, code, prov in records:
        f.write(f"{mid}\t{code}\t{prov}\n")

print(f"[+] Loaded {len(records)} / {len(lines)} official BB(6) holdouts (skipped={len(skipped)}) -> {out_tsv}")
if skipped:
    print("    Skipped sample:", skipped[:3])
