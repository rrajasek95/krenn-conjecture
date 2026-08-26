#!/usr/bin/env python3
r"""W31 / R4 round 2 -- EXACT block-linear solve on the doubled-GHZ deformation.
UNAUDITED PROBE.  Exact rational arithmetic (Fraction).  No floats, no
hill-climbing.  Single process, nice'd, checkpointed to results_r4b.json.

WHY THE METHOD CHANGED.  Round 1 scored candidates by "number of satisfied
equations" and hill-climbed.  That is the wrong objective on an exact-zero
variety: the optimum is a measure-zero set and the landscape is rugged.  Its
own positive control B1b failed twice (52/78, then 69/78 at N=4), so its
output was never evidence.  Round 2 SOLVES instead.

THE STRUCTURE THAT MAKES SOLVING POSSIBLE.  Every perfect matching uses AT
MOST ONE cell of a given block, so for a fixed block e,

    H_w  =  sum_{cells (i,j) of e} coeff_w(i,j) * A_e[i][j]  +  const_w

is **linear** in that block's nine cells, with coefficients that are exact
polynomials in the other blocks' cells.  So the system is multilinear and
admits exact block-coordinate solves: pick a block, build the 6,558 x 9
coefficient matrix over Q, and take its kernel.  A kernel vector with every
occupied cell nonzero is an exact update; the constants are checked after.

THE ANSATZ (Lemma W31-2).  The C_8 member is two GHZ_4^3 copies joined across
the split {0,1,2,3}|{4,5,6,7}.  Hold the twelve within-half single cells at
their GHZ values (all 1 -- any nonzero values are equivalent under the
diagonal gauge) and solve over the **144 cross cells** only.  That is the
doubled-GHZ deformation.

CONTROLS
  S1  POSITIVE CALIBRATION: the same solver at N = 4 on the full template must
      find an exact source.  This is the control round 1 failed; if it fails
      again the lane is still not evidence about anything.
  S2  the linearity claim is verified: for a random block and random values,
      H_w recomputed from the linear form must equal H_w computed directly
      (0 mismatches required).
  S3  every reported update keeps all occupied cells nonzero and is applied
      only if it does not decrease the number of satisfied mixed equations.
  S4  MUTATION: a deliberately wrong coefficient row must break S2.
  S5  reporting is ledger-18: `found` / `not found in budget`, never
      "does not exist".
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
from fractions import Fraction
from itertools import combinations, product

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_F = os.path.join(HERE, "results_r4b.json")
N, FULL = 8, 511
EDGES = tuple(combinations(range(N), 2))
EIDX = {e: i for i, e in enumerate(EDGES)}
C8_MEMBER = [1, 16, 256, 511, 511, 503, 447, 256, 16, 510, 495, 511, 511, 1,
             383, 511, 510, 511, 511, 255, 511, 383, 1, 16, 256, 256, 16, 1]


def pms_of(n):
    def rec(vs):
        if not vs:
            return [()]
        a, rest = vs[0], vs[1:]
        out = []
        for i, b in enumerate(rest):
            for mm in rec(rest[:i] + rest[i + 1:]):
                out.append(((a, b),) + mm)
        return out
    return tuple(tuple(sorted(m)) for m in rec(tuple(range(n))))


def cells_of(mask):
    return [(c // 3, c % 3) for c in range(9) if (mask >> c) & 1]


class Sys:
    def __init__(self, n, T):
        self.n = n
        self.E = tuple(combinations(range(n), 2))
        self.ei = {e: i for i, e in enumerate(self.E)}
        self.pms = pms_of(n)
        self.T = T
        self.words = tuple(product(range(3), repeat=n))
        self.mixed = tuple(w for w in self.words if len(set(w)) > 1)
        self.consts = tuple((c,) * n for c in range(3))
        self.slots = [(e, i, j) for e in self.E
                      for (i, j) in cells_of(T[self.ei[e]])]

    def occ(self, e, i, j):
        return (self.T[self.ei[e]] >> (3 * i + j)) & 1

    def H(self, val, w):
        t = Fraction(0)
        for M in self.pms:
            p = Fraction(1)
            for e in M:
                i, j = w[e[0]], w[e[1]]
                if not self.occ(e, i, j):
                    p = Fraction(0)
                    break
                p *= val[(e, i, j)]
            t += p
        return t

    def lin(self, val, e):
        """H_w = sum_{cells of e} coef[w][(i,j)] * A_e[i][j] + const[w]."""
        cs = cells_of(self.T[self.ei[e]])
        rows, consts = [], []
        for w in self.mixed:
            row = {c: Fraction(0) for c in cs}
            cst = Fraction(0)
            for M in self.pms:
                p, ok, used = Fraction(1), True, None
                for f in M:
                    i, j = w[f[0]], w[f[1]]
                    if not self.occ(f, i, j):
                        ok = False
                        break
                    if f == e:
                        used = (i, j)
                    else:
                        p *= val[(f, i, j)]
                if not ok:
                    continue
                if used is None:
                    cst += p
                else:
                    row[used] += p
            rows.append(row)
            consts.append(cst)
        return cs, rows, consts

    def satisfied(self, val):
        return sum(1 for w in self.mixed if self.H(val, w) == 0)

    def consts_ok(self, val):
        return all(self.H(val, w) != 0 for w in self.consts)


def kernel(rows, cs):
    """exact kernel basis of the matrix whose rows are dicts over cs."""
    m = [[r[c] for c in cs] for r in rows]
    ncol = len(cs)
    piv, r = [], 0
    for c in range(ncol):
        k = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if k is None:
            continue
        m[r], m[k] = m[k], m[r]
        pv = m[r][c]
        m[r] = [x / pv for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        piv.append(c)
        r += 1
        if r == len(m):
            break
    free = [c for c in range(ncol) if c not in piv]
    basis = []
    for fc in free:
        v = [Fraction(0)] * ncol
        v[fc] = Fraction(1)
        for ri, pc in enumerate(piv):
            v[pc] = -m[ri][fc]
        basis.append(v)
    return basis


def solve_lane(S, val, seconds, rng, tag, ck):
    t0 = time.time()
    best = S.satisfied(val)
    nm = len(S.mixed)
    hist = []
    cross = [e for e in S.E if len(cells_of(S.T[S.ei[e]])) > 1]
    while time.time() - t0 < seconds and best < nm:
        e = rng.choice(cross)
        cs, rows, consts = S.lin(val, e)
        # solve the homogeneous part: we need sum coef*A = -const.  Restrict
        # to the words whose const vanishes and take the kernel there; then
        # accept only if the score does not drop (control S3).
        hom = [r for r, c in zip(rows, consts) if c == 0]
        if not hom:
            continue
        bas = kernel(hom, cs)
        if not bas:
            continue
        for _ in range(12):
            coef = [Fraction(rng.randint(-6, 6)) for _ in bas]
            if all(c == 0 for c in coef):
                continue
            cand = [sum(cf * b[k] for cf, b in zip(coef, bas))
                    for k in range(len(cs))]
            if any(x == 0 for x in cand):
                continue                                    # S3: all nonzero
            new = dict(val)
            for k, c in enumerate(cs):
                new[(e, c[0], c[1])] = cand[k]
            sc = S.satisfied(new)
            if sc >= best and S.consts_ok(new):
                if sc > best:
                    hist.append((round(time.time() - t0, 1), sc))
                best, val = sc, new
                break
        ck()
    return dict(tag=tag, best_satisfied=best, n_mixed=nm,
                seconds=round(time.time() - t0, 1), history=hist,
                found_exact_source=(best == nm and S.consts_ok(val)),
                status=("found" if best == nm and S.consts_ok(val)
                        else "not found in budget")), val


def main():
    OUT = {"_header": "UNAUDITED W31/R4 round 2: exact block-linear solve on "
                      "the doubled-GHZ deformation. Exact rationals only. A "
                      "failed construction is NOT an impossibility proof.",
           "_pinned_head": open(os.path.join(HERE,
                                             "PINNED_HEAD.txt")).read().strip()}

    def ck():
        with open(OUT_F, "w") as fh:
            json.dump(OUT, fh, indent=1, sort_keys=True)

    rng = random.Random(20260820)

    # ---- S2 / S4 : the linearity claim ------------------------------------
    S8 = Sys(8, C8_MEMBER)
    val = {s: Fraction(rng.randint(1, 9)) for s in
           [(e, i, j) for e in S8.E for (i, j) in cells_of(S8.T[S8.ei[e]])]}
    e0 = S8.E[3]
    cs, rows, consts = S8.lin(val, e0)
    mism = 0
    for k, w in enumerate(S8.mixed[:200]):
        lhs = consts[k] + sum(rows[k][c] * val[(e0, c[0], c[1])] for c in cs)
        if lhs != S8.H(val, w):
            mism += 1
    OUT["S2_linearity_mismatches"] = mism
    bad = dict(rows[0])
    bad[cs[0]] += 1
    OUT["S4_mutation_fires"] = (
        consts[0] + sum(bad[c] * val[(e0, c[0], c[1])] for c in cs)
        != S8.H(val, S8.mixed[0]))
    ck()
    print("[S2] linearity mismatches:", mism, " [S4] mutation fires:",
          OUT["S4_mutation_fires"], flush=True)

    # ---- S1 : positive calibration at N = 4 -------------------------------
    S4s = Sys(4, [FULL] * 6)
    v4 = {s: Fraction(rng.randint(1, 5)) for s in
          [(e, i, j) for e in S4s.E for (i, j) in cells_of(FULL)]}
    r4, _ = solve_lane(S4s, v4, 180, rng, "S1_N4_positive_control", ck)
    OUT["S1_N4"] = r4
    ck()
    print("[S1] N=4 calibration:", r4["status"], r4["best_satisfied"], "/",
          r4["n_mixed"], flush=True)
    if not r4["found_exact_source"]:
        OUT["S1_WARNING"] = ("the solver did not find an exact source at N=4 "
                             "within budget; the C_8 run below is descriptive "
                             "only and is NOT evidence about the stratum.")
        print("[S1] WARNING:", OUT["S1_WARNING"], flush=True)
    ck()

    # ---- the doubled-GHZ deformation on the C_8 member --------------------
    # hold the twelve within-half single cells at 1; solve over the 144 cross
    # cells.
    v8 = {}
    for e in S8.E:
        for (i, j) in cells_of(S8.T[S8.ei[e]]):
            inside = (e[0] < 4) == (e[1] < 4)
            v8[(e, i, j)] = Fraction(1) if inside else \
                Fraction(rng.randint(1, 9))
    OUT["ansatz"] = ("twelve within-half GHZ single cells pinned to 1; "
                     "solving over the 144 cross cells")
    r8, _ = solve_lane(S8, v8, 2400, rng, "C8_doubled_GHZ_deformation", ck)
    OUT["C8"] = r8
    OUT["SUMMARY"] = dict(n_mixed=r8["n_mixed"],
                          best=r8["best_satisfied"],
                          found=r8["found_exact_source"],
                          calibrated=r4["found_exact_source"],
                          honest_note="not found in budget != does not exist")
    ck()
    print("[C8]", r8["status"], r8["best_satisfied"], "/", r8["n_mixed"],
          flush=True)
    declared = ["S1_N4", "S2_linearity_mismatches", "S4_mutation_fires", "C8"]
    missing = [d for d in declared if d not in OUT]
    assert not missing, "CONTROL NEVER RAN: %s" % missing
    print("control manifest OK:", declared, flush=True)


if __name__ == "__main__":
    main()
