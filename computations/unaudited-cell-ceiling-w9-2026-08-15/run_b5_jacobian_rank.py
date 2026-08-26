#!/usr/bin/env python3
"""W9 Task B5 -- is the exactness system on an admissible template actually
INDEPENDENT?  Exact Jacobian rank over Q.

RIGOROUS FACT (used as the yardstick).  Let G = (C^*)^24 act on sources by
A_uv -> D_u A_uv D_v^T.  Gauge multiplies H(c^N) by prod_u d_{u,c} and maps
zeros to zeros, so the subgroup G_1 = {g : prod_u g_{u,c} = 1, c=0,1,2}
(dimension 21) preserves EXACTNESS.  The stabiliser of a source with
template T has dimension 24 - r(T), r(T) = rank of the cell/slot incidence
matrix.  Hence

   (*) if an exact source with template T exists, the exact locus inside
       (C^*)^{Sigma(T)} has a component through it of dimension >= r(T) - 3,
       so at a smooth point of that component the Jacobian of the exactness
       system has rank <= Sigma(T) - r(T) + 3.

So: measuring the generic Jacobian rank J(T) tells us how far the system is
from that budget.  J(T) = Sigma(T) (full column rank at a random point)
means the E+3 equations are locally independent in every direction -- the
system is NOT degenerate, and the dimension count of task B4 is meaningful
rather than an artefact of syzygies.

This is a measurement at a RANDOM point, so it bounds the rank on the exact
locus only from above in the generic direction; it is EVIDENCE, not a proof.
Exact arithmetic over Q throughout.
"""
from __future__ import annotations
import json, os, random, sys
from fractions import Fraction as F
from itertools import combinations, product
import w9_template as wt
import w9_core as w9
from run_b4_dimension_count import gauge_rank

EDGES = tuple(combinations(range(8), 2))
COLORS = (0, 1, 2)
MATCHINGS = wt.perfect_matchings(tuple(range(8)))


def jacobian_rank(template, values, cap=None, verbose=False):
    """Exact rank over Q of d(H_w)/d(cell) for all words w with fibre>=1
    (mixed) plus the 3 pure words.  Incremental elimination, early exit at
    full column rank."""
    cellidx = {}
    for e in sorted(template):
        for c in sorted(template[e]):
            cellidx[(e, c)] = len(cellidx)
    n = len(cellidx)
    piv = []        # list of (row, pivot col)
    rank = 0
    words = list(product(COLORS, repeat=8))
    random.Random(7).shuffle(words)
    # put the pure words first
    words = [(c,) * 8 for c in COLORS] + [w for w in words if len(set(w)) > 1]
    used = 0
    for w in words:
        row = [F(0)] * n
        any_term = False
        for M in MATCHINGS:
            ok = True
            vals = []
            for (u, v) in M:
                c = (w[u], w[v])
                if c not in template[(u, v)]:
                    ok = False
                    break
                vals.append(values[((u, v), c)])
            if not ok:
                continue
            any_term = True
            for k, (u, v) in enumerate(M):
                prod = F(1)
                for t, x in enumerate(vals):
                    if t != k:
                        prod *= x
                row[cellidx[((u, v), (w[u], w[v]))]] += prod
        if not any_term:
            continue
        used += 1
        # reduce
        r = row
        for pr, pc in piv:
            if r[pc]:
                f = r[pc] / pr[pc]
                r = [a - f * b for a, b in zip(r, pr)]
        nz = next((c for c in range(n) if r[c] != 0), None)
        if nz is not None:
            piv.append((r, nz))
            rank += 1
            if rank == n:
                break
        if cap and used > cap:
            break
    return rank, n, used


def analyse(label, template, seed=1):
    rng = random.Random(seed)
    values = {}
    for e in template:
        for c in template[e]:
            values[(e, c)] = F(rng.randint(1, 40), rng.randint(1, 7))
    Sigma = sum(len(s) for s in template.values())
    r = gauge_rank(template)
    J, n, used = jacobian_rank(template, values)
    budget = Sigma - r + 3
    return {"label": label, "Sigma": Sigma, "gauge_rank": r,
            "jacobian_rank": J, "vars": n, "equations_used": used,
            "rank_budget_if_exact_exists": budget,
            "exceeds_budget": J > budget}


if __name__ == "__main__":
    import importlib
    mod = importlib.import_module("verify_n8_d2_kill_and_monochrome_rigidity")

    def build(params):
        blocks = mod.build_stage_a(params)
        return {(u, v): [[F(x) for x in row] for row in mod.C.oriented(blocks, u, v)]
                for u, v in combinations(range(8), 2)}
    BEST = ((F(-7), F(-9)), (F(7), F(8)), F(5,3), F(-7,4), F(-1,5), F(-8,5),
            (F(-7,4), F(-4), F(7,5)), (F(-3,2), F(-5,4), F(-9)),
            (F(1,5), F(8,3), F(-1,5)), (F(-9,2), F(1), F(3,4)), F(6), F(-9))

    print("=" * 96)
    print("B5  exact Jacobian rank of the exactness system (over Q, random point)")
    print("=" * 96)
    print(f"{'template':26s} {'Sigma':>6} {'r':>4} {'J(rank)':>8} {'budget=S-r+3':>13}"
          f" {'J>budget?':>10}")
    out = []

    # calibration: the object that EXISTS
    tplA = wt.template_of(build(BEST))
    rec = analyse("STAGE_A_GENERIC", tplA)
    out.append(rec)
    print(f"{rec['label']:26s} {rec['Sigma']:6d} {rec['gauge_rank']:4d}"
          f" {rec['jacobian_rank']:8d} {rec['rank_budget_if_exact_exists']:13d}"
          f" {str(rec['exceeds_budget']):>10}")

    # W6 Sigma_min certificates
    blob = json.load(open(os.path.join("..", "unaudited-bridge-w6-2026-08-15",
                                       "results_sigmamin_N8.json")))
    for rec0 in blob["rows"]:
        if rec0["template"] is None or rec0["m"] not in (19, 20, 22, 23, 24, 27):
            continue
        T = {EDGES[n]: frozenset(tuple(c) for c in s)
             for n, s in enumerate(rec0["template"])}
        rec = analyse(f"sigmamin_m{rec0['m']}", T)
        out.append(rec)
        print(f"{rec['label']:26s} {rec['Sigma']:6d} {rec['gauge_rank']:4d}"
              f" {rec['jacobian_rank']:8d} {rec['rank_budget_if_exact_exists']:13d}"
              f" {str(rec['exceeds_budget']):>10}", flush=True)

    print("\nReading: J = Sigma means the exactness equations are locally")
    print("INDEPENDENT in every cell direction at a random point of the template.")
    print("An exact source with that template needs a >= (r-3)-dimensional")
    print("component, i.e. rank <= Sigma - r + 3 at its smooth points.")
    with open("results_b5_jacobian_rank.json", "w") as fh:
        json.dump({"rows": out}, fh, indent=1, default=str)
    print("\nwrote results_b5_jacobian_rank.json")
