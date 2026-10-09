#!/usr/bin/env python3
"""Pin the frame-descent search, witness and exact replay dependencies."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
FILES = [
    "research/paired-cube-diagonal-bit-168-followup/README.md",
    "research/paired-cube-diagonal-bit-168-followup/PROOF.md",
    "research/paired-cube-diagonal-bit-168-followup/NOTICE",
    "research/paired-cube-diagonal-bit-168-followup/search.py",
    "research/paired-cube-diagonal-bit-168-followup/verify.py",
    "research/paired-cube-diagonal-bit-168-followup/pin_sources.py",
    "research/paired-cube-diagonal-bit-168-followup/frame-descent.json",
    "research/paired-cube-diagonal-bit-168/SOURCE.json",
    "research/paired-cube-diagonal-bit-168/references/pr200-upstream-SOURCE.json",
    "research/source-assisted/global/assemble_profiles.py",
    "research/source-assisted/global/FINITE_BRIDGE.txt",
    "research/source-assisted-v4/assemble.py",
]


def main():
    files = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
             for name in FILES if (ROOT / name).is_file()}
    (OUT / "SOURCE.json").write_text(
        json.dumps({"files": files, "scope": "Frozen search, exact frame witness, derived certificate and pricing dependencies."},
                   indent=2, sort_keys=True) + "\n", encoding="utf-8")
    missing = [name for name in FILES if name not in files]
    if missing:
        print("Awaiting derived files:", ", ".join(missing))
    print(f"Pinned {len(files)} available sources; {len(missing)} derived outputs pending")


if __name__ == "__main__":
    main()
