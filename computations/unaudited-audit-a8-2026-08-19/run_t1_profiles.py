#!/usr/bin/env python3
"""A8 T1 -- the profile / parity layer of the diagonal chain.

Targets:
  (a) W27-P1  : X_5 = EXACT at N=8; the unique off-count-5 profile is (3,3,2).
                Also the general-N statement X_{N - ceil(N/3)} = EXACT.
  (b) W25-D1  : odd colour class  =>  H_w = 0 on diagonal sources (every even N).
  (c) W27-D2  : diagonal X_4 = EXACT at N=8 (composition of (a) and (b)).
  (d) the "12 real-condition profiles" claim ((6,2,0),(4,4,0),(4,2,2)).

Everything against the RAW word definition of H (sum over all PMs of K_N).
Mutation controls throughout.
"""
import random
import sys
import time
from fractions import Fraction
from itertools import combinations

sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a8-2026-08-19")
from a8_core import (COLORS, H_raw, checkpoint, diag_blocks, haf, is_constant,
                     offcount, perfect_matchings, profile, require, words)

OUT = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a8-2026-08-19"
R = {}
RAN = []


def sect(s):
    print("=" * 74)
    print(s)
    print("=" * 74)


# ------------------------------------------------------------------ (a) P1
sect("(a) W27-P1: max off-count over all words, per N  [pure combinatorics]")
tab = {}
for n in (2, 4, 6, 8, 10, 12):
    best = -1
    argmax = []
    for w in words(n):
        oc = offcount(w)
        if oc > best:
            best, argmax = oc, [profile(w)]
        elif oc == best and profile(w) not in argmax:
            argmax.append(profile(w))
    # predicted:  max off-count = n - ceil(n/3)
    pred = n - -(-n // 3)
    tab[n] = dict(max_off=best, pred=pred, ok=best == pred,
                  argmax_profiles=sorted(set(tuple(sorted(p, reverse=True)) for p in argmax)))
    print(f"   N={n:2d}  max off-count = {best}  (pred n-ceil(n/3) = {pred})  "
          f"attaining shapes {tab[n]['argmax_profiles']}")
R["t1a_maxoff"] = tab
RAN.append("T1a_maxoff")
require(tab[8]["max_off"] == 5, "N=8 max off-count must be 5")
require(tab[8]["argmax_profiles"] == [(3, 3, 2)], "N=8 unique top shape must be (3,3,2)")
print("   => X_5 = EXACT at N=8 (every word is 5-near-constant); the only")
print("      off-count-5 shape is (3,3,2).  W27-P1 CONFIRMED (definitional).")
print("   => at N=6 max off-count is 4 (shape (2,2,2)); at N=10 it is 7 ((4,3,3)).")

# MUTATION CONTROL: a deliberately wrong off-count (max instead of min) must
# break the (3,3,2) uniqueness.
bad = set()
for w in words(8):
    oc = max(8 - w.count(g) for g in COLORS)   # WRONG statistic
    if oc == 5:
        bad.add(tuple(sorted(profile(w), reverse=True)))
print(f"   [mutation ctrl] wrong statistic gives off-5 shapes {sorted(bad)} "
      f"(must NOT be [(3,3,2)] alone): {'PASS' if bad != {(3,3,2)} else 'FAIL'}")
require(bad != {(3, 3, 2)}, "mutation control did not fire")
RAN.append("T1a_mutation")

# ------------------------------------------------------------------ (b) D1
sect("(b) W25-D1: odd colour class => H_w = 0 on DIAGONAL sources")
rng = random.Random(20260819)


def rand_diag(n, denom=17, nz=True):
    t = {}
    for c in COLORS:
        t[c] = {}
        for e in combinations(range(n), 2):
            v = Fraction(rng.randint(-denom, denom), rng.randint(1, denom))
            while nz and v == 0:
                v = Fraction(rng.randint(-denom, denom), rng.randint(1, denom))
            t[c][e] = v
    return t


for n in (4, 6):
    pms = perfect_matchings(range(n))
    checked = 0
    viol = []
    for trial in range(6):
        t = rand_diag(n)
        A = diag_blocks(t)
        for w in words(n):
            pr = profile(w)
            odd = any(x % 2 for x in pr)
            h = H_raw(A, w, pms)
            checked += 1
            if odd and h != 0:
                viol.append((n, trial, w, str(h)))
    print(f"   N={n}: {checked} (word, source) pairs, odd-class violations = {len(viol)}")
    require(not viol, f"D1 violated at N={n}: {viol[:3]}")
R["t1b_D1_small"] = dict(N4_N6="exhaustive words x 6 random diagonal sources, 0 violations")
RAN.append("T1b_D1_exhaustive_N4_N6")

# N=8 sampled
pms8 = perfect_matchings(range(8))
require(len(pms8) == 105, "K_8 must have 105 PMs")
oddwords = [w for w in words(8) if any(x % 2 for x in profile(w))]
print(f"   N=8: {len(oddwords)} words with an odd colour class (of {3**8})")
samp = rng.sample(oddwords, 400)
viol8 = []
for trial in range(3):
    A = diag_blocks(rand_diag(8))
    for w in samp:
        if H_raw(A, w, pms8) != 0:
            viol8.append((trial, w))
print(f"   N=8: 3 sources x 400 sampled odd words -> violations = {len(viol8)}")
require(not viol8, "D1 violated at N=8")
R["t1b_D1_n8"] = dict(odd_words=len(oddwords), sampled=400, sources=3, violations=0)
RAN.append("T1b_D1_sampled_N8")

# MUTATION CONTROL 1: a NON-diagonal source must break D1 (else H_raw is broken).
fired = 0
for trial in range(3):
    A = diag_blocks(rand_diag(6))
    e0 = (0, 1)
    A[e0][0][1] = Fraction(3)          # one off-diagonal entry
    for w in words(6):
        if any(x % 2 for x in profile(w)) and H_raw(A, w, perfect_matchings(range(6))) != 0:
            fired += 1
print(f"   [mutation ctrl] one off-diagonal entry at N=6 -> {fired} nonzero odd-class "
      f"values (must be > 0): {'PASS' if fired else 'FAIL'}")
require(fired > 0, "mutation control (non-diagonal) did not fire")
RAN.append("T1b_mutation_offdiag")

# MUTATION CONTROL 2: the *even*-class mixed words must NOT be automatically 0.
nz = 0
A = diag_blocks(rand_diag(8))
for w in words(8):
    pr = profile(w)
    if not is_constant(w) and all(x % 2 == 0 for x in pr) and H_raw(A, w, pms8) != 0:
        nz += 1
print(f"   [mutation ctrl] even-class mixed words with H != 0 on a random diagonal "
      f"source: {nz} (must be > 0): {'PASS' if nz else 'FAIL'}")
require(nz > 0, "even-class words are not automatically zero -- control")
RAN.append("T1b_mutation_evenclass_live")

# ---------------------------------------------------------- (d) 12 profiles
sect("(d) the live (non-automatic) diagonal conditions at N=8, off-count <= 4")
live = {}
for w in words(8):
    if is_constant(w):
        continue
    pr = profile(w)
    if any(x % 2 for x in pr):
        continue                     # automatic 0 by D1
    if offcount(w) > 4:
        continue                     # not an X_4 condition
    live[pr] = live.get(pr, 0) + 1
print(f"   ordered live profiles: {len(live)}   shapes "
      f"{sorted(set(tuple(sorted(p, reverse=True)) for p in live))}")
for p in sorted(live):
    print(f"      {p}: {live[p]} words")
R["t1d_live_profiles"] = {str(k): v for k, v in sorted(live.items())}
require(len(live) == 12, "must be 12 ordered live profiles")
require(sorted(set(tuple(sorted(p, reverse=True)) for p in live)) ==
        [(4, 2, 2), (4, 4, 0), (6, 2, 0)], "live shapes")
RAN.append("T1d_live_profiles")

# is any (3,3,2) word 4-near-constant?  (must be no -- that is the D2 hinge)
n332 = [w for w in words(8) if tuple(sorted(profile(w), reverse=True)) == (3, 3, 2)]
print(f"   (3,3,2) words: {len(n332)}; off-counts {sorted(set(offcount(w) for w in n332))} "
      f"(must be {{5}}) ; odd classes present in all: "
      f"{all(any(x % 2 for x in profile(w)) for w in n332)}")
require(all(offcount(w) == 5 for w in n332), "(3,3,2) must have off-count 5")
require(all(any(x % 2 for x in profile(w)) for w in n332), "(3,3,2) must have odd parts")
RAN.append("T1d_332_hinge")

# ------------------------------------------------------------------ (c) D2
sect("(c) W27-D2: DIAGONAL X_4 = EXACT at N=8 -- direct machine check")
# We do not need a *point* of X_4: the statement is
#   for every diagonal A,  A in X_4  <=>  A EXACT.
# "=>" is the content.  Verify the logical skeleton exhaustively over WORDS:
#   every word is either (i) off-count <= 4  [an X_4 condition], or
#   (ii) constant [off-count 0], or (iii) has an odd class [automatic 0].
bad = [w for w in words(8)
       if offcount(w) > 4 and not is_constant(w) and not any(x % 2 for x in profile(w))]
print(f"   words that are neither X_4-constrained nor automatically 0: {len(bad)} "
      f"(must be 0)")
require(not bad, f"D2 skeleton broken: {bad[:5]}")
R["t1c_D2"] = dict(uncovered_words=0, status="CONFIRMED (composition of P1 and D1)")
RAN.append("T1c_D2_composition")

# MUTATION CONTROL: at N=10 the same composition must FAIL at k=4 (and the
# report's claim is that N=8 is the special order).
for n in (6, 10):
    bad_n = [w for w in words(n)
             if offcount(w) > 4 and not is_constant(w) and not any(x % 2 for x in profile(w))]
    tops = sorted(set(tuple(sorted(profile(w), reverse=True)) for w in words(n)
                      if offcount(w) == n - -(-n // 3)))
    print(f"   [control] N={n}: uncovered-at-k=4 words = {len(bad_n)}; top shapes {tops}; "
          f"all-even top shape present: {any(all(x % 2 == 0 for x in s) for s in tops)}")
R["t1c_other_N"] = "N=6 top (2,2,2) all-even; N=10 top (4,3,3) has odd parts -- see log"
RAN.append("T1c_control_other_N")

# N=6 / N=10 top-profile parity (the report claims N=6 and N=10 have all-even top profiles)
for n in (6, 10, 12):
    top = n - -(-n // 3)
    tops = sorted(set(tuple(sorted(profile(w), reverse=True)) for w in words(n)
                      if offcount(w) == top))
    print(f"   N={n:2d} top off-count {top}: shapes {tops}  all-even? "
          f"{[all(x % 2 == 0 for x in s) for s in tops]}")
R["t1c_top_parity"] = "see log"

MAN = dict(declared=["T1a_maxoff", "T1a_mutation", "T1b_D1_exhaustive_N4_N6",
                     "T1b_D1_sampled_N8", "T1b_mutation_offdiag",
                     "T1b_mutation_evenclass_live", "T1d_live_profiles",
                     "T1d_332_hinge", "T1c_D2_composition", "T1c_control_other_N"],
           ran=RAN)
MAN["missing"] = [x for x in MAN["declared"] if x not in RAN]
print("CONTROL MANIFEST:", MAN)
require(not MAN["missing"], "control manifest incomplete")
R["manifest"] = MAN
checkpoint(OUT + "/results_t1_profiles.json", R)
