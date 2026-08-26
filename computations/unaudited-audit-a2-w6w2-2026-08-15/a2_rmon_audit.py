#!/usr/bin/env python3
"""AUDIT A2 / claim B.7 -- R_mon: definition coherence + independent
re-verification of the depth-1 / depth-2 upgrade census (W2: 174,048
templates, all singleton-killed).

Definition audit (combinatorial facts checked here, not asserted):
  D1  R_mon = every block's cell set is the graph of a PARTIAL INJECTION
      (at most one cell per row and per column).  R_cell (<= 1 cell) is the
      subfamily with all blocks of size <= 1.
  D2  R_mon and R_cell are closed under the monomial gauge group
      (per-site diagonal scalings and per-site colour permutations) -- checked
      by exhaustive orbit computation on all 512 cell supports.
  D3  a partial-injection block with k >= 2 cells has rank k >= 2 and is never
      a combinatorial rectangle; hence inside R_mon W6's budget
      beta >= 3N - m + |H| reads beta >= 3N/2 (12 at N = 8), i.e. at least
      half the blocks must be SINGLE cells -- checked here.

Upgrade census: rebuilt from W2's 28 base models (the objects themselves were
re-verified independently in a2_w2_audit.py); every upgraded template is
re-counted with the a2_core subset-DP counter.
"""

from __future__ import annotations

import json
import random
import sys
from itertools import combinations, product

from a2_core import audit_template, fibre_counts_dp_numpy, geom, normalise_template

W2 = ("/Users/rishi/workplace/krenn-conjecture/computations/"
      "unaudited-witness-splitting-w2-2026-08-15")
N = 8
EDGES = tuple(combinations(range(N), 2))
CELLS = [(a, b) for a in range(3) for b in range(3)]


def is_partial_injection(cells):
    rows = [a for a, _ in cells]
    cols = [b for _, b in cells]
    return len(set(rows)) == len(rows) and len(set(cols)) == len(cols)


def is_rectangle(cells):
    if not cells:
        return True
    rows = sorted({a for a, _ in cells})
    cols = sorted({b for _, b in cells})
    return len(cells) == len(rows) * len(cols) and all(
        (a, b) in cells for a in rows for b in cols)


def d2_check():
    """D2: closure of the two families under per-site colour permutation and
    (trivially) diagonal scaling, on all 512 supports."""
    import itertools
    bad_mon = bad_cell = 0
    perms = list(itertools.permutations(range(3)))
    for mask in range(512):
        cells = frozenset(CELLS[i] for i in range(9) if mask >> i & 1)
        for pu in perms:
            for pv in perms:
                img = frozenset((pu[a], pv[b]) for a, b in cells)
                if is_partial_injection(cells) != is_partial_injection(img):
                    bad_mon += 1
                if (len(cells) <= 1) != (len(img) <= 1):
                    bad_cell += 1
    return {"supports_tested": 512, "R_mon_closure_violations": bad_mon,
            "R_cell_closure_violations": bad_cell}


def d3_check():
    """D3: partial injections with >= 2 cells are never rectangles (so they
    are forced rank >= 2), hence |H| = m - beta inside R_mon."""
    bad = 0
    for mask in range(512):
        cells = frozenset(CELLS[i] for i in range(9) if mask >> i & 1)
        if is_partial_injection(cells) and len(cells) >= 2 and is_rectangle(cells):
            bad += 1
    return {"partial_injections_with_ge2_cells_that_are_rectangles": bad,
            "consequence": "inside R_mon, |H| = m - beta, so the budget "
                           "beta >= 3N - m + |H| becomes beta >= 3N/2"}


def upgrade_options(cells):
    """Extra cells keeping the block a partial injection."""
    rows = {a for a, _ in cells}
    cols = {b for _, b in cells}
    return [(a, b) for a in range(3) for b in range(3)
            if a not in rows and b not in cols]


def main():
    args = sys.argv[1:]
    depth2_cap = int(args[args.index("--depth2") + 1]) if "--depth2" in args else 0
    g = geom(N)
    out = {"D2": d2_check(), "D3": d3_check()}
    print("D2 (gauge closure over all 512 supports):", out["D2"])
    print("D3:", out["D3"])

    blob = json.load(open(f"{W2}/hunt8_models.json"))
    bases = [m["labels"] for r in blob["results"].values() for m in r["models"]]
    print(f"base templates: {len(bases)}")

    def as_template(cellsets):
        return normalise_template(g, [frozenset(s) for s in cellsets])

    # depth 1 -- exhaustive
    n1 = killed1 = 0
    minsing1 = None
    for labels in bases:
        base = [frozenset() if x is None else frozenset({tuple(x)})
                for x in labels]
        for i in range(len(EDGES)):
            for extra in upgrade_options(base[i]):
                cellsets = list(base)
                cellsets[i] = base[i] | {extra}
                counts = fibre_counts_dp_numpy(g, as_template(cellsets))
                singles = int(((counts == 1) & g.mixed).sum())
                n1 += 1
                if singles:
                    killed1 += 1
                minsing1 = singles if minsing1 is None else min(minsing1, singles)
    print(f"depth 1: {n1} templates (W2: 3136), singleton-killed {killed1}, "
          f"minimum singleton count {minsing1}")
    out["depth1"] = {"templates": n1, "killed": killed1,
                     "min_singletons": minsing1}

    # depth 2 -- exhaustive if asked, else a random sample
    rng = random.Random(31337)
    pairs = []
    for bi, labels in enumerate(bases):
        base = [frozenset() if x is None else frozenset({tuple(x)})
                for x in labels]
        opts = [(i, e) for i in range(len(EDGES))
                for e in upgrade_options(base[i])]
        for (i, e1), (j, e2) in combinations(opts, 2):
            if i == j and not is_partial_injection(base[i] | {e1, e2}):
                continue
            pairs.append((bi, i, e1, j, e2))
    print(f"depth 2: {len(pairs)} templates enumerated (W2: 170912)")
    sample = pairs if depth2_cap in (0, len(pairs)) else rng.sample(
        pairs, min(depth2_cap, len(pairs)))
    n2 = killed2 = 0
    minsing2 = None
    for bi, i, e1, j, e2 in sample:
        base = [frozenset() if x is None else frozenset({tuple(x)})
                for x in bases[bi]]
        cellsets = list(base)
        cellsets[i] = cellsets[i] | {e1}
        cellsets[j] = cellsets[j] | {e2}
        counts = fibre_counts_dp_numpy(g, as_template(cellsets))
        singles = int(((counts == 1) & g.mixed).sum())
        n2 += 1
        if singles:
            killed2 += 1
        minsing2 = singles if minsing2 is None else min(minsing2, singles)
    print(f"depth 2 checked: {n2}, singleton-killed {killed2}, "
          f"minimum singleton count {minsing2}")
    out["depth2"] = {"enumerated": len(pairs), "checked": n2,
                     "killed": killed2, "min_singletons": minsing2}
    out["total_enumerated"] = n1 + len(pairs)
    print(f"total enumerated: {out['total_enumerated']} (W2: 174048)")
    with open("results_rmon_audit.json", "w") as h:
        json.dump(out, h, indent=1, default=str)
    print("wrote results_rmon_audit.json")


if __name__ == "__main__":
    main()
