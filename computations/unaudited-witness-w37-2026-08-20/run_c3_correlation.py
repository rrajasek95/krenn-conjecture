"""W37 / C3 -- DOES LOWER DEFECT COUNT BUY WITNESSES?  (UNAUDITED)

C2 found a witness-bearing sample inside F8's own X_3 component, and it
carried FEWER off-count-4/5 defects (94) than the all-blocked ones
(103-113).  That is exactly the brief's central question in measurable
form: as a point moves UP the ladder (fewer X_4/X_5 violations), do
witnesses appear?

C3 samples F8's local component broadly (every site with positive
solution dimension, many draws, two independent samplers) and records
(number of defects, number of witnesses) at each point, then reports the
joint distribution.  Ledger 25: the witness count is a DISJUNCTION over
caps decided exactly, so no sampling bias in the per-point verdict; the
sampling is over POINTS and is reported as such.
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
from collections import Counter
from fractions import Fraction
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "unaudited-x3core-w25-2026-08-15"))

import w37_core as C
import w37_decide as D
from run_c1_builder import solve_affine, site_rows, apply_site, words_upto

OUT = os.path.join(HERE, "results_c3_correlation.json")
RES = {"lane": "W37", "task": "C3 defect/witness correlation",
       "unaudited": True, "points": []}


def load_f8():
    return C.parse_source(json.load(open(os.path.join(
        HERE, "..", "unaudited-x3core-w25-2026-08-15",
        "OBJECT_W25-F8_n8_allblocked_X3.json")))["blocks"], 8)


def main():
    t0 = time.time()
    src = load_f8()
    W3 = words_upto(3)
    sysmem = {}
    for z in range(8):
        sysmem[z] = site_rows(src, z, W3)
    order = [1, 7, 3, 4, 5, 6, 0, 2]
    seeds = [(0, "A"), (1, "B")]
    n_done = 0
    for spread in (1, 2, 4):
        for z in order:
            rws, rhs, idx, nc = sysmem[z]
            for si, tag in seeds:
                for t in range(4):
                    rng = random.Random(hash((z, spread, si, t)) % 10 ** 9)
                    x = solve_affine(rws, rhs, nc, rng, spread=spread)
                    if x is None:
                        continue
                    s2 = apply_site(src, z, x, idx)
                    if not C.in_Xk(s2, 8, 3):
                        continue
                    _, bad = C.defects(s2, 8)
                    live = [(p, q) for p, q in combinations(range(8), 2)
                            if C.is_live(s2, p, q)]
                    wit = []
                    for (p, q) in live:
                        U = tuple(a for a in range(8) if a not in (p, q))
                        if D.decide_pair(s2, p, q, U, chars=(0,), timeout=180,
                                         do_search=False)["verdict"] \
                                == "WITNESS":
                            wit.append([p, q])
                    oc = Counter(C.offcount(w) for w in bad)
                    rec = {"site": z, "spread": spread, "sampler": tag,
                           "trial": t, "n_live": len(live),
                           "n_defects": len(bad),
                           "off4": oc.get(4, 0), "off5": oc.get(5, 0),
                           "n_witness": len(wit), "witness_pairs": wit}
                    RES["points"].append(rec)
                    n_done += 1
                    print(f"   z={z} spread={spread} {tag}{t}: defects "
                          f"{len(bad)} (off4 {oc.get(4,0)}, off5 "
                          f"{oc.get(5,0)}), witnesses {len(wit)}", flush=True)
                    if len(wit):
                        C.ckpt(os.path.join(
                            HERE, f"OBJECT_W37_X3witness_{z}_{spread}_{tag}{t}"
                                  ".json"),
                            {"blocks": {f"{u},{v}":
                                        [[str(a) for a in r] for r in m]
                                        for (u, v), m in s2.items()},
                             "N": 8, "witness_pairs": wit,
                             "n_defects": len(bad)})
                    C.ckpt(OUT, RES)
    pts = RES["points"]
    tab = Counter((p["n_witness"] > 0, p["n_defects"]) for p in pts)
    RES["summary"] = {
        "n_points": len(pts),
        "n_with_witness": sum(1 for p in pts if p["n_witness"] > 0),
        "defects_when_witness": sorted(p["n_defects"] for p in pts
                                       if p["n_witness"] > 0),
        "defects_when_blocked": sorted(p["n_defects"] for p in pts
                                       if p["n_witness"] == 0),
        "joint": {str(k): v for k, v in tab.items()},
        "seconds": round(time.time() - t0, 1)}
    C.ckpt(OUT, RES)
    print("\nSUMMARY", json.dumps(RES["summary"])[:1200])


if __name__ == "__main__":
    main()
