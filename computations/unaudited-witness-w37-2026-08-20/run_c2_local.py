"""W37 / C2 -- THE LOCAL X_3 GEOMETRY AT F8, AND WHICH X_4 ROWS RESIST.

Replaces C1's global walk (too slow at N=8) with the exact linear object
that answers the same questions much more sharply.

At a fixed site z, H_w is LINEAR in the 63 unknowns
{A_{z,y}[i][j] : y != z} because every perfect matching uses exactly one
edge at z:
    H_w(A) = sum_{y != z} A_{z,y}[w_z][w_y] * haf_{V-{z,y}}(w).
So, holding every block not incident to z fixed at F8's values:

  (C2a) the affine solution space S_z of the X_3 system at z -- its
        dimension MEASURES F8's local component (W25's stated soft spot:
        "F8 is one object, component/dimension unmeasured");
  (C2b) sample S_z, decide all 21 pairs at each sample: is ALL-BLOCKED an
        isolated accident or a property of the whole component?
  (C2c) for every off-count-4 word u, is the system  X_3-at-z + (H_u = 0)
        still consistent?  A word that is inconsistent at EVERY site is
        LOCALLY UNREMOVABLE -- the exact sense in which an X_4 equation
        'resists' at F8.  This is the witness-restoration mechanism the
        brief asks to characterise, computed exactly by rank.
  (C2d) the aligned-split stratum: build an N=8 source with the
        (S1)(S2)(S3)(S4) geometry and drive it into X_3 -- every such
        point has a witness by THEOREM W37-PER, so the stratum is a
        witness-guaranteed region of X_3 at N=8.
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
from run_c1_builder import (rref, solve_affine, site_rows, apply_site,
                            words_upto)

OUT = os.path.join(HERE, "results_c2_local.json")
RES = {"lane": "W37", "task": "C2 local X_3 geometry at F8", "unaudited": True}
RAN = []
DECLARED = ["control_rank", "dimensions", "component_allblocked",
            "resisting_rows", "aligned_split"]
N = 8


def load_f8():
    return C.parse_source(json.load(open(os.path.join(
        HERE, "..", "unaudited-x3core-w25-2026-08-15",
        "OBJECT_W25-F8_n8_allblocked_X3.json")))["blocks"], 8)


def rank_of(rows, ncols):
    red, piv = rref([r[:] for r in rows], ncols)
    return len(piv)


def consistent(rows, rhs, ncols):
    aug = [r + [b] for r, b in zip(rows, rhs)]
    red, piv = rref(aug, ncols)
    return not any(all(row[c] == 0 for c in range(ncols)) and row[ncols] != 0
                   for row in red)


def main():
    t0 = time.time()
    src = load_f8()
    W3 = words_upto(3)
    print(f"  X_3 system: {len(W3)} words, 63 unknowns per site", flush=True)

    # ---- control: F8 must itself solve every site system (ledger 27/28)
    print("\n=== C2.0 CONTROL: F8 solves its own site systems ===", flush=True)
    ctrl = {}
    for z in range(N):
        rows, rhs, idx, nc = site_rows(src, z, W3)
        x = [Fraction(0)] * nc
        for (y, i, j), col in idx.items():
            x[col] = C.block(src, z, y)[i][j]
        ok = all(sum(r[c] * x[c] for c in range(nc)) == b
                 for r, b in zip(rows, rhs))
        ctrl[z] = ok
        assert ok, f"F8 fails its own site-{z} system"
    print("   8/8 sites: F8 is an exact solution of each site system")
    RES["control_rank"] = ctrl; RAN.append("control_rank"); C.ckpt(OUT, RES)

    # ---- (a) dimensions
    print("\n=== C2.1 dimension of the X_3 solution space at each site ===",
          flush=True)
    dims = {}
    sysmem = {}
    for z in range(N):
        rows, rhs, idx, nc = site_rows(src, z, W3)
        r = rank_of(rows, nc)
        dims[z] = {"rank": r, "dim": nc - r, "ncols": nc}
        sysmem[z] = (rows, rhs, idx, nc)
        print(f"   site {z}: rank {r}, solution dim {nc - r}", flush=True)
    RES["dimensions"] = dims; RAN.append("dimensions"); C.ckpt(OUT, RES)

    # ---- (b) sample the component and decide
    print("\n=== C2.2 all-blocked across the local component ===", flush=True)
    rng = random.Random(37)
    rows_out = []
    for z in range(N):
        if dims[z]["dim"] == 0:
            continue
        rws, rhs, idx, nc = sysmem[z]
        for t in range(3):
            x = solve_affine(rws, rhs, nc, rng, spread=2)
            if x is None:
                continue
            s2 = apply_site(src, z, x, idx)
            if not C.in_Xk(s2, 8, 3):
                rows_out.append({"site": z, "trial": t, "error": "not X_3"})
                continue
            live = [(p, q) for p, q in combinations(range(8), 2)
                    if C.is_live(s2, p, q)]
            nw = 0
            for (p, q) in live:
                U = tuple(a for a in range(8) if a not in (p, q))
                if D.decide_pair(s2, p, q, U, chars=(0,), timeout=180,
                                 do_search=False)["verdict"] == "WITNESS":
                    nw += 1
            _, bad = C.defects(s2, 8)
            rows_out.append({"site": z, "trial": t, "n_live": len(live),
                             "n_witness": nw, "n_defects": len(bad),
                             "offcounts": {str(k): v for k, v in
                                           Counter(C.offcount(w)
                                                   for w in bad).items()}})
            print(f"   site {z} sample {t}: live {len(live)}, witnesses {nw},"
                  f" defects {len(bad)}", flush=True)
            RES["component_allblocked"] = rows_out
            C.ckpt(OUT, RES)
    RAN.append("component_allblocked")

    # ---- (c) which off-4 rows resist
    print("\n=== C2.3 which off-count-4 words can be zeroed at some site? ===",
          flush=True)
    off4 = [w for w in C.all_words(8) if C.offcount(w) == 4]
    _, bad = C.defects(src, 8)
    cur_bad4 = set(w for w in bad if C.offcount(w) == 4)
    removable = Counter()
    stuck = Counter()
    detail = {"removable_words": [], "stuck_words": []}
    for u in off4:
        ok_any = False
        for z in range(N):
            rws, rhs, idx, nc = sysmem[z]
            row = [Fraction(0)] * nc
            others = [y for y in range(N) if y != z]
            for y in others:
                rest = tuple(t for t in range(N) if t not in (z, y))
                hv = C.haf_word(src, u, rest)
                if hv != 0:
                    row[idx[(y, u[z], u[y])]] += hv
            if consistent(rws + [row], rhs + [Fraction(0)], nc):
                ok_any = True
                break
        key = C.profile(u)
        if ok_any:
            removable[key] += 1
            if u in cur_bad4:
                detail["removable_words"].append(list(u))
        else:
            stuck[key] += 1
            detail["stuck_words"].append(list(u))
    print(f"   removable at some site: {sum(removable.values())} of "
          f"{len(off4)}   {dict(removable)}")
    print(f"   STUCK at every site:    {sum(stuck.values())}   {dict(stuck)}")
    RES["resisting_rows"] = {
        "removable": {str(k): v for k, v in removable.items()},
        "stuck": {str(k): v for k, v in stuck.items()},
        "n_off4": len(off4),
        "n_currently_violated": len(cur_bad4),
        "n_violated_and_removable": len(detail["removable_words"]),
        "stuck_sample": detail["stuck_words"][:40]}
    RAN.append("resisting_rows"); C.ckpt(OUT, RES)

    RES["seconds"] = round(time.time() - t0, 1)
    RES["manifest"] = {"declared": DECLARED, "ran": RAN,
                       "missing": [x for x in DECLARED if x not in RAN]}
    C.ckpt(OUT, RES)
    print("\nMANIFEST", RES["manifest"])


if __name__ == "__main__":
    main()
