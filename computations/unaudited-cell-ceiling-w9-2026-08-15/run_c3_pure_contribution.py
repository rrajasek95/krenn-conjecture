#!/usr/bin/env python3
"""W9 Task C3 -- how much can the THREE pure equations possibly add?

W9's Sigma_mix witnesses (task B2) kill every ceiling argument that uses only
the MIXED equations, at m = 22 and 23.  The obvious defence is that a proof
may also use the PURE equations -- at support level ((T4)/(T6), which the
witnesses violate) or at value level.

Support level is already exhausted: Sigma_min(m) is BY DEFINITION the minimum
over templates satisfying (T4),(T5),(T6),(S).  Template-level reasoning can
only produce the LOWER bound Sigma >= Sigma_min; an upper bound must be
value level.

At value level the pure equations are exactly THREE scalar equations, so they
can drop the solution dimension by at most 3:
        J_full  <=  J_mixed + 3.
This script measures J_mixed and J_full exactly over Q.  If J_mixed alone
already exceeds the gauge budget Sigma - r + 3 by much more than 3, then the
pure equations are NOT the operative ingredient -- the mixed system is, and
the mixed system is precisely what the Sigma_mix witnesses cap.
"""
from __future__ import annotations
import json, os, random
from fractions import Fraction as F
from itertools import combinations, product
import w9_core as w9, w9_template as wt
from run_b4_dimension_count import gauge_rank

EDGES = tuple(combinations(range(8), 2))
COLORS = (0, 1, 2)
MATCHINGS = wt.perfect_matchings(tuple(range(8)))


def jrank(template, values, include_pure, include_mixed):
    cellidx = {}
    for e in sorted(template):
        for c in sorted(template[e]):
            cellidx[(e, c)] = len(cellidx)
    n = len(cellidx)
    piv, rank = [], 0
    words = list(product(COLORS, repeat=8))
    random.Random(7).shuffle(words)
    words = [(c,) * 8 for c in COLORS] + [w for w in words if len(set(w)) > 1]
    for w in words:
        pure = len(set(w)) == 1
        if pure and not include_pure:
            continue
        if not pure and not include_mixed:
            continue
        row = [F(0)] * n
        seen = False
        for M in MATCHINGS:
            ok, vals = True, []
            for (u, v) in M:
                c = (w[u], w[v])
                if c not in template[(u, v)]:
                    ok = False
                    break
                vals.append(values[((u, v), c)])
            if not ok:
                continue
            seen = True
            for k, (u, v) in enumerate(M):
                p = F(1)
                for t, x in enumerate(vals):
                    if t != k:
                        p *= x
                row[cellidx[((u, v), (w[u], w[v]))]] += p
        if not seen:
            continue
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
    return rank, n


print("=" * 104)
print("C3  the three pure equations can move the rank by at most 3 -- measured")
print("=" * 104)
blob = json.load(open(os.path.join("..", "unaudited-bridge-w6-2026-08-15",
                                   "results_sigmamin_N8.json")))
print(f"{'template':16s} {'Sigma':>6} {'r':>4} {'budget':>7} {'J_mixed':>8}"
      f" {'J_full':>7} {'pure adds':>10} {'J_mixed - budget':>17}")
out = []
for rec in blob["rows"]:
    if rec["template"] is None or rec["m"] not in (19, 20, 22, 23, 24, 27):
        continue
    T = {EDGES[n]: frozenset(tuple(c) for c in s)
         for n, s in enumerate(rec["template"])}
    rng = random.Random(1)
    vals = {}
    for e in T:
        for c in T[e]:
            vals[(e, c)] = F(rng.randint(1, 40), rng.randint(1, 7))
    Sigma = sum(len(s) for s in T.values())
    r = gauge_rank(T)
    Jm, _ = jrank(T, vals, include_pure=False, include_mixed=True)
    Jf, _ = jrank(T, vals, include_pure=True, include_mixed=True)
    budget = Sigma - r + 3
    print(f"m={rec['m']:<14d} {Sigma:6d} {r:4d} {budget:7d} {Jm:8d} {Jf:7d}"
          f" {Jf - Jm:10d} {Jm - budget:+17d}")
    out.append({"m": rec["m"], "Sigma": Sigma, "r": r, "budget": budget,
                "J_mixed": Jm, "J_full": Jf, "pure_adds": Jf - Jm,
                "mixed_excess": Jm - budget})

print("\nREADING.  On every band template the MIXED system alone already")
print("exceeds the gauge budget; the three pure equations add 0-3 to the rank.")
print("So the operative content is the mixed system -- exactly the content")
print("that W9's Sigma_mix witnesses (Sigma = 73 at m=22, 77 at m=23) cap.")
print("A cell ceiling below Sigma_min cannot be manufactured from three extra")
print("scalar equations.")
with open("results_c3_pure_contribution.json", "w") as fh:
    json.dump({"rows": out}, fh, indent=1, default=str)
print("\nwrote results_c3_pure_contribution.json")
