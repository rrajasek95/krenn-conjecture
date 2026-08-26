#!/usr/bin/env python3
"""W10 task A -- (i) cross-check my core against W6/W9's, (ii) state and verify
the GAUGE FACT precisely, (iii) derive the fork lemma, (iv) mutation controls.

GAUGE FACT (stated here in the exact form W10 relies on).
Let g = (g_{u,c})_{u in V, c in COLORS} be ANY family of NONZERO scalars and
put (g.A)_uv[i][j] = g_{u,i} g_{v,j} A_uv[i][j].  Then for every word w

        H(g.A)_w = ( prod_{u in V} g_{u,w_u} ) * H(A)_w                (G)

because every perfect matching covers every vertex exactly once.  Hence
 (G1) g.A has the SAME template as A (all g_{u,c} != 0);
 (G2) g.A is mixed-exact iff A is;
 (G3) H(g.A)_{c^N} = (prod_u g_{u,c}) H(A)_{c^N}.

LEMMA W10-G (the fork's first link).  If A is mixed-exact at N sites and all
three pure coefficients H_{c^N} are NONZERO, then A is gauge-equivalent to a
fully EXACT source with the SAME template.
Proof: take g_{0,c} = 1/H(A)_{c^N} and g_{u,c} = 1 for u > 0; apply (G1)-(G3).

COROLLARY W10-6 (with the committed six-site theorem: no exact source at N=6).
Every mixed-exact six-site source has H_{c^6} = 0 for at least one colour c.
In particular a mixed-exact six-site source whose template satisfies (T4)
(all three pure fibres nonempty) HAS a pure coefficient vanishing while its
fibre is nonempty.  If that fibre has size 1 the coefficient is a single
nonzero product, so it cannot vanish -- hence the vanishing pure fibre has
size >= 2 and the vanishing is BY CANCELLATION.  So at N = 6 the W10 question
reduces to: does a mixed-exact source on an admissible template exist at all?
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction as F
from itertools import combinations, product

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (HERE,
          os.path.join(REPO, "computations", "unaudited-bridge-w6-2026-08-15"),
          os.path.join(REPO, "computations", "unaudited-cell-ceiling-w9-2026-08-15")):
    if p not in sys.path:
        sys.path.insert(0, p)

import w10_core as w10                                          # noqa: E402
from w10_core import COLORS, F as _F, require                    # noqa: E402
import w6_core                                                   # noqa: E402
import w9_template                                               # noqa: E402

OUT = {}
log = []


def say(s=""):
    print(s)
    log.append(s)


def rand_source(rng, size, zero_bias=0.0, lo=-6, hi=6):
    src = w10.zero_source(size)
    for e in w10.edges(size):
        for i in COLORS:
            for j in COLORS:
                if rng.random() < zero_bias:
                    continue
                src[e][i][j] = F(rng.randint(lo, hi), rng.randint(1, 3))
    return src


# ------------------------------------------------------- A1 cross-check core
say("=" * 78)
say("A1  cross-check: W10 hafnian/template vs W6/W9 implementations")
say("=" * 78)
rng = random.Random(1010)
n_words = n_audit = 0
mism_h = mism_a = 0
for size in (6, 8):
    for trial in range(6 if size == 6 else 3):
        src = rand_source(rng, size, zero_bias=0.35)
        words = list(product(COLORS, repeat=size))
        if size == 8:
            words = rng.sample(words, 300)
        for w in words:
            mine = w10.hafnian_word(src, size, w)
            theirs = w6_core.hafnian(src, tuple(range(size)),
                                     {u: w[u] for u in range(size)})
            n_words += 1
            if mine != theirs:
                mism_h += 1
        tpl_mine = w10.template_of(src, size)
        tpl_w9 = w9_template.template_of(src, size)
        a_mine = w10.audit(tpl_mine, size)
        a_w9 = w9_template.audit(tpl_w9, size)
        n_audit += 1
        same = (tpl_mine == tpl_w9
                and a_mine["m"] == a_w9["m"] and a_mine["Sigma"] == a_w9["Sigma"]
                and a_mine["beta"] == a_w9["beta"]
                and a_mine["T4_pure_fibres"] == a_w9["T4_pure_fibres"]
                and a_mine["T5"] == a_w9["T5_min_degree_ok"]
                and a_mine["T6"] == a_w9["T6_slots_ok"]
                and a_mine["S"] == a_w9["S_singleton_free"]
                and a_mine["mixed_fibre_histogram"] == a_w9["mixed_fibre_histogram"])
        if not same:
            mism_a += 1
say(f"  hafnian values compared : {n_words}   mismatches {mism_h}")
say(f"  template audits compared: {n_audit}   mismatches {mism_a}")
require(mism_h == 0 and mism_a == 0, "core cross-check FAILED")
OUT["A1_crosscheck"] = {"words": n_words, "hafnian_mismatches": mism_h,
                        "audits": n_audit, "audit_mismatches": mism_a}

# ------------------------------------------------------- A2 the gauge identity
say()
say("=" * 78)
say("A2  gauge identity (G):  H(g.A)_w = (prod_u g_{u,w_u}) H(A)_w")
say("=" * 78)
checked = viol = 0
for size in (6, 8):
    for trial in range(5 if size == 6 else 2):
        src = rand_source(rng, size, zero_bias=0.3)
        g = [[F(rng.randint(-5, 5) or 2, rng.randint(1, 3)) for _ in COLORS]
             for _ in range(size)]
        gsrc = w10.apply_gauge(src, size, g)
        words = list(product(COLORS, repeat=size))
        if size == 8:
            words = rng.sample(words, 250)
        for w in words:
            lhs = w10.hafnian_word(gsrc, size, w)
            fac = F(1)
            for u in range(size):
                fac *= g[u][w[u]]
            rhs = fac * w10.hafnian_word(src, size, w)
            checked += 1
            if lhs != rhs:
                viol += 1
say(f"  identity checks {checked}   violations {viol}")
require(viol == 0, "gauge identity FAILED")
OUT["A2_gauge_identity"] = {"checked": checked, "violations": viol}

# MUTATION CONTROL M1: a *non*-gauge transformation must break (G).
say("  [control M1] mutate the transformation to a non-gauge one:")
bad = 0
tot = 0
for trial in range(6):
    src = rand_source(rng, 6, zero_bias=0.2)
    g = [[F(rng.randint(1, 5)) for _ in COLORS] for _ in range(6)]
    gsrc = w10.apply_gauge(src, 6, g)
    # perturb ONE cell of ONE block -> no longer of the form g_{u,i}g_{v,j}
    e = (0, 1)
    gsrc[e][0][0] += F(1)
    for w in product(COLORS, repeat=6):
        fac = F(1)
        for u in range(6):
            fac *= g[u][w[u]]
        tot += 1
        if w10.hafnian_word(gsrc, 6, w) != fac * w10.hafnian_word(src, 6, w):
            bad += 1
say(f"     mutated identity: {bad} of {tot} words now violate (G)  "
    f"(expected: many)")
require(bad > 0, "control M1 did not fire")
OUT["A2_control_M1_nongauge"] = {"violations": bad, "checked": tot}

# MUTATION CONTROL M2: a gauge with a ZERO entry changes the template.
say("  [control M2] gauge with a zero entry -> template changes (G1 needs g!=0):")
src = rand_source(rng, 6, zero_bias=0.0)
g = [[F(1)] * 3 for _ in range(6)]
g[0][2] = F(0)
t0 = w10.template_of(src, 6)
t1 = w10.template_of(w10.apply_gauge(src, 6, g), 6)
say(f"     templates equal? {t0 == t1}  (expected False)")
require(t0 != t1, "control M2 did not fire")
OUT["A2_control_M2_zero_gauge_changes_template"] = (t0 != t1)

# ------------------------------------------- A3 Lemma W10-G, tested positively
say()
say("=" * 78)
say("A3  LEMMA W10-G: mixed-exact + all three pures nonzero  =>  gauges to EXACT")
say("=" * 78)
# Positive control: build genuinely mixed-exact sources with all pures nonzero
# at N = 4 (where exact sources DO exist: the K_4 exception Delta_{4,3}), by
# taking an exact source and de-normalising it with a random gauge.
# First: find an exact N=4 source (exhaustive-free: use the known Delta_{4,3}
# construction verified below from scratch).
def delta43():
    """The K_4 exception Delta_{4,3} (P2's `k4_landing_source` docstring):
    on four sites every unordered pair lies in EXACTLY ONE perfect matching,
    so giving matching k the single cell (k,k) on both of its edges makes
    H_w = [w=0000] + [w=1111] + [w=2222] with no interference at all."""
    src = w10.zero_source(4)
    matchings = {0: ((0, 1), (2, 3)), 1: ((0, 2), (1, 3)), 2: ((0, 3), (1, 2))}
    for c, es in matchings.items():
        for e in es:
            src[e][c][c] = F(1)
    return src


d43 = delta43()
pc = w10.pure_coefficients(d43, 4)
md = w10.mixed_defects(d43, 4)
say(f"  Delta_43 (K_4 exception): pures {pc}  #mixed defects {len(md)}")
aud43 = w10.audit(w10.template_of(d43, 4), 4)
say(f"  Delta_43 template: m={aud43['m']} Sigma={aud43['Sigma']} "
    f"beta={aud43['beta']} pure fibres {aud43['T4_pure_fibres']} "
    f"ADMISSIBLE={aud43['ADMISSIBLE']}")
OUT["A3_delta43_audit"] = {k: v for k, v in aud43.items()
                           if k != "mixed_fibre_histogram"}
require(d43 is not None and w10.is_exact(d43, 4), "no exact N=4 source built")
say(f"  EXACT N=4 source confirmed (Delta_43): pures "
    f"{w10.pure_coefficients(d43, 4)}, mixed defects 0")

lemma_tests = []
for trial in range(20):
    g = [[F(rng.randint(-6, 6) or 3, rng.randint(1, 3)) for _ in COLORS]
         for _ in range(4)]
    A = w10.apply_gauge(d43, 4, g)            # mixed-exact, all pures nonzero
    require(w10.is_mixed_exact(A, 4), "gauged Delta_43 lost mixed-exactness")
    p = w10.pure_coefficients(A, 4)
    require(all(x != 0 for x in p), "gauged Delta_43 lost nonzero pures")
    B = w10.gauge_to_exact(A, 4)
    ok = w10.is_exact(B, 4)
    same_tpl = w10.template_of(A, 4) == w10.template_of(B, 4)
    lemma_tests.append(bool(ok and same_tpl))
say(f"  Lemma W10-G verified on {len(lemma_tests)} de-normalised objects: "
    f"{sum(lemma_tests)}/{len(lemma_tests)} gauge back to EXACT with the SAME template")
require(all(lemma_tests), "Lemma W10-G failed on a positive control")
OUT["A3_lemmaG"] = {"tests": len(lemma_tests), "passed": sum(lemma_tests)}

# MUTATION CONTROL M3: the exactness checker must FIRE on a perturbation.
say("  [control M3] perturb one cell of the exact N=4 source:")
fires = 0
for trial in range(10):
    A = {e: [row[:] for row in d43[e]] for e in w10.edges(4)}
    e = rng.choice(w10.edges(4))
    i, j = rng.choice(COLORS), rng.choice(COLORS)
    A[e][i][j] += F(rng.randint(1, 4))
    if not w10.is_exact(A, 4):
        fires += 1
say(f"     checker rejected {fires}/10 perturbed sources (expected 10/10)")
require(fires == 10, "control M3 did not fire")
OUT["A3_control_M3"] = fires

# ---------------------------------------- A4 the fork lemma, stated & recorded
say()
say("=" * 78)
say("A4  COROLLARY W10-6 (fork link), with the committed six-site theorem")
say("=" * 78)
say("  Committed: proofs/six-site-arbitrary-complex-obstruction.md Thm 1.1 --")
say("  there is NO complex six-site source with H_6(A) = Delta_{6,3}.")
say("  Lemma W10-G (A3) + Thm 1.1  =>  every MIXED-EXACT six-site source has")
say("  H_{c^6} = 0 for at least one colour c.")
say("  If that colour's pure FIBRE is nonempty, H_{c^6} is a sum of >= 1")
say("  nonzero matching products; a single term cannot vanish, so the fibre")
say("  has size >= 2 and the vanishing is BY CANCELLATION.")
say("  Hence at N=6:  W10's question  <=>  does a mixed-exact source on an")
say("  admissible (T4/T5/T6/S) template exist AT ALL?")
say()
say("  Note (recorded, used later): MIXED-EXACT => (S) automatically, since a")
say("  mixed word of fibre 1 would make H_w a single nonzero product; and")
say("  (T4) => (T6), since the matching realising the constant word c^N")
say("  covers every vertex and so fills every slot (u,c).")

# verify the two 'notes' as facts on random templates
n_ok = n_bad = 0
for trial in range(400):
    size = 6
    tpl = {}
    for e in w10.edges(size):
        cells = frozenset((i, j) for i in COLORS for j in COLORS
                          if rng.random() < 0.35)
        tpl[e] = cells
    a = w10.audit(tpl, size)
    if a["T4"]:
        n_ok += 1
        if not a["T6"]:
            n_bad += 1
say(f"  check (T4 => T6) on {n_ok} random templates satisfying T4: "
    f"{n_bad} counterexamples (expected 0)")
require(n_bad == 0, "(T4 => T6) failed")
OUT["A4_T4_implies_T6"] = {"T4_templates": n_ok, "counterexamples": n_bad}

# (mixed-exact => S) is checked on every witness produced later; here a control
# that the S-checker fires:
tpl = {e: frozenset() for e in w10.edges(6)}
for e in ((0, 1), (2, 3), (4, 5)):
    tpl[e] = frozenset({(0, 0), (1, 1), (2, 2)})
a = w10.audit(tpl, 6)
say(f"  [control M4] single-matching template: mixed singletons "
    f"{a['n_mixed_singletons']} (expected > 0), S={a['S']} (expected False)")
require(a["n_mixed_singletons"] > 0 and not a["S"], "control M4 did not fire")
OUT["A4_control_M4"] = a["n_mixed_singletons"]

with open(os.path.join(HERE, "results_a_gauge_and_crosscheck.json"), "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
with open(os.path.join(HERE, "log_a_gauge_and_crosscheck.txt"), "w") as fh:
    fh.write("\n".join(log) + "\n")
say()
say("ALL TASK-A CHECKS PASS")
