"""W37 / A2 -- THE EXACT COUNTERFACTUAL DECISIONS AT F8 (UNAUDITED).

A1's cap search is ONE-SIDED (ledger 25): it can find witnesses, never
prove blockage.  A2 decides each system exactly with Singular.

Systems decided at every live pair (p,q) of F8:
  E0    the true cap system                      (must reproduce ALL BLOCKED)
  E-X4  as if F8 were in X_4  (the 78 off-count-4 defects zeroed)
  E-X5  as if F8 were EXACT   (all 103 defects zeroed)
  E-o5  the 25 off-count-5 defects zeroed only   (the complementary probe)

LEDGER 28 CONTROL (first, and it must fire): the same pipeline on
Delta^3_8 -- a known X_3 point at N=8 that CARRIES witnesses.  If the
pipeline reports no witness there, every zero below is meaningless.
"""
from __future__ import annotations

import json
import os
import sys
import time
from fractions import Fraction
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "unaudited-x3core-w25-2026-08-15"))

import w37_core as C
import w37_decide as D
from run_a1_falsifier import decide_cleaned, search_cleaned

OUT = os.path.join(HERE, "results_a2_counterfactual.json")
RES = {"lane": "W37", "task": "A2 exact counterfactual decisions",
       "unaudited": True, "rows": []}
DECLARED = ["ctrl_ledger28_delta3_8", "E0", "E_X4", "E_X5", "E_o5"]
RAN = []


def load_f8():
    d = json.load(open(os.path.join(HERE, "..",
                                    "unaudited-x3core-w25-2026-08-15",
                                    "OBJECT_W25-F8_n8_allblocked_X3.json")))
    return C.parse_source(d["blocks"], d["N"])


def ctrl_ledger28():
    """A known X_3 point at N=8 WITH witnesses must pass the same pipeline."""
    import w25_core as W25
    src25 = W25.delta3_N(8)
    src = {k: [[Fraction(x) for x in row] for row in v]
           for k, v in src25.items()}
    _, bad = C.defects(src, 8)
    print(f"  Delta^3_8: in X_3 = {C.in_Xk(src, 8, 3)}, "
          f"{len(bad)} defects, off-counts "
          f"{sorted(set(C.offcount(w) for w in bad))}")
    hits = []
    for p, q in combinations(range(8), 2):
        if not C.is_live(src, p, q):
            continue
        U = tuple(x for x in range(8) if x not in (p, q))
        K, _ = D.search_witness(src, p, q, U)
        if K is not None:
            hits.append([p, q])
    print(f"  search fires at {len(hits)} pairs: {hits[:12]}")
    assert hits, "LEDGER 28: the cap search never fires -- pipeline is hollow"
    # and the cleaned path must fire too (it is the path used below)
    p, q = hits[0]
    U = tuple(x for x in range(8) if x not in (p, q))
    K2 = search_cleaned(src, p, q, U, sorted(bad))
    K3 = search_cleaned(src, p, q, U, [])
    print(f"  cleaned-path search at {p},{q}: Z=all -> "
          f"{'hit' if K2 else 'MISS'}, Z=empty -> {'hit' if K3 else 'MISS'}")
    assert K3 is not None, "cleaned path with Z=empty must equal the true system"
    return {"n_defects": len(bad), "search_hit_pairs": hits,
            "cleaned_path_Zempty_hit": K3 is not None,
            "cleaned_path_Zall_hit": K2 is not None}


def main():
    t0 = time.time()
    print("=== A2.0 LEDGER-28 POSITIVE CONTROL ===", flush=True)
    RES["ctrl_ledger28_delta3_8"] = ctrl_ledger28()
    RAN.append("ctrl_ledger28_delta3_8")
    C.ckpt(OUT, RES)

    src = load_f8()
    _, bad = C.defects(src, 8)
    allZ = sorted(bad)
    Z4 = [w for w in allZ if C.offcount(w) == 4]
    Z5 = [w for w in allZ if C.offcount(w) == 5]
    live = [(p, q) for p, q in combinations(range(8), 2)
            if C.is_live(src, p, q)]
    systems = [("E_X5", allZ), ("E_X4", Z4), ("E0", []), ("E_o5", Z5)]

    done = set()
    if os.path.exists(OUT + ".resume"):
        for r in json.load(open(OUT + ".resume")):
            done.add((r["system"], r["pair"][0], r["pair"][1]))
            RES["rows"].append(r)

    for name, Z in systems:
        print(f"\n=== A2 system {name} (|Z| = {len(Z)}) ===", flush=True)
        for (p, q) in live:
            if (name, p, q) in done:
                continue
            U = tuple(x for x in range(8) if x not in (p, q))
            t = time.time()
            v = decide_cleaned(src, p, q, U, Z, char=0, timeout=600)
            row = {"system": name, "pair": [p, q], "verdict": v,
                   "sec": round(time.time() - t, 1)}
            RES["rows"].append(row)
            print(f"   {name} {p},{q}: {v}  ({row['sec']}s)", flush=True)
            C.ckpt(OUT, RES)
            with open(OUT + ".resume", "w") as fh:
                json.dump(RES["rows"], fh)
        RAN.append(name)
        summary = {}
        for r in RES["rows"]:
            if r["system"] == name:
                summary[r["verdict"]] = summary.get(r["verdict"], 0) + 1
        RES.setdefault("summary", {})[name] = summary
        print(f"   >>> {name}: {summary}", flush=True)
        C.ckpt(OUT, RES)

    RES["seconds"] = round(time.time() - t0, 1)
    RES["manifest"] = {"declared": DECLARED, "ran": RAN,
                       "missing": [x for x in DECLARED if x not in RAN]}
    C.ckpt(OUT, RES)
    print("\nMANIFEST", RES["manifest"], flush=True)


if __name__ == "__main__":
    main()
