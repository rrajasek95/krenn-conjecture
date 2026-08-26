#!/usr/bin/env python3
"""W9 Task B6 -- POSITIVE CONTROL for the B4/B5 diagnostics.

The B5 yardstick ("an exact source with template T needs Jacobian rank
<= Sigma - r(T) + 3 at a smooth point") is only trustworthy if it PASSES on
templates that provably do carry an exact object.  Two controls:

 C-a  d = 2 (bicoloured) GHZ at N = 4 and N = 6, if it exists: search
      exhaustively over small integer sources for H = e_0^(x)N + e_1^(x)N.
 C-b  the trivially exact "one-colour" source: H = e_c^(x)N, realised by a
      single perfect matching with the cell (c,c).  This certainly exists,
      so the diagnostic MUST pass on it.
 C-c  STAGE_A (exists) -- already passes in B5.

Exact arithmetic throughout.
"""
from __future__ import annotations
import itertools, json, random, sys
from fractions import Fraction as F
from itertools import combinations, product
import w9_template as wt
from run_b4_dimension_count import gauge_rank, supported_mixed
from run_b5_jacobian_rank import jacobian_rank

COLORS = (0, 1, 2)


def haf(src, sites, word, matchings):
    tot = F(0)
    for M in matchings:
        t = F(1)
        for u, v in M:
            t *= src[(u, v)][word[u]][word[v]]
            if t == 0:
                break
        tot += t
    return tot


def search_d2(N, trials=400000, seed=3):
    """Random integer search for a d=2 exact source at N sites (colours 0,1
    only; colour 2 identically zero)."""
    rng = random.Random(seed)
    edges = tuple(combinations(range(N), 2))
    Ms = wt.perfect_matchings(tuple(range(N)))
    words = list(product((0, 1), repeat=N))
    for _ in range(trials):
        src = {}
        for e in edges:
            blk = [[F(0)] * 3 for _ in range(3)]
            for a in (0, 1):
                for b in (0, 1):
                    if rng.random() < 0.5:
                        blk[a][b] = F(rng.randint(-2, 2))
            src[e] = blk
        ok = True
        for w in words:
            want = 1 if len(set(w)) == 1 else 0
            if haf(src, range(N), w, Ms) != want:
                ok = False
                break
        if ok:
            return src
    return None


print("=" * 88)
print("B6  POSITIVE CONTROLS for the B4/B5 overdetermination diagnostics")
print("=" * 88)
OUT = {}

# --- C-b: the one-colour source (H = e_2^(x)8): definitely exists ---------
N = 8
edges = tuple(combinations(range(N), 2))
M0 = ((0, 1), (2, 3), (4, 5), (6, 7))
src = {e: [[F(0)] * 3 for _ in range(3)] for e in edges}
for e in M0:
    src[e][2][2] = F(1)
T = wt.template_of(src, N)
Sigma = sum(len(s) for s in T.values())
r = gauge_rank(T)
vals = {(e, (2, 2)): F(1) for e in M0}
J, n, used = jacobian_rank(T, vals)
E, E2, sing, pures = supported_mixed(T)
print(f"\nC-b  one-colour source (H = e_2^(x)8, single matching):")
print(f"     Sigma = {Sigma}, E = {E}, r = {r}, J = {J}, "
      f"budget = Sigma-r+3 = {Sigma-r+3}")
print(f"     (DC) Sigma >= E + r ?  {Sigma} >= {E}+{r}={E+r}  -> "
      f"{'PASS' if Sigma >= E+r else 'FAIL'}")
print(f"     (B5) J <= budget ?     {J} <= {Sigma-r+3}  -> "
      f"{'PASS' if J <= Sigma-r+3 else 'FAIL'}")
OUT["C_b_one_colour"] = {"Sigma": Sigma, "E": E, "r": r, "J": J,
                         "budget": Sigma - r + 3,
                         "DC_pass": Sigma >= E + r, "B5_pass": J <= Sigma - r + 3}

# --- C-a: d=2 GHZ ---------------------------------------------------------
for NN in (4, 6):
    print(f"\nC-a  exhaustive-ish random search for a d=2 exact source at N={NN} ...",
          flush=True)
    s = search_d2(NN, trials=200000 if NN == 4 else 300000)
    if s is None:
        print(f"     none found (search only; NOT a non-existence proof)")
        OUT[f"C_a_d2_N{NN}"] = None
        continue
    T = wt.template_of(s, NN)
    Sigma = sum(len(x) for x in T.values())
    print(f"     FOUND a d=2 exact source at N={NN}: Sigma = {Sigma}")
    OUT[f"C_a_d2_N{NN}"] = {"Sigma": Sigma,
                            "source": {f"{u},{v}": [[str(x) for x in row]
                                                    for row in s[(u, v)]]
                                       for (u, v) in s}}

with open("results_b6_positive_control.json", "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
print("\nwrote results_b6_positive_control.json")
