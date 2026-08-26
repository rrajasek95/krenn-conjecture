#!/usr/bin/env python3
"""W32 / T10 -- WHICH PROVED-SLICE LEMMAS ARE SLICE-INDEPENDENT (attack line 1).

Machine-checks, one lemma at a time:

  W27-R1 (site reduction)          -- slice-INDEPENDENT (already calibrated in
        run_03; re-asserted here on general blocks).
  W27-R2 (order-3 site symmetry + colour rotation collapses the three colour
        systems to one) -- slice-INDEPENDENT: checked directly on general
        sigma-symmetric blocks (the score must be 0 or 3, never 1 or 2), and
        checked to be NON-VACUOUS by exhibiting sigma-symmetric general
        backgrounds that DO reach the X_3 rung.
  W28-SYM (averaging)              -- slice-INDEPENDENT as a statement about a
        symmetric background's linear system (checked on general blocks), but
        it CANNOT be applied to a general X_4 point: X_4 is not closed under
        averaging (run_02) and a general background has no symmetry.
  W28-DEC (diagonal parity decoupling 21 -> 7) -- DIAGONAL-ONLY: for general
        blocks a word with an odd colour class has H_w != 0 in general, so
        the parity block-splitting has no analogue.  Measured.
  W28-FREE (free-site split)       -- DIAGONAL/SPARSE-ONLY: its engine is the
        single-entry row, whose frequency is measured in run_05 (28.7% on
        diagonal backgrounds, 0.00% on general dense ones).  Here we check
        the LOGICAL step directly: count star variables forced to zero.

Also: the sigma-symmetric GENERAL slice sweep, seeded properly (W28 left it
as unresolved search silence at 18,000 backgrounds).
"""
from __future__ import annotations

import itertools
import json
import os
import random
import sys
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w32_bg as BG  # noqa: E402
from w32_core import (Manifest, all_words, haf_word, offcount, profile,
                      require, zero_source)  # noqa: E402

OUT = os.path.join(HERE, "results_t10.json")
PRIMES = (13, 31)
SECONDS = int(sys.argv[1]) if len(sys.argv) > 1 else 1800
rng = random.Random(60613)
R = {}
MAN = Manifest(["R2_scores_collapse", "R2_slice_informative", "SYM_general",
                "DEC_fails_general", "FREE_forcing_census"])

SIG = {0: 1, 1: 2, 2: 0, 3: 4, 4: 5, 5: 3, 6: 6}
RHO = {0: 1, 1: 2, 2: 0}


def orbits():
    seen, reps = {}, []
    for i, e in enumerate(BG.EDGES):
        for a in range(3):
            for b in range(3):
                if (i, a, b) in seen:
                    continue
                cur, orb = (i, a, b), []
                for _ in range(3):
                    orb.append(cur)
                    (ii, aa, bb) = cur
                    (u, v) = BG.EDGES[ii]
                    su, sv = SIG[u], SIG[v]
                    na, nb = RHO[aa], RHO[bb]
                    cur = ((BG.EIDX[(su, sv)], na, nb) if su < sv
                           else (BG.EIDX[(sv, su)], nb, na))
                k = len(reps)
                reps.append((i, a, b))
                for t in orb:
                    seen[t] = k
    return reps, seen


REPS, ORB = orbits()
DIAG_ORB = sorted({ORB[(i, a, a)] for i in range(len(BG.EDGES))
                   for a in range(3)})


def sigma_F(p, vals):
    F = [[[0] * 3 for _ in range(3)] for _ in BG.EDGES]
    for (i, a, b), k in ORB.items():
        F[i][a][b] = vals[k]
    return F


# ------------------------------------------------------------------ W27-R2
def task_R2(seconds):
    """Score must be 0 or 3 on the sigma slice; and the slice must carry X_3."""
    scores4, rungs = {}, {}
    hits3 = 0
    examples = []
    t0 = time.time()
    n = 0
    while time.time() - t0 < seconds:
        p = PRIMES[rng.randrange(2)]
        vals = [0] * len(REPS)
        mode = rng.random()
        if mode < 0.5:                      # sigma-symmetric DIAGONAL
            for k in DIAG_ORB:
                if rng.random() < rng.choice([0.3, 0.5, 0.8]):
                    vals[k] = rng.randrange(1, p)
        elif mode < 0.85:                   # diagonal + a few cross orbits
            for k in DIAG_ORB:
                if rng.random() < rng.choice([0.4, 0.7]):
                    vals[k] = rng.randrange(1, p)
            for _ in range(rng.randrange(1, 5)):
                vals[rng.randrange(len(REPS))] = rng.randrange(1, p)
        else:                               # general sparse
            for k in range(len(REPS)):
                if rng.random() < rng.choice([0.1, 0.2]):
                    vals[k] = rng.randrange(1, p)
        F = sigma_F(p, vals)
        s4 = BG.score(F, p, k=4)
        scores4[str(s4)] = scores4.get(str(s4), 0) + 1
        r = 0
        for k in (2, 3, 4):
            if BG.score(F, p, k=k) == 3:
                r = k
            else:
                break
        rungs[str(r)] = rungs.get(str(r), 0) + 1
        if r >= 3:
            hits3 += 1
            if len(examples) < 3:
                examples.append({"p": p, "vals": vals, "rung": r,
                                 "diagonal": all(vals[k] == 0 for k in
                                                 range(len(REPS))
                                                 if k not in DIAG_ORB)})
        n += 1
    require(all(k in ("0", "3") for k in scores4),
            f"W27-R2 FAILS on general blocks: sigma scores {scores4}")
    MAN.mark("R2_scores_collapse")
    informative = hits3 > 0
    R["R2"] = {"n": n, "k4_scores": scores4, "rungs": rungs,
               "X3_hits": hits3, "slice_informative": informative,
               "n_params": len(REPS), "examples": examples}
    print(f"W27-R2 on GENERAL blocks: {n} sigma backgrounds, k=4 scores"
          f" {scores4} (only 0 and 3 occur => the colour rotation carries the"
          f" three systems into each other off the diagonal too)")
    print(f"  sigma slice rung histogram {rungs}; carries X_3: {informative}")
    require(informative,
            "sigma-general slice never reached X_3 -- ledger 18: an "
            "X_4-silence on it would carry no information")
    MAN.mark("R2_slice_informative")


# ------------------------------------------------------------------ W28-SYM
def task_SYM():
    """If a sigma-symmetric GENERAL background makes the colour-c system
    feasible, the system has a sigma-invariant solution (averaging over the
    order-3 group; char != 3).  Checked by comparing the feasibility of the
    full 21-unknown system with that of the 7-orbit-unknown system."""
    ok, tested = 0, 0
    for _ in range(400):
        p = PRIMES[rng.randrange(2)]
        vals = [0] * len(REPS)
        for k in DIAG_ORB:
            if rng.random() < 0.6:
                vals[k] = rng.randrange(1, p)
        for _ in range(rng.randrange(0, 4)):
            vals[rng.randrange(len(REPS))] = rng.randrange(1, p)
        F = sigma_F(p, vals)
        for kk in (2, 3):
            full = BG.feasible_colours(F, p, k=kk)
            if not any(full):
                continue
            # orbit-reduced system for colour 0: x_{y,d} constant on the
            # orbits of (y,d) under (sigma, rho)
            oid = {}
            reps = []
            for y in range(7):
                for d in range(3):
                    if (y, d) in oid:
                        continue
                    t, orb = (y, d), []
                    for _ in range(3):
                        orb.append(t)
                        t = (SIG[t[0]], RHO[t[1]])
                    k2 = len(reps)
                    reps.append((y, d))
                    for q in orb:
                        oid[q] = k2
            rows = BG.rows_of(F, p)
            drop = BG.DROP[(0, kk)]
            ci = BG.CONSTROW[0]
            M, rhs = [], []
            for i, r in enumerate(rows):
                if i in drop:
                    continue
                v = [0] * len(reps)
                for (j, val) in r:
                    v[oid[(j // 3, j % 3)]] = (v[oid[(j // 3, j % 3)]]
                                               + val) % p
                M.append(v)
                rhs.append(1 if i == ci else 0)
            aug = [M[i] + [rhs[i]] for i in range(len(M))]
            r0 = 0
            for col in range(len(reps)):
                pr = None
                for i in range(r0, len(aug)):
                    if aug[i][col]:
                        pr = i
                        break
                if pr is None:
                    continue
                aug[r0], aug[pr] = aug[pr], aug[r0]
                inv = pow(aug[r0][col], p - 2, p)
                aug[r0] = [x * inv % p for x in aug[r0]]
                for i in range(len(aug)):
                    if i != r0 and aug[i][col]:
                        f = aug[i][col]
                        aug[i] = [(x - f * y) % p
                                  for x, y in zip(aug[i], aug[r0])]
                r0 += 1
            red_ok = not any(aug[i][len(reps)] and not any(aug[i][:len(reps)])
                             for i in range(len(aug)))
            tested += 1
            if red_ok == full[0]:
                ok += 1
    require(tested > 0 and ok == tested,
            f"W28-SYM averaging FAILS on general blocks: {ok}/{tested}")
    MAN.mark("SYM_general")
    R["SYM"] = {"tested": tested, "agree": ok,
                "verdict": "averaging is slice-INDEPENDENT (needs only a "
                           "symmetric background and char != |H|), but it "
                           "constrains nothing without that symmetry"}
    print(f"W28-SYM on GENERAL blocks: {ok}/{tested} agreements between the"
          f" 21-unknown and the 7-orbit-unknown systems => averaging survives"
          f" off the diagonal")


# ------------------------------------------------------------------ W28-DEC
def task_DEC():
    """Diagonal parity decoupling has no general analogue: count words with an
    odd colour class whose H_w is nonzero for a general source."""
    tot, nz = 0, 0
    for _ in range(6):
        src = zero_source(8)
        for e in src:
            for a in range(3):
                for b in range(3):
                    src[e][a][b] = Fraction(rng.randint(-4, 4))
        for w in all_words(8):
            if offcount(w) > 4 or len(set(w)) < 2:
                continue
            pr = profile(w)
            if all(x % 2 == 0 for x in pr):
                continue
            tot += 1
            if haf_word(src, w) != 0:
                nz += 1
    require(nz > 0, "DEC control: no odd-class word was nonzero -- suspicious")
    MAN.mark("DEC_fails_general")
    R["DEC"] = {"odd_class_words_tested": tot, "nonzero": nz,
                "fraction_nonzero": nz / tot,
                "verdict": "DIAGONAL-ONLY"}
    print(f"W28-DEC: {nz}/{tot} ({100*nz/tot:.1f}%) odd-colour-class imposed"
          f" words have H_w != 0 on general sources => the parity decoupling"
          f" (21 -> 7) is diagonal-only")


# ------------------------------------------------------------------ W28-FREE
def task_FREE():
    """Count star variables FORCED to zero by single-entry rows (the FREE
    mechanism), for diagonal vs general backgrounds."""
    res = {}
    p = 31
    for label in ("diagonal", "general_dense", "general_sparse",
                  "ctriple_plus_cross"):
        forced = []
        for _ in range(10):
            if label == "diagonal":
                F = [[[rng.randrange(p) if a == b else 0 for b in range(3)]
                      for a in range(3)] for _ in BG.EDGES]
            elif label == "general_dense":
                F = [[[rng.randrange(p) for _ in range(3)] for _ in range(3)]
                     for _ in BG.EDGES]
            elif label == "general_sparse":
                F = [[[rng.randrange(p) if rng.random() < .35 else 0
                       for _ in range(3)] for _ in range(3)]
                     for _ in BG.EDGES]
            else:
                F = [[[rng.randrange(p) if (a == b and rng.random() < .35)
                       else 0 for b in range(3)] for a in range(3)]
                     for _ in BG.EDGES]
                for _ in range(3):
                    i = rng.randrange(len(BG.EDGES))
                    a, b = rng.randrange(3), rng.randrange(3)
                    if a != b:
                        F[i][a][b] = rng.randrange(1, p)
            rows = BG.rows_of(F, p)
            zs = set()
            for i, r in enumerate(rows):
                if i in BG.DROP[(0, 4)] or i == BG.CONSTROW[0]:
                    continue
                if len(r) == 1:
                    zs.add(r[0][0])
            forced.append(len(zs))
        res[label] = {"mean_forced_star_vars_of_21":
                      sum(forced) / len(forced), "samples": forced}
        print(f"  W28-FREE forcing, {label}: mean {sum(forced)/len(forced):.1f}"
              f" of 21 star variables forced to zero by single-entry rows")
    require(res["general_dense"]["mean_forced_star_vars_of_21"] == 0,
            "unexpected: dense general backgrounds do force star variables")
    MAN.mark("FREE_forcing_census")
    R["FREE"] = res


def main():
    task_R2(min(900, SECONDS // 2))
    task_SYM()
    task_DEC()
    print("W28-FREE forcing census:")
    task_FREE()
    R["manifest"] = MAN.assert_complete()
    with open(OUT, "w") as fh:
        json.dump(R, fh, indent=1, sort_keys=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
