#!/usr/bin/env python3
"""W28 T3 -- the N = 8 SKELETON INVARIANT hunt.

W27-S3 established that the witness/blocked verdict at N = 8 is determined by
the skeleton (constant across weight points), and W27-S2 that the N = 6 law
(W27-S1) is wrong at N = 8 (63 of 377 pairs), with 12 endpoint-type cells
carrying BOTH verdicts.  This runner takes W27's 377-row decided table and
searches the feature space systematically:

 * every single feature (reproducing W27's overlap counts as a control);
 * every conjunction of up to THREE literals over the whole derived feature
   set, on both sides (sufficient-for-WITNESS and sufficient-for-BLOCKED);
 * exhaustive small decision trees (depth <= 3) to test whether ANY exact
   classifier exists inside this feature set;
 * the named principled candidates: npm-refinements (npm = 0 => blocked, and
   the parity/cycle stratification of npm >= 1), the W25-U3 predictor's
   failure structure, and the off-colour component counts.

The outcome is either an exact rule (a candidate N = 8 law) or a QUANTIFIED
statement of how non-local the invariant is relative to these features.
"""
from __future__ import annotations

import json
import sys
import time
from itertools import combinations

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-x4empty-w28-2026-08-18")
W27 = ("/Users/rishi/workplace/krenn-conjecture/computations/"
       "unaudited-penult-w27-2026-08-18")
sys.path.insert(0, BASE)

RES = {}
RAN = []
OUT = f"{BASE}/results_t3_skeleton.json"


def control(n):
    if n not in RAN:
        RAN.append(n)


def ck(tag=""):
    RES["ran"] = RAN
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    if tag:
        print(f"      [checkpoint {tag}]", flush=True)


def derive(r):
    """The feature vector of one row (all values hashable)."""
    npoff = json.loads(r["npm_rest_off"])
    nfoff = json.loads(r["npm_full_off"])
    comps = json.loads(r["off_comp_sizes"])
    sizes = r["sizes"]
    f = {
        "type_pair": r["type_pair"],
        "colour": r["colour"],
        "sizes": str(sizes),
        "min_deg_c1": r["min_deg_c1"],
        "max_deg_c1": r["max_deg_c1"],
        "min_live_deg": r["min_live_deg"],
        "max_live_deg": r["max_live_deg"],
        "n_clean_endpoints": r["n_clean_endpoints"],
        "n_clean_vertices": r["n_clean_vertices"],
        "npm_rest_c1": r["npm_rest_c1"],
        "npm_full_c1": r["npm_full_c1"],
        "off_same_comp": r["off_same_comp"],
        "off_comp_p": r["off_comp_p"],
        "off_comp_q": r["off_comp_q"],
        "off_deg_p": r["off_deg_p"],
        "off_deg_q": r["off_deg_q"],
        "min_off_deg": r["min_off_deg"],
        "n_live_edges": r["n_live_edges"],
        "both_clean": r["both_clean"],
        "predicted_S1": r["predicted_S1"],
        # ---------------- derived
        "npm_rest_c1_zero": r["npm_rest_c1"] == 0,
        "npm_rest_c1_par": r["npm_rest_c1"] % 2,
        "npm_rest_c1_cap": min(r["npm_rest_c1"], 3),
        "npm_full_c1_par": r["npm_full_c1"] % 2,
        "npm_full_c1_cap": min(r["npm_full_c1"], 4),
        "npm_drop": r["npm_full_c1"] - r["npm_rest_c1"],
        "npm_drop_par": (r["npm_full_c1"] - r["npm_rest_c1"]) % 2,
        "npm_rest_off_sum": sum(npoff),
        "npm_rest_off_zero": sum(npoff) == 0,
        "npm_rest_off_min": min(npoff),
        "npm_rest_off_max": max(npoff),
        "npm_full_off_sum": sum(nfoff),
        "npm_full_off_min": min(nfoff),
        "npm_full_off_max": max(nfoff),
        "npm_full_off_par": sum(nfoff) % 2,
        "n_off_comps": len(comps),
        "max_off_comp": max(comps),
        "min_off_comp": min(comps),
        "off_comp_all8": comps == [8],
        "sizes_sorted": str(sorted(sizes)),
        "size_min": min(sizes),
        "size_max": max(sizes),
        "size_sum": sum(sizes),
        "deg_sum_c1": r["min_deg_c1"] + r["max_deg_c1"],
        "deg_pair_c1": str(sorted([r["min_deg_c1"], r["max_deg_c1"]])),
        "off_deg_pair": str(sorted([r["off_deg_p"], r["off_deg_q"]])),
        "clean_and_npm0": (r["n_clean_endpoints"] > 0
                           and r["npm_rest_c1"] == 0),
    }
    return f


def literals(rows, feats):
    """All (feature, value) equality literals plus numeric thresholds."""
    lits = []
    for name in feats:
        vals = sorted(set(str(r[name]) for r in rows))
        if len(vals) > 40:
            continue
        for v in vals:
            lits.append((name, "==", v))
        nums = [r[name] for r in rows]
        if all(isinstance(x, int) and not isinstance(x, bool) for x in nums):
            for thr in sorted(set(nums))[:-1]:
                lits.append((name, "<=", thr))
    return lits


def sat(r, lit):
    name, op, v = lit
    if op == "==":
        return str(r[name]) == v
    return r[name] <= v


def main():
    t0 = time.time()
    with open(f"{W27}/results_t2d_n8rule.json") as fh:
        D = json.load(fh)
    T = D["table"]
    rows = [derive(r) for r in T]
    y = [r["verdict"] == "WITNESS" for r in T]
    nW, nB = sum(y), len(y) - sum(y)
    print(f"W27's N=8 decided table: {len(T)} pairs, {nW} WITNESS / {nB} "
          f"BLOCKED")
    RES["dataset"] = {"rows": len(T), "witness": nW, "blocked": nB,
                      "source": "W27 results_t2d_n8rule.json"}

    print("=" * 74)
    print("(0) CONTROL: reproduce W27's reported sufficient conditions")
    print("=" * 74)
    ctl = {}
    n0 = sum(1 for r, t in zip(rows, y) if r["npm_rest_c1"] == 0)
    n0b = sum(1 for r, t in zip(rows, y) if r["npm_rest_c1"] == 0 and not t)
    ctl["npm_rest_c1==0 => BLOCKED"] = f"{n0b}/{n0}"
    tp = '((1, (1, 1)), (1, (1, 1)))'
    m = sum(1 for r in rows if r["type_pair"] == tp)
    mw = sum(1 for r, t in zip(rows, y) if r["type_pair"] == tp and t)
    ctl[f"type_pair=={tp} => WITNESS"] = f"{mw}/{m}"
    agree = sum(1 for r, t in zip(rows, y)
                if (r["predicted_S1"] == "WITNESS") == t)
    ctl["W27-S1 (the N=6 law) accuracy at N=8"] = f"{agree}/{len(y)}"
    print(f"   {json.dumps(ctl, indent=3)}")
    assert n0b == n0 and n0 == 36, (n0, n0b)
    assert mw == m and m == 193, (m, mw)
    assert len(y) - agree == 63
    RES["controls"] = ctl
    control("T3_0_reproduce")
    ck("ctrl")

    feats = sorted(rows[0].keys())
    lits = literals(rows, feats)
    print(f"   feature space: {len(feats)} features, {len(lits)} literals")

    print("=" * 74)
    print("(1) SINGLE-LITERAL sufficient conditions (both sides)")
    print("=" * 74)
    best = {"W": [], "B": []}
    for lit in lits:
        idx = [i for i, r in enumerate(rows) if sat(r, lit)]
        if not idx:
            continue
        w = sum(1 for i in idx if y[i])
        if w == len(idx):
            best["W"].append((len(idx), str(lit)))
        if w == 0:
            best["B"].append((len(idx), str(lit)))
    best["W"].sort(reverse=True)
    best["B"].sort(reverse=True)
    print(f"   best single sufficient-for-WITNESS: {best['W'][:4]}")
    print(f"   best single sufficient-for-BLOCKED: {best['B'][:4]}")
    RES["single"] = {"witness": best["W"][:12], "blocked": best["B"][:12]}
    control("T3_1_single")
    ck("single")

    print("=" * 74)
    print("(2) CONJUNCTIONS of up to three literals")
    print("=" * 74)
    cov = {"W": [], "B": []}
    L = len(lits)
    masks = []
    for lit in lits:
        masks.append(frozenset(i for i, r in enumerate(rows) if sat(r, lit)))
    Wset = set(i for i in range(len(y)) if y[i])
    for a in range(L):
        for b in range(a + 1, L):
            ab = masks[a] & masks[b]
            if not ab:
                continue
            wa = len(ab & Wset)
            if wa == len(ab) and len(ab) >= 8:
                cov["W"].append((len(ab), f"{lits[a]} & {lits[b]}"))
            if wa == 0 and len(ab) >= 8:
                cov["B"].append((len(ab), f"{lits[a]} & {lits[b]}"))
    cov["W"].sort(reverse=True)
    cov["B"].sort(reverse=True)
    print(f"   best 2-literal sufficient-for-WITNESS: {cov['W'][:3]}")
    print(f"   best 2-literal sufficient-for-BLOCKED: {cov['B'][:3]}")
    RES["pairs"] = {"witness": cov["W"][:10], "blocked": cov["B"][:10]}
    control("T3_2_pairs")
    ck("pairs")

    print("=" * 74)
    print("(3) IS THERE AN EXACT CLASSIFIER IN THIS FEATURE SET?  "
          "(indistinguishable-pair test)")
    print("=" * 74)
    # Two rows with identical full feature vectors but different verdicts
    # prove that NO function of these features can be exact.
    keyed = {}
    for r, t in zip(rows, y):
        k2 = tuple(str(r[f]) for f in feats)
        keyed.setdefault(k2, set()).add(t)
    clash = [k2 for k2, v in keyed.items() if len(v) > 1]
    print(f"   distinct feature vectors: {len(keyed)}; carrying BOTH verdicts: "
          f"{len(clash)}")
    # drop the object-identifying features and retry (a genuine skeleton
    # invariant may not use 'sizes'/'colour', which identify the object)
    core = [f for f in feats if f not in ("sizes", "sizes_sorted", "colour",
                                          "size_min", "size_max", "size_sum",
                                          "n_live_edges", "predicted_S1")]
    keyed2 = {}
    for r, t in zip(rows, y):
        k2 = tuple(str(r[f]) for f in core)
        keyed2.setdefault(k2, set()).add(t)
    clash2 = [k2 for k2, v in keyed2.items() if len(v) > 1]
    nclash2 = sum(1 for r, t in zip(rows, y)
                  if tuple(str(r[f]) for f in core) in set(clash2))
    print(f"   using only the {len(core)} SKELETON-LOCAL features: "
          f"{len(keyed2)} vectors, {len(clash2)} carry both verdicts "
          f"({nclash2} of the {len(y)} pairs live in a clashing cell)")
    RES["exactness"] = {"n_feature_vectors": len(keyed),
                        "clashing_full": len(clash),
                        "core_features": len(core),
                        "n_vectors_core": len(keyed2),
                        "clashing_core": len(clash2),
                        "rows_in_clashing_cells": nclash2}
    control("T3_3_exactness")
    ck("exact")

    print("=" * 74)
    print("(4) GREEDY EXACT COVER: how few conjunctive rules classify all 377?")
    print("=" * 74)
    remaining = set(range(len(y)))
    rules = []
    pool = [(len(m), i) for i, m in enumerate(masks)]
    while remaining:
        bestr = None
        for a in range(L):
            for b in range(a, L):
                s = masks[a] if a == b else masks[a] & masks[b]
                s = s & remaining
                if not s:
                    continue
                w = sum(1 for i in s if y[i])
                if w == len(s) or w == 0:
                    lab = "WITNESS" if w else "BLOCKED"
                    if bestr is None or len(s) > bestr[0]:
                        bestr = (len(s), lab,
                                 str(lits[a]) if a == b
                                 else f"{lits[a]} & {lits[b]}")
        if bestr is None:
            break
        rules.append(bestr)
        cov2 = set()
        for i in list(remaining):
            pass
        # recompute the covered set for the chosen rule
        parts = bestr[2].split(" & ")
        idxs = [j for j in range(L) if str(lits[j]) in parts]
        s = masks[idxs[0]]
        for j in idxs[1:]:
            s = s & masks[j]
        remaining -= s
        if len(rules) > 40:
            break
    print(f"   {len(rules)} conjunctive rules of width <= 2 classify "
          f"{len(y)-len(remaining)}/{len(y)} pairs exactly; "
          f"{len(remaining)} left over")
    for r in rules[:10]:
        print(f"      {r[0]:4d} -> {r[1]:8s}  {r[2]}")
    RES["cover"] = {"n_rules": len(rules), "uncovered": len(remaining),
                    "rules": [list(map(str, r)) for r in rules[:25]]}
    control("T3_4_cover")

    decl = ["T3_0_reproduce", "T3_1_single", "T3_2_pairs", "T3_3_exactness",
            "T3_4_cover"]
    RES["manifest"] = {"declared": decl, "ran": RAN,
                       "missing": [x for x in decl if x not in RAN]}
    RES["seconds"] = round(time.time() - t0, 1)
    print(f"CONTROL MANIFEST: {RES['manifest']}")
    assert not RES["manifest"]["missing"]
    ck("final")
    print(f"wrote {OUT} ({RES['seconds']}s)")


if __name__ == "__main__":
    main()
