#!/usr/bin/env python3
"""Join the two modular remainder supports to literal colour-content labels."""
from hashlib import sha256
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COORDS = (ROOT / "computations/unaudited-codex-orbit0-filtered-k17-census-2026-08-23"
          / "k17_colour_content_first_shell_coordinates.tsv")
OUT = HERE / "target_remainder_common_support.tsv"
RESULT = HERE / "results_remainder_support.json"


def load(prime):
    lines = (HERE / f"target_remainder_p{prime}.tsv").read_text().splitlines()
    if lines[0] != "coordinate_id\tresidue":
        raise RuntimeError(lines[0])
    return {int(row.split("\t")[0]): int(row.split("\t")[1]) for row in lines[1:]}


def main():
    labels = {}
    for row in COORDS.read_text().splitlines()[1:]:
        ident, label, *_ = row.split("\t")
        labels[int(ident)] = label
    left, right = load(32003), load(32009)
    if left.keys() != right.keys() or len(left) != 4612:
        raise RuntimeError((len(left), len(right), len(left.keys() ^ right.keys())))
    lines = ["coordinate_id\tcolour_content_type\tresidue_p32003\tresidue_p32009"]
    lines.extend(f"{key}\t{labels[key]}\t{left[key]}\t{right[key]}" for key in sorted(left))
    OUT.write_text("\n".join(lines) + "\n")
    result = {
        "status": "EXACT_COMMON_MODULAR_REMAINDER_SUPPORT",
        "support": 4612,
        "coordinate_sha256": sha256(COORDS.read_bytes()).hexdigest(),
        "output_sha256": sha256(OUT.read_bytes()).hexdigest(),
        "scope": "normal-form support for the capped literal first shell at p32003 and p32009",
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
