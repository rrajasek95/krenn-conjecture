#!/usr/bin/env python3
"""AUDIT A4 / CHECK 09 -- the remaining adversarial controls for W12-A/W12-B.

(a) the EVENNESS of |L|,|R| is load-bearing: with an odd part, supported
    matchings use an ODD number of crossing edges and a single active
    crossing edge does NOT give a factorisation;
(b) the split-certificate verifier rejects malformed certificates;
(c) cross-implementation agreement: A4's extractor vs the probe's w12_cut on
    the same templates (equation and non-vanishing counts);
(d) MUTATION on the pinning RULE: replacing (P1)/(P2) by "pin everything"
    must manufacture kills where none are sound.
"""
from __future__ import annotations

import json
import os
import sys
from fractions import Fraction
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(HERE))
W8 = os.path.join(ROOT, "computations", "unaudited-template-kill-w8-2026-08-15")
W12D = os.path.join(ROOT, "computations",
                    "unaudited-thickfibre-w12-2026-08-15")
sys.path.insert(0, os.path.join(ROOT, "computations"))
import a4_engine as E   # noqa: E402
import a4_cut as CUT    # noqa: E402

out = {}
N = 8

with open(os.path.join(W8, "results_close_m20.json")) as fh:
    SURV = E.Template.from_masks(json.load(fh)["survivors"][0])
with open(os.path.join(W8, "results_immunity.json")) as fh:
    IMM = {e["m"]: E.Template.from_masks(e["template"])
           for e in json.load(fh)["results"]}

# ------------------------------------------------------------------ (a)
print("=== (a) evenness of the parts is load-bearing ===")
T = IMM[20]
rows = []
for L in (frozenset({0, 1, 2}), frozenset({0}), frozenset({0, 1, 2, 3})):
    R = frozenset(range(N)) - L
    counts = set()
    star_nonfactor = 0
    star_total = 0
    for w in E.words(N):
        for M in T.fibre_matchings(w):
            counts.add(sum(1 for (u, v) in M if (u in L) != (v in L)))
        if CUT.star_like(CUT.active_crossing(T, w, L)):
            star_total += 1
            F_ = T.fibre_poly(w)
            FL = T.fibre_poly(w, sites=sorted(L))
            FR = T.fibre_poly(w, sites=sorted(R))
            prod = E.poly_mul(FL, FR) if (FL and FR) else {}
            if F_ != prod:
                star_nonfactor += 1
    rows.append({"L": sorted(L), "even": len(L) % 2 == 0,
                 "crossing_counts": sorted(counts),
                 "star_words": star_total,
                 "star_words_that_DO_NOT_factor": star_nonfactor})
    print(f"  L={sorted(L)} (|L| {'even' if len(L)%2==0 else 'ODD '}): "
          f"crossing-edge counts realised = {sorted(counts)}; of "
          f"{star_total} star-crossing words, {star_nonfactor} FAIL to factor")
out["a_parity"] = rows
odd = [r for r in rows if not r["even"]]
out["a_odd_breaks_factorisation"] = any(
    r["star_words_that_DO_NOT_factor"] > 0 for r in odd)
print(f"  => evenness load-bearing: {out['a_odd_breaks_factorisation']}")

# ------------------------------------------------------------------ (b)
print("\n=== (b) malformed split certificates must be rejected ===")


def split_ok(T, L, c, cp):
    """The three W12-A clauses, checked independently."""
    R = frozenset(range(N)) - frozenset(L)
    L = frozenset(L)
    if len(L) % 2 or len(R) % 2 or not L or not R or c == cp:
        return False, "shape"
    w = tuple(c if v in L else cp for v in range(N))
    for word in ((c,) * N, (cp,) * N, w):
        if not CUT.star_like(CUT.active_crossing(T, word, L)):
            return False, "not star"
        F_ = T.fibre_poly(word)
        FL = T.fibre_poly(word, sites=sorted(L))
        FR = T.fibre_poly(word, sites=sorted(R))
        if F_ != (E.poly_mul(FL, FR) if (FL and FR) else {}):
            return False, "no factorisation"
    if not T.fibre_poly((c,) * N) or not T.fibre_poly((cp,) * N):
        return False, "empty constant fibre"
    return True, "valid"


cases = [((0, 1, 2, 3), 0, 1, True, "the genuine certificate"),
         ((0, 1, 2), 0, 1, False, "ODD |L|"),
         ((0, 1, 2, 3), 0, 0, False, "c = c'"),
         ((0, 1, 2, 3), 0, 2, None, "different colour pair"),
         ((0, 1, 2, 3, 4, 5, 6, 7), 0, 1, False, "R empty"),
         ((0, 4), 0, 1, None, "a different cut")]
brows = []
for L, c, cp, expect, why in cases:
    ok, reason = split_ok(IMM[20], L, c, cp)
    brows.append({"L": list(L), "c": c, "cprime": cp, "accepted": ok,
                  "reason": reason, "case": why})
    print(f"  {why:24s} L={list(L)} c={c} c'={cp} -> accepted={ok} ({reason})"
          + ("" if expect is None else
             f"   [expected {expect}] {'OK' if ok == expect else 'MISMATCH'}"))
    if expect is not None:
        assert ok == expect
out["b_certificate_verifier"] = brows

# ------------------------------------------------------------------ (c)
print("\n=== (c) cross-implementation agreement with the probe's w12_cut ===")
sys.path.insert(0, W12D)
import w12_core as WC    # noqa: E402
import w12_cut as WCUT   # noqa: E402

geo = WC.geometry()
crows = []
for name, T in (("survivor_m20", SURV), ("immunity_m20", IMM[20]),
                ("immunity_m24", IMM[24])):
    masks = T.to_masks()
    mine_z = mine_nz = 0
    theirs_z = theirs_nz = 0
    for (L, R) in CUT.even_cuts(N):
        cut = CUT.Cut(T, L, R)
        for tag in ("R", "L"):
            ex = cut.extract(tag)
            side = ex["side"]
            mine_z += sum(1 for y in ex["zeros"]
                          if CUT.half_polys(T, side, y))
            mine_nz += len(ex["pinned_side"])
        for tag, (hs, stats) in WCUT.extract(geo, masks, L, R).items():
            theirs_z += len(hs.mixed_eqs)
            theirs_nz += len(hs.const_eqs)
    crows.append({"name": name, "a4_zero_eqs": mine_z,
                  "w12_zero_eqs": theirs_z, "a4_nonvanish": mine_nz,
                  "w12_nonvanish": theirs_nz,
                  "agree": (mine_z == theirs_z and mine_nz == theirs_nz)})
    print(f"  {name:14s} zero-equations A4={mine_z:5d} W12={theirs_z:5d} | "
          f"non-vanishings A4={mine_nz:5d} W12={theirs_nz:5d} | agree="
          f"{crows[-1]['agree']}")
out["c_cross_implementation"] = crows

# ------------------------------------------------------------------ (d)
print("\n=== (d) MUTATION on the pinning rule: 'pin everything' ===")
import verify_n8_d2_kill_and_monochrome_rigidity as V   # noqa: E402
blocks = V.build_stage_a(V.STAGE_A_BASE)
tmp = E.Template(8, ())
occ, values = set(), {}
for k, (u, v) in enumerate(tmp.edges):
    tab = V.C.oriented(blocks, u, v)
    for i in range(3):
        for j in range(3):
            x = Fraction(tab[i][j])
            if x != 0:
                occ.add((k, i, j))
                values[(k, i, j)] = x
NEAR = E.Template(8, occ)


class PinEverything(CUT.Cut):
    def pinned(self, side, other):
        side = tuple(sorted(side))
        return {sub: "BOGUS" for sub in product(range(3), repeat=len(side))}


bad_eq = tot_eq = 0
spurious = 0
for (L, R) in CUT.even_cuts(N):
    cut = PinEverything(NEAR, L, R)
    for tag in ("R", "L"):
        ex = cut.extract(tag)
        side = ex["side"]
        for y in ex["zeros"]:
            p = CUT.half_polys(NEAR, side, y)
            if not p:
                continue
            tot_eq += 1
            if E.poly_eval(p, values) != 0:
                bad_eq += 1
        if set(ex["zeros"]) & set(ex["pinned_side"]):
            spurious += 1
out["d_bogus_pinning"] = {"extracted_equations": tot_eq,
                          "violated_by_the_real_source": bad_eq,
                          "half_systems_declaring_a_kill": spurious}
print(f"  with the bogus rule: {tot_eq} equations extracted from the "
      f"near-exact source's template, {bad_eq} of them VIOLATED by the "
      f"source's own values")
print(f"  and {spurious} half-systems would declare an (unsound) kill")
print(f"  => the (P1)/(P2) pinning rule is load-bearing: "
      f"{bad_eq > 0 and spurious > 0}")
out["d_rule_is_load_bearing"] = (bad_eq > 0 and spurious > 0)

with open(os.path.join(HERE, "results_chk09.json"), "w") as fh:
    json.dump(out, fh, indent=1)
print("wrote results_chk09.json")
