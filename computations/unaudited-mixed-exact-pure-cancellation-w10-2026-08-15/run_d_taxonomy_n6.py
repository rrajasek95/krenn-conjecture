#!/usr/bin/env python3
"""W10 task D -- the N=6 TAXONOMY: how many of the three pure coefficients can
a MIXED-EXACT six-site source keep NONZERO, and at which admissibility layer?

  #nonzero = 3 : IMPOSSIBLE (Lemma W10-G + committed six-site theorem).
  #nonzero = 2 : EXISTS -- exact construction below (Delta_{6,2} padded with a
                 zero third colour).  Template NOT admissible (colour-2 pure
                 fibre empty).  Whether it can be made admissible is probed.
  #nonzero = 1 : probed (this is STAGE_A's pattern at N=8).
  #nonzero = 0 : REALISED on admissible templates at every support (task B).

Floats appear only in the anchored least-squares SEARCHES, explicitly labelled;
the two constructions (Delta_{6,2}, Delta_{4,3}) are exact.
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction as F
from itertools import combinations, product

import numpy as np
from scipy.optimize import least_squares

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (HERE,):
    if p not in sys.path:
        sys.path.insert(0, p)

import w10_core as w10                                            # noqa: E402
import w10_numeric as wn                                          # noqa: E402
from w10_core import COLORS, require                              # noqa: E402

N = 6
EDGES = w10.edges(N)
OUT = {}
log = []


def say(s="", flush=True):
    print(s, flush=flush)
    log.append(s)


def exact_report(label, src, size=N, colours=COLORS):
    vals = {w: w10.hafnian_word(src, size, w)
            for w in product(colours, repeat=size)}
    bad = [w for w in vals if len(set(w)) > 1 and vals[w] != 0]
    aud = w10.audit(w10.template_of(src, size), size)
    rec = {"label": label, "mixed_defects": len(bad),
           "pures": [str(vals[(c,) * size]) for c in colours],
           "m": aud["m"], "Sigma": aud["Sigma"], "beta": aud["beta"],
           "pure_fibres": aud["T4_pure_fibres"], "T4": aud["T4"],
           "T5": aud["T5"], "T6": aud["T6"], "S": aud["S"],
           "ADMISSIBLE": aud["ADMISSIBLE"]}
    say(f"  {label:42s} mixdef {len(bad):3d} | pures {rec['pures']} | "
        f"m={rec['m']} Sigma={rec['Sigma']} | fibres {rec['pure_fibres']} | "
        f"ADMISSIBLE {rec['ADMISSIBLE']}")
    return rec


# ------------------------------------------------------- D0: the 3-case proof
say("=" * 96)
say("D0  #nonzero pures = 3 is IMPOSSIBLE at N=6 (Lemma W10-G + six-site Thm 1.1)")
say("=" * 96)
d43 = w10.zero_source(4)
for c, es in {0: ((0, 1), (2, 3)), 1: ((0, 2), (1, 3)),
              2: ((0, 3), (1, 2))}.items():
    for e in es:
        d43[e][c][c] = F(1)
require(w10.is_exact(d43, 4), "N=4 control broken")
say("  CONTROL that the argument is not vacuous -- at N=4 it is FALSE:")
OUT["D0_control_delta43"] = exact_report("Delta_{4,3} (K_4 exception)", d43, 4)

# ------------------------------- D1: the 2-case EXISTS, exact construction
say()
say("=" * 96)
say("D1  #nonzero pures = 2 -- EXISTS.  Exact construction.")
say("=" * 96)
say("  Restriction lemma: for a colour subset S, H(A|_S)_w = H(A)_w on every")
say("  S-word.  Verified exactly below.  So two nonzero pures at colours c,c'")
say("  give (Lemma W10-G in two colours) an exact TWO-COLOUR source Delta_{6,2}.")
rng = random.Random(4242)
bad = tot = 0
for trial in range(8):
    src = w10.zero_source(N)
    for e in EDGES:
        for i in COLORS:
            for j in COLORS:
                src[e][i][j] = F(rng.randint(-5, 5), rng.randint(1, 3))
    for S in ((0, 1), (0, 2), (1, 2)):
        sub = w10.zero_source(N)
        for e in EDGES:
            for i in S:
                for j in S:
                    sub[e][i][j] = src[e][i][j]
        for w in product(S, repeat=N):
            tot += 1
            if w10.hafnian_word(src, N, w) != w10.hafnian_word(sub, N, w):
                bad += 1
say(f"  restriction lemma: {tot} words checked, {bad} violations (expected 0)")
require(bad == 0, "restriction lemma failed")
OUT["D1_restriction_lemma"] = {"checked": tot, "violations": bad}

say()
say("  CONSTRUCTION (exact, no search).  Take two DISJOINT perfect matchings")
say("  M_0, M_1 whose union is a single N-cycle; a cycle has exactly two")
say("  perfect matchings, so the only supported matchings are M_0 and M_1.")
say("  Give every edge of M_0 the single cell (0,0) and every edge of M_1 the")
say("  single cell (1,1), all weights 1.  Then H_w = [w = 0^N] + [w = 1^N].")
d62 = w10.zero_source(N)
M0 = ((0, 1), (4, 5), (2, 3))
M1 = ((1, 4), (2, 5), (0, 3))
for e in M0:
    d62[e][0][0] = F(1)
for e in M1:
    d62[e][1][1] = F(1)
OUT["D1_delta62"] = exact_report("Delta_{6,2} padded to 3 colours", d62)
require(OUT["D1_delta62"]["mixed_defects"] == 0
        and OUT["D1_delta62"]["pures"] == ["1", "1", "0"], "Delta_62 wrong")
say("  => at N=6 a MIXED-EXACT source with exactly TWO nonzero pure")
say("     coefficients EXISTS.  Its template is NOT admissible: the colour-2")
say("     pure fibre is empty (T4 fails) and min degree is 2 (T5 fails).")
say("  (Same construction works at every even N; the union of two disjoint")
say("   perfect matchings forming one N-cycle has exactly 2 perfect matchings.)")
d82 = w10.zero_source(8)
cyc = [0, 1, 4, 5, 2, 3, 6, 7]
for k in range(0, 8, 2):
    u, v = sorted((cyc[k], cyc[(k + 1) % 8]))
    d82[(u, v)][0][0] = F(1)
for k in range(1, 8, 2):
    u, v = sorted((cyc[k], cyc[(k + 1) % 8]))
    d82[(u, v)][1][1] = F(1)
OUT["D1_delta82"] = exact_report("Delta_{8,2} padded to 3 colours", d82, 8)

# --------------------------- D2 / D3: can the fibres be filled?  (SEARCH)
say()
say("=" * 96)
say("D2/D3  can 2 or 1 nonzero pures be carried on an ADMISSIBLE template?")
say("=" * 96)
say("  Anchors  prod_{e in M} A_e[c][c] = 1  force colour-c's pure fibre to be")
say("  nonempty.  M = {01,23,45}.  FLOAT SEARCH; a miss is 'not found'.")
sys3 = wn.System(N, d=3)
M = ((0, 1), (2, 3), (4, 5))
rs = np.random.default_rng(20260815)


def search(label, pure_targets, anchors, trials):
    best = None
    hits = 0
    for t in range(trials):
        x0 = rs.normal(size=sys3.nv) * (0.3 + 1.5 * rs.random())
        sol = least_squares(
            lambda x: sys3.residual(x, pure_targets=pure_targets,
                                    anchors=anchors), x0,
            jac=lambda x: sys3.jacobian(x, pure_targets=pure_targets,
                                        anchors=anchors),
            method="lm", xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=2000)
        c = float(np.max(np.abs(sol.fun)))
        if best is None or c < best[0]:
            best = (c, sol.x.copy())
        if c < 1e-10:
            hits += 1
    say(f"  {label:52s} best max|res| {best[0]:.3e}  hits {hits}/{trials}")
    return {"label": label, "trials": trials, "best_max_residual": best[0],
            "hits": hits}, best


rows = []
r, b_ctrl = search("[CONTROL] 0 pure targets + anchors on colours 1,2",
                   None, [(1, M), (2, M)], 200)
rows.append(r)
r, b2 = search("2 nonzero pures (H_0=H_1=1) + anchor on colour 2",
               {0: 1.0, 1: 1.0}, [(2, M)], 1500)
rows.append(r)
r, b1 = search("1 nonzero pure (H_0=1) + anchors on colours 1,2",
               {0: 1.0}, [(1, M), (2, M)], 1500)
rows.append(r)
r, b0 = search("all 3 pures = 1 (must FAIL: six-site theorem)",
               {0: 1.0, 1: 1.0, 2: 1.0}, [], 400)
rows.append(r)
OUT["D2_searches"] = rows

# exact re-check of the control hit
if b_ctrl[0] < 1e-9:
    x = b_ctrl[1]
    src = w10.zero_source(N)
    for (e, i, j), k in sys3.vidx.items():
        if abs(x[k]) > 1e-9:
            src[e][i][j] = F(x[k]).limit_denominator(10 ** 7)
    aud = w10.audit(w10.template_of(src, N), N)
    say(f"  [control hit, rationalised] pure fibres {aud['T4_pure_fibres']}, "
        f"admissible {aud['ADMISSIBLE']} -- the exact certified objects of the "
        f"0-pure row are task B's, not this one.")

say()
say("=" * 96)
say("D4  the N=6 taxonomy table")
say("=" * 96)
say(f"{'# nonzero pures':>16} | {'exists?':<12} | {'on an ADMISSIBLE template?':<28} | evidence")
say(f"{'3':>16} | {'NO':<12} | {'n/a':<28} | Lemma W10-G + six-site Thm 1.1")
_s2 = "FOUND" if rows[1]["hits"] else "not found (search)"
_s1 = "FOUND" if rows[2]["hits"] else "not found (search)"
say(f"{'2':>16} | {'YES (exact)':<12} | {_s2:<28} | "
    f"Delta_{{6,2}} cycle construction; anchored search best "
    f"{rows[1]['best_max_residual']:.1e}")
say(f"{'1':>16} | {'?':<12} | {_s1:<28} | "
    f"anchored search best {rows[2]['best_max_residual']:.1e}")
say(f"{'0':>16} | {'YES (exact)':<12} | {'YES, every support 9..15':<28} | task B witnesses")
say()
say(f"  control rows: 0-pure + anchors reaches {rows[0]['best_max_residual']:.1e} "
    f"({rows[0]['hits']}/{rows[0]['trials']} hits) -- the solver CAN reach the")
say(f"  variety; the all-three-pures row reaches only "
    f"{rows[3]['best_max_residual']:.1e} ({rows[3]['hits']}/{rows[3]['trials']} "
    f"hits), as the six-site theorem demands.")

with open(os.path.join(HERE, "results_d_taxonomy_n6.json"), "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
with open(os.path.join(HERE, "log_d_taxonomy_n6.txt"), "w") as fh:
    fh.write("\n".join(log) + "\n")
say("D DONE")
