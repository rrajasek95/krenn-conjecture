#!/usr/bin/env python3
"""AUDIT A4 / CHECK 08 -- W10's two riders on Lemma W10-G:
  (i)  COROLLARY W10-6: every mixed-exact six-site source has a vanishing pure
       (given the committed six-site theorem);
  (ii) (SC) is gauge-invariant at TEMPLATE level.
Plus an independent re-verification of W10's N=6 mixed-exact witnesses.
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction as F
from itertools import combinations, product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(HERE))
W10 = os.path.join(ROOT, "computations",
                   "unaudited-mixed-exact-pure-cancellation-w10-2026-08-15")
import a4_engine as E                     # noqa: E402
from chk07_w10G_gauge import (GQ, H, apply_gauge, edges_of, pures,   # noqa: E402
                              rand_source, template_of)

COLORS = (0, 1, 2)
out = {}


# ---------------------------------------------------- (SC)/(FIE), my version
def sc_slots(source, n):
    """{(p,r): [serving neighbours]}.

    (SC)/(FIE): for every site p and colour r some neighbour j has A_pj
    NONZERO with support inside the single far-end colour r, i.e. every
    occupied cell of the block, read from p, has far-end colour r.
    """
    res = {}
    for p in range(n):
        for r in COLORS:
            servers = []
            for j in range(n):
                if j == p:
                    continue
                u, v = min(p, j), max(p, j)
                blk = source[(u, v)]
                far = set()
                nonzero = False
                for i in COLORS:
                    for k in COLORS:
                        if blk[i][k] != 0:
                            nonzero = True
                            far.add(k if u == p else i)
                if nonzero and far == {r}:
                    servers.append(j)
            res[(p, r)] = servers
    return res


def sc_unserved(source, n):
    return sum(1 for v in sc_slots(source, n).values() if not v)


print("=== (SC) is gauge-invariant at template level ===")
rng = random.Random(777)
rows = []
for n, cx, trials in ((4, False, 25), (6, False, 25), (6, True, 10),
                      (8, False, 8)):
    changed = 0
    tmplchanged = 0
    for _ in range(trials):
        src = rand_source(n, rng, cx, zero_prob=0.55)
        one = GQ(1) if cx else F(1)
        g = [[(GQ(F(rng.randint(-6, 6) or 3, rng.randint(1, 3)),
                  F(rng.randint(-4, 4), rng.randint(1, 3))) if cx
               else F(rng.randint(-6, 6) or 3, rng.randint(1, 3)))
              for _ in COLORS] for _ in range(n)]
        for row in g:
            for k, x in enumerate(row):
                if x == 0:
                    row[k] = one * 3
        A = apply_gauge(src, n, g)
        if sc_unserved(A, n) != sc_unserved(src, n):
            changed += 1
        if template_of(A, n) != template_of(src, n):
            tmplchanged += 1
    rows.append({"n": n, "field": "Q(i)" if cx else "Q", "trials": trials,
                 "sc_changed": changed, "template_changed": tmplchanged})
    print(f"  N={n} over {'Q(i)' if cx else 'Q  '}: {trials} (source,gauge) "
          f"pairs -- (SC) count changed {changed}, template changed "
          f"{tmplchanged}   (both must be 0)")
out["sc_gauge_invariance"] = rows
assert all(r["sc_changed"] == 0 and r["template_changed"] == 0 for r in rows)

# MUTATION CONTROL: (SC) must be sensitive to a genuine template change
sens = 0
tested = 0
for _ in range(60):
    src = rand_source(6, rng, False, zero_prob=0.55)
    base = sc_unserved(src, 6)
    e = rng.choice(edges_of(6))
    i, j = rng.randrange(3), rng.randrange(3)
    mut = {k: [row[:] for row in src[k]] for k in edges_of(6)}
    mut[e][i][j] = F(0) if mut[e][i][j] != 0 else F(5)
    tested += 1
    if sc_unserved(mut, 6) != base:
        sens += 1
out["sc_mutation_control"] = {"tested": tested, "changed": sens}
print(f"  [MUTATION] flipping one cell changes the (SC) count in "
      f"{sens}/{tested} cases  (must be > 0)")
assert sens > 0


# ------------------------------------------- COROLLARY W10-6, the logic step
print("\n=== COROLLARY W10-6 ===")
thm = os.path.join(ROOT, "proofs", "six-site-arbitrary-complex-obstruction.md")
txt = open(thm).read()
has_thm = ("There is no collection of complex matrices" in txt
           and "Delta_{6,3}" in txt.replace("\\", ""))
print(f"  committed six-site theorem present and states 'no complex A with "
      f"H_6(A)=Delta_(6,3)': {has_thm}")
out["committed_six_site_theorem_found"] = has_thm
print("  logic: mixed-exact at N=6 with all three pures nonzero")
print("         --W10-G-->  an EXACT six-site source exists")
print("         --Thm 1.1--> contradiction.  Hence some pure vanishes.  VALID.")
print("  (note: the corollary only needs W10-G's EXISTENCE half, not the")
print("   'same template' half, so it is robust to the template clause.)")

# empirical consistency: every mixed-exact N=6 witness W10 published must have
# a vanishing pure -- re-verified with A4's own engine from the stored source.
with open(os.path.join(W10, "results_b_witness_n6.json")) as fh:
    WIT = json.load(fh)
rows = []
for key, rec in WIT.items():
    if not isinstance(rec, dict) or "source" not in rec:
        continue
    src = {}
    raw = rec["source"]
    for e in edges_of(6):
        k = f"{e[0]},{e[1]}"
        blk = raw.get(k)
        src[e] = ([[F(x) for x in row] for row in blk] if blk
                  else [[F(0)] * 3 for _ in COLORS])
    mixed_bad = sum(1 for w in product(COLORS, repeat=6)
                    if E.is_mixed(w) and H(src, 6, w) != 0)
    p = pures(src, 6)
    rows.append({"witness": key, "label": rec.get("label"),
                 "mixed_defects_A4": mixed_bad,
                 "pures_A4": [str(x) for x in p],
                 "claimed_pures": rec.get("pure_coefficients"),
                 "has_vanishing_pure": any(x == 0 for x in p),
                 "agrees_with_w10": ([str(x) for x in p]
                                     == list(rec.get("pure_coefficients", [])))
                 })
    print(f"  {key:10s} mixed defects (A4 engine) = {mixed_bad}; pures = "
          f"{[str(x) for x in p]}; vanishing pure: "
          f"{any(x == 0 for x in p)}; matches W10: {rows[-1]['agrees_with_w10']}")
out["n6_witnesses"] = rows
out["all_witnesses_mixed_exact"] = all(r["mixed_defects_A4"] == 0 for r in rows)
out["all_witnesses_have_vanishing_pure"] = all(r["has_vanishing_pure"]
                                               for r in rows)
print(f"  all re-verified mixed-exact: {out['all_witnesses_mixed_exact']}; "
      f"all have a vanishing pure (as W10-6 requires): "
      f"{out['all_witnesses_have_vanishing_pure']}")

# MUTATION CONTROL on the witness checker
if rows:
    key = rows[0]["witness"]
    raw = WIT[key]["source"]
    src = {}
    for e in edges_of(6):
        blk = raw.get(f"{e[0]},{e[1]}")
        src[e] = ([[F(x) for x in row] for row in blk] if blk
                  else [[F(0)] * 3 for _ in COLORS])
    src[(0, 1)][0][0] += F(1, 3)
    bad = sum(1 for w in product(COLORS, repeat=6)
              if E.is_mixed(w) and H(src, 6, w) != 0)
    out["witness_mutation_control"] = bad
    print(f"  [MUTATION] perturbing one cell of {key}: {bad} mixed defects "
          f"appear  (must be > 0)")
    assert bad > 0

with open(os.path.join(HERE, "results_chk08.json"), "w") as fh:
    json.dump(out, fh, indent=1, default=str)
print("wrote results_chk08.json")
