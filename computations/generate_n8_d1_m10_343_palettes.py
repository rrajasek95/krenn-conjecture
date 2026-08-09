#!/usr/bin/env python3
"""Discover the deterministic compact root-RUP palette basis for 3+4+3."""

from __future__ import annotations

import argparse
import hashlib
import json
import os

import verify_n8_d1_m10_343_full_shadow as C


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-at", type=int, default=0)
    args = parser.parse_args()
    branches, _admissible, _sigma, _off_sigma = C.family_branches()
    if os.path.exists(C.PALETTE_PATH):
        with open(C.PALETTE_PATH, "rb") as handle:
            palettes = C.decode_palettes(json.loads(handle.read()))
    else:
        palettes = []
    rows = []
    for index, _state in branches:
        if index < args.start_at:
            continue
        row, palettes = C.run_worker(index, palettes, discover=True)
        rows.append(row)
        raw = json.dumps(C.encode_palettes(palettes), sort_keys=True,
                         separators=(",", ":")).encode("ascii")
        with open(C.PALETTE_PATH, "wb") as handle:
            handle.write(raw)
        print("343:%d residuals=%d palettes=%d"
              % (index, row["complete_support_residuals"], len(palettes)),
              flush=True)
    raw = json.dumps(C.encode_palettes(palettes), sort_keys=True,
                     separators=(",", ":")).encode("ascii")
    print("wrote:", C.PALETTE_PATH)
    print("palettes:", len(palettes))
    digest = hashlib.sha256(raw).hexdigest()
    if digest != C.EXPECTED_PALETTE_SHA256:
        raise RuntimeError("the deterministic 3+4+3 palettes changed")
    print("sha256:", digest)


if __name__ == "__main__":
    main()
