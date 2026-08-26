#!/usr/bin/env python3
"""AUDIT A2 -- the SHARP template-level form of the committed slice-cover
input, and its effect on every saved certificate.

The forced incident-edge theorem (notes/slice-cover.md (6)) says: for every
vertex p and colour r there is an active neighbour j with

        A_pj = a (x) e_r^{(j)},   a != 0.

At TEMPLATE level that says exactly:

  (SC)  for every (p, r) some incident edge e = {p,j} has ALL of its cells
        carrying colour r at the FAR endpoint j (equivalently: the cell set of
        e lies in the single column r when read from p).

This is strictly stronger than the two conditions the probes impose:

  * W6/W9's (T6) "every (vertex,colour) slot carries a cell" is the NEAR-side
    condition and follows from the pure words; it is much weaker.
  * W6's counting budget beta >= 3N - m + |H| is a CONSEQUENCE of (SC) --
    valid, but not sharp: it charges every rank-one block with one slot,
    whereas a rank-one block whose far factor is not a coordinate vector
    (e.g. any block with >= 2 cells in >= 2 columns AND >= 2 rows, in
    particular every full 9-cell block) serves NO slot at all.

Sharp count implied by (SC):   3N <= 2*beta + #(edges whose cells lie in a
single row or a single column but which are not a single cell).
"""

from __future__ import annotations

import json
from itertools import combinations

from a2_core import geom, normalise_template

N = 8


def serves(cells, side):
    """Colour served at the OPPOSITE endpoint, or None.

    side = 0 means: the slot sits at the first endpoint u of the edge (u<v),
    so the far endpoint is v and we need every cell to share its v-colour.
    """
    if not cells:
        return None
    idx = 1 - side
    vals = {c[idx] for c in cells}
    return next(iter(vals)) if len(vals) == 1 else None


def slice_cover_report(g, template) -> dict:
    t = normalise_template(g, template)
    served = {(v, c): [] for v in range(g.n) for c in range(3)}
    for i, cells in enumerate(t):
        if not cells:
            continue
        u, v = g.edges[i]
        c0 = serves(cells, 0)          # slot at u, far endpoint v
        if c0 is not None:
            served[(u, c0)].append(i)
        c1 = serves(cells, 1)          # slot at v, far endpoint u
        if c1 is not None:
            served[(v, c1)].append(i)
    missing = [[v, c] for (v, c), lst in served.items() if not lst]
    beta = sum(1 for cells in t if len(cells) == 1)
    one_sided = sum(1 for cells in t
                    if len(cells) >= 2 and (serves(cells, 0) is not None
                                            or serves(cells, 1) is not None))
    return {"SC_ok": not missing, "missing_slots": missing,
            "n_missing": len(missing), "beta": beta,
            "one_sided_multicell": one_sided,
            "sharp_count_lhs": 3 * g.n,
            "sharp_count_rhs": 2 * beta + one_sided,
            "sharp_count_ok": 3 * g.n <= 2 * beta + one_sided}


def load(path, key="template", mkey="m"):
    blob = json.load(open(path))
    rows = blob["rows"] if isinstance(blob, dict) else blob
    return [(r[mkey], r[key]) for r in rows if r.get(key)]


def main():
    g = geom(N)
    C = "/Users/rishi/workplace/krenn-conjecture/computations"
    sources = {
        "W6_sigmamin": load(f"{C}/unaudited-bridge-w6-2026-08-15/"
                            "results_sigmamin_N8.json"),
        "W9_beta_free": load(f"{C}/unaudited-cell-ceiling-w9-2026-08-15/"
                             "results_b0_sigmamin_honest.json"),
        "W9_caseP": load(f"{C}/unaudited-cell-ceiling-w9-2026-08-15/"
                         "results_b8_sigmamin_balanced.json"),
        "A2_own_witnesses": load("results_hunt_restricted_low.json"),
    }
    out = {}
    for name, rows in sources.items():
        recs = []
        print(f"=== {name} ===")
        for m, tpl in rows:
            r = slice_cover_report(g, [[tuple(c) for c in s] for s in tpl])
            recs.append({"m": m, **r})
            print(f"  m={m:2d}: (SC) {'ok' if r['SC_ok'] else 'VIOLATED'} "
                  f"({r['n_missing']} of 24 slots unservable), "
                  f"sharp count 24 <= 2*{r['beta']}+{r['one_sided_multicell']}"
                  f"={r['sharp_count_rhs']} "
                  f"{'ok' if r['sharp_count_ok'] else 'FAILS'}")
        out[name] = recs

    # W2's 28 full-support R_cell templates
    blob = json.load(open(f"{C}/unaudited-witness-splitting-w2-2026-08-15/"
                          "hunt8_models.json"))
    recs = []
    print("=== W2_28_full_support ===")
    for res in blob["results"].values():
        for mod in res["models"]:
            tpl = [[] if x is None else [tuple(x)] for x in mod["labels"]]
            r = slice_cover_report(g, tpl)
            recs.append({"m": mod["support"], **r})
    okc = sum(1 for r in recs if r["SC_ok"])
    print(f"  {okc} of {len(recs)} satisfy (SC)")
    out["W2_28_full_support"] = recs

    with open("results_slicecover.json", "w") as h:
        json.dump(out, h, indent=1, default=str)
    print("wrote results_slicecover.json")


if __name__ == "__main__":
    main()
