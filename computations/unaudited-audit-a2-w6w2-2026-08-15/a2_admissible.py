#!/usr/bin/env python3
"""AUDIT A2 -- template-level ADMISSIBILITY against W6's own budget.

A template only describes which cells are occupied.  W6's budget is about
BLOCK RANKS, so it constrains templates only through the realisability map:

  * a block with cell set S has rank 1 for some choice of values  <=>
    S is a combinatorial rectangle A x B  (rank one = a (x) b, support
    supp(a) x supp(b));  otherwise EVERY source with that template has
    rank(block) >= 2, i.e. the block is in H.
  * hence  |H| >= h_min(T) := #{blocks whose cell set is not a rectangle},
    and the budget  beta >= 3N - m + |H|  forces

        (ADM)   beta(T)  >=  3N - m + h_min(T).

  * Hall refinement, with R taken as large as possible (all rectangle
    blocks, which is the most permissive reading):

        (HALL)  for every S subset V:
                #(non-basis rectangle edges inside S) <= sum_{v in S}(d_R(v)-3)

A template violating (ADM) or (HALL) cannot be the template of an exact
source, so it is worthless as a Sigma_min certificate.
"""

from __future__ import annotations

import json
import sys
from itertools import combinations

from a2_core import geom, normalise_template


def is_rectangle(cells) -> bool:
    if not cells:
        return True
    rows = sorted({a for a, _ in cells})
    cols = sorted({b for _, b in cells})
    return len(cells) == len(rows) * len(cols) and all(
        (a, b) in cells for a in rows for b in cols)


def admissibility(g, template) -> dict:
    t = normalise_template(g, template)
    support = [i for i, s in enumerate(t) if s]
    m = len(support)
    beta = sum(1 for i in support if len(t[i]) == 1)
    h_min = sum(1 for i in support if not is_rectangle(t[i]))
    floor = 3 * g.n - m
    need = floor + h_min
    # Hall with R = rectangle blocks (maximal R)
    rect = [i for i in support if is_rectangle(t[i])]
    basis = {i for i in support if len(t[i]) == 1}
    dR = [0] * g.n
    for i in rect:
        u, v = g.edges[i]
        dR[u] += 1
        dR[v] += 1
    worst = None
    for size in range(1, g.n + 1):
        for S in combinations(range(g.n), size):
            Sset = set(S)
            inside_nonbasis = sum(
                1 for i in rect
                if i not in basis and g.edges[i][0] in Sset
                and g.edges[i][1] in Sset)
            allowance = sum(dR[v] - 3 for v in S)
            slack = allowance - inside_nonbasis
            if worst is None or slack < worst[0]:
                worst = (slack, list(S), inside_nonbasis, allowance)
    return {"m": m, "beta": beta, "h_min_forced_rank2": h_min,
            "budget_floor": max(0, floor), "budget_requires_beta_at_least": need,
            "ADM_ok": beta >= need,
            "HALL_worst_slack": worst[0], "HALL_worst_set": worst[1],
            "HALL_ok": worst[0] >= 0,
            "nonrectangle_blocks": [list(g.edges[i]) for i in support
                                    if not is_rectangle(t[i])],
            "min_dR": min(dR)}


def load_w6():
    base = ("/Users/rishi/workplace/krenn-conjecture/computations/"
            "unaudited-bridge-w6-2026-08-15/results_sigmamin_N8.json")
    return [(r["m"], r["template"]) for r in json.load(open(base))["rows"]
            if r["template"]]


def load_w9():
    base = ("/Users/rishi/workplace/krenn-conjecture/computations/"
            "unaudited-cell-ceiling-w9-2026-08-15/results_b0_sigmamin_honest.json")
    return [(r["m"], r["template"]) for r in json.load(open(base))["rows"]
            if r.get("template")]


def load_w9_balanced():
    base = ("/Users/rishi/workplace/krenn-conjecture/computations/"
            "unaudited-cell-ceiling-w9-2026-08-15/results_b8_sigmamin_balanced.json")
    try:
        blob = json.load(open(base))
    except Exception:
        return []
    rows = blob["rows"] if isinstance(blob, dict) else blob
    out = []
    for r in rows:
        for key in ("template_P", "template", "templateP"):
            if r.get(key):
                out.append((r["m"], r[key]))
                break
    return out


def main():
    g = geom(8)
    report = {}
    for name, loader in (("W6_sigmamin", load_w6), ("W9_beta_free", load_w9),
                         ("W9_caseP", load_w9_balanced)):
        rows = []
        print(f"=== {name} ===")
        for m, tpl in loader():
            t = [[tuple(c) for c in s] for s in tpl]
            a = admissibility(g, t)
            rows.append({"m": m, **a})
            print(f"  m={m:2d} beta={a['beta']:2d} h_min={a['h_min_forced_rank2']:2d} "
                  f"needs beta>={a['budget_requires_beta_at_least']:3d} "
                  f"ADM={'ok' if a['ADM_ok'] else 'VIOLATED'}  "
                  f"HALL slack={a['HALL_worst_slack']:3d} "
                  f"{'ok' if a['HALL_ok'] else 'VIOLATED'}")
        report[name] = rows
    with open("results_admissibility.json", "w") as h:
        json.dump(report, h, indent=1, default=str)
    print("wrote results_admissibility.json")


if __name__ == "__main__":
    sys.exit(main())
