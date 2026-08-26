#!/usr/bin/env python3
"""AUDIT A4 / CHECK 06 -- CLAIM 7 (reduction soundness, incl. the UNTESTED
elementary-divisor > 1 branch) and CLAIM 8 (the negative control).

CLAIM 7 has two parts.
  (7a) the torus reduction z = (x^{lambda_1},...,x^{lambda_d}) is surjective
       onto (C*)^d.  Argument: C* is divisible, hence injective as a
       Z-module, so Hom(-,C*) is exact and Lambda -> Z^Sigma dualises to a
       SURJECTION (C*)^Sigma -> Hom(Lambda,C*) = (C*)^d.  We check the
       load-bearing consequence numerically: a NON-SATURATED Lambda still
       has every target hit (roots exist in C but NOT in Q -- so the same
       reduction over Q would be unsound, which we exhibit).
  (7b) BEHAVIOURAL test of the untested branch: a synthetic half-system whose
       binomial lattice has elementary divisor 2 must come back 'undecided',
       not 'killed' and not 'feasible'.

CLAIM 8: the committed near-exact source's template, extracted with MY
extractor; the source's own values must satisfy every extracted ZERO
equation.
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(HERE))
W12 = os.path.join(ROOT, "computations", "unaudited-thickfibre-w12-2026-08-15")
sys.path.insert(0, os.path.join(ROOT, "computations"))
import a4_engine as E   # noqa: E402
import a4_cut as CUT    # noqa: E402

out = {}

# ============================================================ CLAIM 7a
print("=== CLAIM 7a: divisibility of C* is what makes the reduction exact ===")
# Lambda = 2Z inside Z (Sigma = 1, d = 1): z = x^2.
# Over C the map C* -> C*, x -> x^2 is onto; over Q* it is not.
import cmath  # noqa: E402
targets = [-1, 2, 1j, -3 + 4j]
lifts = []
for t in targets:
    x = cmath.sqrt(complex(t))
    lifts.append({"target": str(t), "lift": str(x),
                  "residual": abs(x * x - complex(t))})
qfail = all(not float(q ** 0.5).is_integer() for q in (2, 3, 5))
out["7a_C_surjective_examples"] = lifts
out["7a_Q_not_surjective"] = qfail
print("  x -> x^2 hits every target in C* (residuals):",
      [round(l["residual"], 18) for l in lifts])
print("  over Q* it does not (2,3,5 are not squares):", qfail)
print("  => the reduction is valid over C only; the pipeline's Singular")
print("     tests are UNIT-IDEAL tests, which are stable under Q -> C, so a")
print("     'killed' verdict transfers.  A 'feasible' verdict would not.")

# ============================================================ CLAIM 7b
print("\n=== CLAIM 7b: BEHAVIOURAL test of the elementary-divisor>1 branch ===")
sys.path.insert(0, W12)
import w12_cutdecide as CD   # noqa: E402
import w12_reduce as RED     # noqa: E402
import w12_torus as TOR      # noqa: E402


class FakeHalf:
    """Duck-typed half-system: exactly the interface decide_half consumes."""

    def __init__(self, nvars, mixed, const):
        self.nvars = nvars
        self.mixed_eqs = dict(mixed)
        self.const_eqs = dict(const)
        self.vars = [(0, 0, k) for k in range(nvars)]
        self.sites = tuple(range(2))

    def varname(self, n):
        return f"q{n}"


def run_fake(name, nvars, mixed, const, expect_note):
    hs = FakeHalf(nvars, mixed, const)
    stats = {"immediate_contradiction": [], "forced_zero_words": len(mixed),
             "pinned_other": 0, "live_zero_equations": len(mixed),
             "pinned_side": len(const), "nvars": nvars}
    red = RED.ReducedSystem(hs)
    phi = RED.MonomialValues(red.d)
    contra = False
    for vec, val in red.binomial_rows():
        if phi.learn(vec, val) == "contradiction":
            contra = True
    sol = TOR.TorusSolution(red.d, phi.rows, phi.vals)
    v = CD.decide_half(hs, stats, timeout=60)
    print(f"  [{name}] d={red.d} binomial rows={len(red.binomial_rows())} "
          f"divisors={sol.divisors} free={sol.free} lattice-contradiction="
          f"{contra}\n      -> VERDICT {v['verdict']!r}  ({v.get('reason','')})"
          f"\n      truth: {expect_note}")
    return {"name": name, "d": red.d, "divisors": [str(x) for x in sol.divisors],
            "free": sol.free, "verdict": v["verdict"],
            "reason": v.get("reason", ""), "truth": expect_note}


rows7b = []
# (i) divisor 2, TRUE answer = feasible over C  (t^2 = -1, t = +-i, t != -1)
rows7b.append(run_fake(
    "divisor2-feasible", 3,
    {(0, 0): [(0, 0), (1, 1)]},                 # x0^2 + x1^2 = 0
    {(1, 1): [(0,), (1,)]},                     # x0 + x1 != 0
    "FEASIBLE over C (t=+-i); a 'killed' here would be UNSOUND"))
# (ii) divisor 2 where the system is in fact INFEASIBLE over C:
#      t^2 = -1 and the constant 1 + t^2 must be != 0, i.e. 0 != 0.
rows7b.append(run_fake(
    "divisor2-infeasible", 3,
    {(0, 0): [(0, 0), (1, 1)]},                 # x0^2 + x1^2 = 0
    {(1, 1): [(0, 0), (1, 1)]},                 # x0^2 + x1^2 != 0  (clash!)
    "INFEASIBLE; the honest verdict is 'killed', 'undecided' is a MISS"))
# (iii) control: a divisor-1 system that IS killed, to show the branch guard
#       is what changes the answer, not the shape of the input.
rows7b.append(run_fake(
    "divisor1-killed", 2,
    {(0, 0): [(0,), (1,)], (0, 1): [(0,), (1,)]},
    {(1, 1): [(0,), (1,)]},
    "INFEASIBLE (x0 + x1 = 0 and x0 + x1 != 0); must be 'killed'"))
out["7b_synthetic"] = rows7b
out["7b_no_wrong_kill"] = (rows7b[0]["verdict"] != "killed")
out["7b_branch_reached"] = any(r["divisors"] not in ([], ["1"])
                               for r in rows7b)
print(f"  branch actually exercised: {out['7b_branch_reached']}; "
      f"no wrong kill on the feasible instance: {out['7b_no_wrong_kill']}")

# ============================================================ CLAIM 8
print("\n=== CLAIM 8: negative control, the committed near-exact source ===")
import verify_n8_d2_kill_and_monochrome_rigidity as V   # noqa: E402

blocks = V.build_stage_a(V.STAGE_A_BASE)
tmp = E.Template(8, ())
occ, values = set(), {}
for k, (u, v) in enumerate(tmp.edges):
    table = V.C.oriented(blocks, u, v)
    for i in range(3):
        for j in range(3):
            x = Fraction(table[i][j])
            if x != 0:
                occ.add((k, i, j))
                values[(k, i, j)] = x
T = E.Template(8, occ)
print(f"  template: m={T.m()} sigma={T.sigma()}")

# my own recomputation of H on every word
mixed_defects, const_vals, minfib = 0, {}, None
sizes = []
for w in E.words(8):
    p = T.fibre_poly(w)
    val = E.poly_eval(p, values) if p else 0
    if E.is_mixed(w):
        if p:
            sizes.append(len(p))
        if val != 0:
            mixed_defects += 1
    else:
        const_vals["".join(map(str, w))] = str(val)
minfib = min(sizes) if sizes else 0
print(f"  recomputed by A4's engine: mixed defects = {mixed_defects} "
      f"(must be 0); constants = {const_vals}; min mixed fibre = {minfib}")
out["8_mixed_defects"] = mixed_defects
out["8_constant_values"] = const_vals
out["8_min_mixed_fibre"] = minfib

tot_eq = tot_nz = bad_eq = bad_nz = 0
bad_nz_detail = []
for (L, R) in CUT.even_cuts(8):
    cut = CUT.Cut(T, L, R)
    for tag in ("R", "L"):
        ex = cut.extract(tag)
        side = ex["side"]
        for y in ex["zeros"]:
            p = CUT.half_polys(T, side, y)
            if not p:
                continue
            tot_eq += 1
            if E.poly_eval(p, values) != 0:
                bad_eq += 1
        for y, why in ex["pinned_side"].items():
            p = CUT.half_polys(T, side, y)
            tot_nz += 1
            if E.poly_eval(p, values) == 0:
                bad_nz += 1
                bad_nz_detail.append([sorted(L), tag,
                                      "".join(map(str, y)), why])
out["8_extraction"] = {"zero_equations": tot_eq, "violated": bad_eq,
                       "nonvanishings": tot_nz, "violated_nonvanishings":
                       bad_nz, "violated_nonvanishing_examples":
                       bad_nz_detail[:6]}
print(f"  A4 extractor over all even cuts: {tot_eq} zero-equations "
      f"(violated {bad_eq}), {tot_nz} non-vanishings (violated {bad_nz})")
if bad_nz:
    print(f"    violated non-vanishings are all (P2) constant pins: "
          f"{sorted({d[3] for d in bad_nz_detail})}; examples "
          f"{bad_nz_detail[:3]}")

# MUTATION CONTROL: perturbing one cell must break extracted equations
rng = random.Random(7)
worst = 0
for trial in range(5):
    var = rng.choice(sorted(values))
    mut = dict(values)
    mut[var] = mut[var] + Fraction(1, 7)
    broken = 0
    tot = 0
    for (L, R) in CUT.even_cuts(8):
        cut = CUT.Cut(T, L, R)
        for tag in ("R", "L"):
            ex = cut.extract(tag)
            for y in ex["zeros"]:
                p = CUT.half_polys(T, ex["side"], y)
                if not p:
                    continue
                tot += 1
                if E.poly_eval(p, mut) != 0:
                    broken += 1
    worst = max(worst, broken)
    print(f"  MUTATION {E.varname(T, var)} += 1/7 -> {broken}/{tot} extracted "
          f"equations violated")
out["8_mutation_max_broken"] = worst

with open(os.path.join(HERE, "results_chk06.json"), "w") as fh:
    json.dump(out, fh, indent=1)
print("wrote results_chk06.json")
