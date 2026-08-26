#!/usr/bin/env python3
"""AUDIT A4 / CHECK 01 -- engine sanity + CLAIM 4 (the 8-word hand certificate).

Independent of every W12 module.  Exact integer/Fraction arithmetic.
"""
from __future__ import annotations

import json
import os
import sys
from fractions import Fraction
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(HERE))
W8 = os.path.join(ROOT, "computations", "unaudited-template-kill-w8-2026-08-15")

import a4_engine as E  # noqa: E402

out = {}


# ---------------------------------------------------------------- sanity
def sanity():
    r = {}
    for n, expect in ((2, 1), (4, 3), (6, 15), (8, 105), (10, 945)):
        got = len(E.all_perfect_matchings(range(n)))
        r[f"pm_count_{n}"] = got
        assert got == expect, (n, got, expect)
    # every matching is a genuine perfect matching, all distinct
    pms = E.all_perfect_matchings(range(8))
    assert len(set(pms)) == 105
    for M in pms:
        cov = [v for e in M for v in e]
        assert sorted(cov) == list(range(8))
    r["pm_structure_ok"] = True
    # round-trip of the mask encoding
    t = E.Template.from_masks([292, 0, 511, 1] + [0] * 24)
    assert t.to_masks()[:4] == (292, 0, 511, 1)
    assert sorted(t.cells_of(0)) == [(0, 2), (1, 2), (2, 2)]
    r["mask_roundtrip_ok"] = True
    return r


out["sanity"] = sanity()
print("SANITY", out["sanity"])


# ------------------------------------------------- load the m=20 survivor
with open(os.path.join(W8, "results_close_m20.json")) as fh:
    W8DATA = json.load(fh)
SURV_MASKS = tuple(W8DATA["survivors"][0])
print("W8 results_close_m20.json: status =", W8DATA.get("status"),
      "  n_survivors =", len(W8DATA["survivors"]))
T = E.Template.from_masks(SURV_MASKS)
out["survivor_masks"] = list(SURV_MASKS)
out["survivor_m"] = T.m()
out["survivor_sigma"] = T.sigma()
print(f"SURVIVOR m={T.m()} sigma={T.sigma()}")
assert T.m() == 20 and T.sigma() == 58


# ---- independent full-fibre census (also gives the histogram control)
def census(tmpl):
    hist = {}
    live_mixed = 0
    consts = {}
    singl = 0
    polys = {}
    for w in E.words(tmpl.n):
        p = tmpl.fibre_poly(w)
        if not p:
            continue
        polys[w] = p
        # every coefficient must be 1 (distinct-monomial fact)
        assert set(p.values()) == {1}, (w, p)
        if E.is_mixed(w):
            hist[len(p)] = hist.get(len(p), 0) + 1
            live_mixed += 1
            if len(p) == 1:
                singl += 1
        else:
            consts[w] = len(p)
    return hist, live_mixed, consts, singl, polys


hist, live, consts, singl, POLYS = census(T)
out["survivor_histogram"] = {str(k): v for k, v in sorted(hist.items())}
out["survivor_live_mixed"] = live
out["survivor_constant_fibre_sizes"] = {"".join(map(str, k)): v
                                        for k, v in consts.items()}
out["survivor_mixed_singletons"] = singl
print("SURVIVOR mixed-fibre histogram:", sorted(hist.items()),
      " live mixed words:", live, " singletons:", singl)
print("SURVIVOR constant fibre sizes:", out["survivor_constant_fibre_sizes"])
W8_HIST = {2: 90, 3: 42, 8: 8, 10: 12, 12: 6, 15: 1}
out["histogram_matches_w8_published"] = (hist == W8_HIST)
print("matches W8's published histogram:", hist == W8_HIST)


# ------------------------------------------------------- CLAIM 4 fibres
WORDS = ["00011000", "00011020", "00111000", "00111020",
         "00100000", "00100020", "00000020"]
CONST = "00000000"
CLAIMED = {
    "00011000": ["x_07_00 x_13_01 x_24_01 x_56_00",
                 "x_07_00 x_13_01 x_26_00 x_45_10"],
    "00011020": ["x_07_00 x_13_01 x_24_01 x_56_02",
                 "x_07_00 x_13_01 x_26_02 x_45_10"],
    "00111000": ["x_07_00 x_13_01 x_24_11 x_56_00",
                 "x_07_00 x_13_01 x_26_10 x_45_10"],
    "00111020": ["x_07_00 x_13_01 x_24_11 x_56_02",
                 "x_07_00 x_13_01 x_26_12 x_45_10"],
    "00100000": ["x_07_00 x_15_00 x_26_10 x_34_00",
                 "x_07_00 x_16_00 x_25_10 x_34_00"],
    "00100020": ["x_07_00 x_15_00 x_26_12 x_34_00",
                 "x_07_00 x_16_02 x_25_10 x_34_00"],
    "00000020": ["x_07_00 x_12_00 x_34_00 x_56_02",
                 "x_07_00 x_15_00 x_26_02 x_34_00",
                 "x_07_00 x_16_02 x_25_00 x_34_00"],
    "00000000": ["x_07_00 x_12_00 x_34_00 x_56_00",
                 "x_07_00 x_15_00 x_26_00 x_34_00",
                 "x_07_00 x_16_00 x_25_00 x_34_00"],
}
cert_rows = {}
allmatch = True
for s in WORDS + [CONST]:
    w = tuple(int(ch) for ch in s)
    p = T.fibre_poly(w)
    mine = sorted(" ".join(E.varname(T, v) for v in sorted(mono))
                  for mono in p)
    claimed = sorted(CLAIMED[s])
    ok = (mine == claimed)
    allmatch &= ok
    cert_rows[s] = {"mixed": E.is_mixed(w), "size": len(p),
                    "monomials": mine, "matches_w12_report": ok}
    print(f"  {s} {'mixed ' if E.is_mixed(w) else 'CONST '} "
          f"|fibre|={len(p)} match={ok}")
out["certificate_fibres"] = cert_rows
out["certificate_fibres_all_match"] = allmatch
print("CLAIM 4 fibre table matches W12's report:", allmatch)


# --------------- the proportionality chain, re-derived symbolically
# Work in the field Q(a) of rational functions?  No -- do it structurally:
# assign ALL cells generic nonzero rationals, impose the six binomial
# equations by SOLVING for six cells, then verify F(0^8) = lambda F(w7)
# identically.  We do it with exact Fractions on a random-but-fixed point.
def cell(u, v, i, j):
    return (T.eidx[(u, v)], i, j)


def check_chain():
    """Exact re-derivation of the lambda chain on a generic solution point."""
    import random
    rng = random.Random(20260815)
    res = {"trials": 0, "chain_ok": 0, "F0_zero": 0}
    for trial in range(200):
        # free values (all nonzero rationals)
        val = {}
        for var in T.occ:
            val[var] = Fraction(rng.randint(1, 40), rng.randint(1, 40)) * \
                rng.choice([1, -1])
        # impose w1..w6 by solving for six cells:
        #   w1: x24_01 x56_00 + x26_00 x45_10 = 0  -> solve x26_00
        #   w2: x24_01 x56_02 + x26_02 x45_10 = 0  -> solve x26_02
        #   w3: x24_11 x56_00 + x26_10 x45_10 = 0  -> solve x26_10
        #   w4: x24_11 x56_02 + x26_12 x45_10 = 0  -> solve x26_12
        #   w5: x15_00 x26_10 + x16_00 x25_10 = 0  -> solve x16_00
        #   w6: x15_00 x26_12 + x16_02 x25_10 = 0  -> solve x16_02
        v = val
        v[cell(2, 6, 0, 0)] = -v[cell(2, 4, 0, 1)] * v[cell(5, 6, 0, 0)] / \
            v[cell(4, 5, 1, 0)]
        v[cell(2, 6, 0, 2)] = -v[cell(2, 4, 0, 1)] * v[cell(5, 6, 0, 2)] / \
            v[cell(4, 5, 1, 0)]
        v[cell(2, 6, 1, 0)] = -v[cell(2, 4, 1, 1)] * v[cell(5, 6, 0, 0)] / \
            v[cell(4, 5, 1, 0)]
        v[cell(2, 6, 1, 2)] = -v[cell(2, 4, 1, 1)] * v[cell(5, 6, 0, 2)] / \
            v[cell(4, 5, 1, 0)]
        v[cell(1, 6, 0, 0)] = -v[cell(1, 5, 0, 0)] * v[cell(2, 6, 1, 0)] / \
            v[cell(2, 5, 1, 0)]
        v[cell(1, 6, 0, 2)] = -v[cell(1, 5, 0, 0)] * v[cell(2, 6, 1, 2)] / \
            v[cell(2, 5, 1, 0)]
        if any(x == 0 for x in v.values()):
            continue
        res["trials"] += 1
        # the six equations really hold now
        for s in WORDS[:6]:
            assert E.poly_eval(POLYS[tuple(int(c) for c in s)], v) == 0, s
        lam = v[cell(5, 6, 0, 0)] / v[cell(5, 6, 0, 2)]
        ok = (v[cell(2, 6, 0, 0)] == lam * v[cell(2, 6, 0, 2)] and
              v[cell(2, 6, 1, 0)] == lam * v[cell(2, 6, 1, 2)] and
              v[cell(1, 6, 0, 0)] == lam * v[cell(1, 6, 0, 2)])
        res["chain_ok"] += bool(ok)
        F0 = E.poly_eval(POLYS[(0,) * 8], v)
        Fw7 = E.poly_eval(POLYS[tuple(int(c) for c in "00000020")], v)
        assert F0 == lam * Fw7, (F0, lam, Fw7)
        # now additionally impose w7 = 0 by solving for x12_00, and check F0 = 0
        v2 = dict(v)
        v2[cell(1, 2, 0, 0)] = -(v[cell(1, 5, 0, 0)] * v[cell(2, 6, 0, 2)] +
                                 v[cell(1, 6, 0, 2)] * v[cell(2, 5, 0, 0)]) / \
            v[cell(5, 6, 0, 2)]
        if v2[cell(1, 2, 0, 0)] == 0:
            continue
        assert E.poly_eval(POLYS[tuple(int(c) for c in "00000020")], v2) == 0
        if E.poly_eval(POLYS[(0,) * 8], v2) == 0:
            res["F0_zero"] += 1
    return res


out["lambda_chain"] = check_chain()
print("LAMBDA CHAIN (exact, 200 generic points):", out["lambda_chain"])

with open(os.path.join(HERE, "results_chk01.json"), "w") as fh:
    json.dump(out, fh, indent=1)
print("wrote results_chk01.json")
