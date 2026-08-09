#!/usr/bin/env python3
"""Discover compact m=11 root-RUP palettes extending the m=10 basis."""

from __future__ import annotations

import argparse
import hashlib
import json
import os

import verify_n8_d1_m11_full_shadow as C


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-at", type=int, default=0)
    parser.add_argument("--fresh", action="store_true")
    args = parser.parse_args()
    branches, _admissible, _sigma, _off_sigma, _census = C.family_branches()
    if os.path.exists(C.PALETTE_PATH) and not args.fresh:
        with open(C.PALETTE_PATH, "rb") as handle:
            palettes = C.H.decode_palettes(json.loads(handle.read()))
    else:
        with open(C.B.PALETTE_PATH, "rb") as handle:
            palettes = C.H.decode_palettes(json.loads(handle.read()))
    for position, (family, index, _state, _additions) in enumerate(branches):
        if position < args.start_at:
            continue
        row, palettes = C.run_worker(family, index, palettes, discover=True)
        raw = json.dumps(C.H.encode_palettes(palettes), sort_keys=True,
                         separators=(",", ":")).encode("ascii")
        with open(C.PALETTE_PATH, "wb") as handle:
            handle.write(raw)
        print("%d %s:%d residuals=%d palettes=%d"
              % (position, family, index,
                 row["complete_support_residuals"], len(palettes)),
              flush=True)
    raw = json.dumps(C.H.encode_palettes(palettes), sort_keys=True,
                     separators=(",", ":")).encode("ascii")
    digest = hashlib.sha256(raw).hexdigest()
    if C.EXPECTED_PALETTE_SHA256 != "TO_BE_FROZEN":
        C.require(digest == C.EXPECTED_PALETTE_SHA256,
                  "the deterministic m=11 palettes changed")
    print("wrote:", C.PALETTE_PATH)
    print("palettes:", len(palettes))
    print("sha256:", digest)


if __name__ == "__main__":
    main()
