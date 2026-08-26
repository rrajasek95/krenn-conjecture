#!/usr/bin/env python3
"""UNAUDITED PROBE (W12) -- structural dump of the two targets."""

from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w12_core as C  # noqa: E402
from run_t4_calibration import load_survivor, load_immunity  # noqa: E402


def dump(geo, template, name):
    print(f"===== {name} =====")
    print(f"m={C.support(template)} Sigma={C.sigma(template)}")
    full = []
    for e, mask in enumerate(template):
        if not mask:
            continue
        u, v = geo.edges[e]
        kind = C.block_class(mask)
        cc = C.cells(mask)
        if mask == C.FULL9:
            full.append((u, v))
        print(f"  edge {u}{v} [{kind:6s}] n={len(cc)} cells={cc}")
    print(f"  FULL nine-cell blocks ({len(full)}): {full}")
    # degrees in the full-block graph
    deg = {}
    for (u, v) in full:
        deg[u] = deg.get(u, 0) + 1
        deg[v] = deg.get(v, 0) + 1
    print(f"  full-block degrees: {[deg.get(x,0) for x in range(8)]}")
    # matchings supported on every word ("universal")
    universal = []
    fullset = {geo.eindex[e] for e in full}
    for n, me in enumerate(geo.medges):
        if all(e in fullset for e in me):
            universal.append(tuple(geo.edges[e] for e in me))
    print(f"  universal matchings: {len(universal)} -> {universal}")
    # single-cell (R) graph
    R = [(geo.edges[e], C.cells(mask)[0]) for e, mask in enumerate(template)
         if bin(mask).count("1") == 1]
    print(f"  single cells ({len(R)}):")
    for (u, v), (i, j) in R:
        print(f"     ({u},{v}) cell ({i},{j}) -> serves demand ({u},{j}) and ({v},{i})")
    dem = C.fie_demands(geo, template)
    unserved = [k for k, v in dem.items() if not v]
    print(f"  unserved (SC) demands: {unserved}")
    return {"full": full, "universal": [list(map(list, u)) for u in universal],
            "singles": [[list(uv), list(ij)] for uv, ij in R]}


def main():
    geo = C.geometry()
    out = {}
    surv = load_survivor()
    out["survivor"] = dump(geo, surv, "SURVIVOR m=20 Sigma=58")
    imm = load_immunity()
    for m, tmpl, _ in imm[:3]:
        out[f"immunity_m{m}"] = dump(geo, tmpl, f"IMMUNITY m={m}")
    with open(os.path.join(HERE, "results_t0_structure.json"), "w") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
