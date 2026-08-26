#!/usr/bin/env python3
"""UNAUDITED PROBE (W8) -- value-level verdicts on the admissible
zero-singleton templates produced by w8_sat.py.

Pinned HEAD: a1196b4dca9f83452483734a3273c0c43d5cf3b5

For every template: re-audit it independently (FIE, constants, singletons,
budget), then run the exact closure kill engine in cell coordinates and, when
every block is rectangular (= rank-one admissible), in the strictly stronger
rank-one coordinates.  Verdicts other than "survivor" are proofs that no
nonzero complex values on that support can be exact.

Run: python3 w8_kill.py [files...]
"""

from __future__ import annotations

import glob
import json
import sys
from collections import Counter

import w8_core as C
from w8_symmetry import canonical_fast


def verdicts_for(geo, template):
    compat = C.compat_matrix(geo, template)
    audit = C.audit(geo, template, compat)
    cell, rank1 = C.analyse_best(geo, template, compat=compat)
    return audit, cell, rank1


def main():
    geo = C.geometry(8)
    files = sys.argv[1:] or sorted(glob.glob("results_sat_m*.json"))
    rows = []
    seen = {}
    for name in files:
        data = json.load(open(name))
        for template in data.get("found", []):
            template = tuple(template)
            key = canonical_fast(geo, template)
            audit, cell, rank1 = verdicts_for(geo, template)
            row = {"file": name, "m": audit["m"], "sigma": audit["sigma"],
                   "beta": audit["beta"], "thin": audit["thin"],
                   "fat": audit["fat"], "fie": audit["fie"],
                   "constants": audit["constants"],
                   "singletons": audit["mixed_singletons"],
                   "H_blocks": audit["H_blocks"],
                   "min_fibre": min(audit["fibre_histogram"] or {1: 1}),
                   "histogram": audit["fibre_histogram"],
                   "verdict_cell": cell["verdict"],
                   "verdict_rank1": None if rank1 is None else rank1["verdict"],
                   "detail_cell": {k: v for k, v in cell.items()
                                   if k in ("count", "word", "terms",
                                            "binomials", "relations",
                                            "mixed_fibres", "coefficients")},
                   "new_orbit": key not in seen,
                   "template": list(template)}
            seen.setdefault(key, row)
            rows.append(row)
            print(f"  m={row['m']:2d} Sigma={row['sigma']:3d} beta={row['beta']:2d}"
                  f" thin={row['thin']:2d} fat={row['fat']:2d} FIE={row['fie']}"
                  f" sing={row['singletons']} minfib={row['min_fibre']}"
                  f"  ->  {row['verdict_cell']}"
                  f" | rank1 {row['verdict_rank1']}", flush=True)
    tally = Counter(r["verdict_cell"] for r in rows)
    tally1 = Counter(str(r["verdict_rank1"]) for r in rows)
    print("\ncell-coordinate verdicts:", dict(tally))
    print("rank-one verdicts:", dict(tally1))
    print(f"distinct S_8 x S_3 orbits: {len(seen)}")
    json.dump({"rows": rows, "verdicts_cell": dict(tally),
               "verdicts_rank1": dict(tally1), "orbits": len(seen)},
              open("results_kill.json", "w"), indent=1, default=str)
    print("wrote results_kill.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
