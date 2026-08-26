#!/usr/bin/env python3
"""UNAUDITED PROBE (W4 / Route F.1) -- the NON-generic mode: when the error span
properly drops below W, in Pfaffian coordinates.

Pinned HEAD: 26ba69f7e643694c6a58464af6e9e1de9ec92f01

Motivated by W2's calibration warning: "kappa_c^2 blocks iff the span fills W"
is the generic (vacuous) mode.  The structural content is the drop.  In the
xi/Gram picture the drop has an exact and purely block-theoretic description.

THE BOUND.  With P_x = column space of A_{p|x} and Q_x = column space of
A_{q|x} (both inside C^3), and P = sum_x P_x, Q = sum_x Q_x,

    span{E_w} =  image of  mu_pq : Xi_a (x) .. (x) Xi_d -> Sym^2 V_p (x) Sym^2 V_q
              subset  sum_{T={x,z}} (P_x . P_z) (x) (Q_y . Q_w)         (B1)
              subset  Sym^2 P (x) Sym^2 Q.                              (B2)

Consequence (a NECESSARY condition for kappa_c^2 blocking, not vacuous):

    kappa_c^2 = e_c^2 (x) e_c^2  in span   =>   e_c in P  and  e_c in Q,     (N)

i.e. the colour-c axis must be hit by the columns of the p-blocks AND of the
q-blocks at the four deleted sites.

THE COORDINATE REGIME (W2's R_cell: at most one cell per block).  Write the
single cell of the block (p,x) as (i_x, j_x) (row = colour at p) and of (q,x)
as (k_x, l_x).  Then Xi_x = {(a e_{i_x}, b e_{k_x})} and

    E(eta) = sum_{T={x,z}} a_x a_z b_y b_w (e_{i_x} e_{i_z}) (x) (e_{k_y} e_{k_w}),

so the span is spanned by at most SIX Segre-Veronese monomials, one per
2-subset T of U -- exactly W2's observed span range 1..6.  Hence

    kappa_c^2 blocks  <=>  some 2-subset T = {x,z} of U has
                           i_x = i_z = c   and   k_y = k_w = c
                           for the complementary pair {y,w} = T^c
                           (with the surviving coefficient nonzero).      (C)

(C) is a SUPPORT condition on the cell pattern, not a rank condition -- the
shape J.2 consumes.  Both (N) and (C) are verified exactly below.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.abspath(os.path.join(
    HERE, "..", "unaudited-witness-splitting-p2-2026-08-15")))

from wsplit_core import (KAPPA_VARS, PAIRS, Source, lin_zero, lin_mul,
                         matrix_rank, quad_vector, in_row_space, require)
from translate import PfaffFrame, RANGE3, rank_of, solve_in_span
from payoff import m2star, intersect_with_dc

SITES = tuple(range(6))


# ------------------------------------------------------------ generators

def rcell_source(rng, allow_zero=False):
    """R_cell: at most one cell per aggregate block."""
    blocks, cells = {}, {}
    for pair in PAIRS:
        matrix = [[Fraction(0)] * 3 for _ in range(3)]
        if allow_zero and rng.random() < 0.15:
            blocks[pair] = matrix
            cells[pair] = None
            continue
        i, j = rng.randrange(3), rng.randrange(3)
        matrix[i][j] = Fraction(rng.choice([1, 2, -1, 3, -2]))
        blocks[pair] = matrix
        cells[pair] = (i, j)
    return Source(blocks), cells


def rmon_source(rng):
    """R_mon: every block a monomial (partial injection) matrix."""
    blocks = {}
    for pair in PAIRS:
        matrix = [[Fraction(0)] * 3 for _ in range(3)]
        columns = list(range(3))
        rng.shuffle(columns)
        for i in range(3):
            if rng.random() < 0.7:
                matrix[i][columns[i]] = Fraction(rng.choice([1, 2, -1, 3]))
        blocks[pair] = matrix
    return Source(blocks)


def sparse_rank_source(rng):
    """Rank-one blocks with sparse factors (the noncoordinate rank-one end)."""
    blocks = {}
    for pair in PAIRS:
        left = [Fraction(0)] * 3
        right = [Fraction(0)] * 3
        for vector in (left, right):
            for index in rng.sample(range(3), rng.choice([1, 1, 2])):
                vector[index] = Fraction(rng.choice([1, 2, -1]))
        blocks[pair] = [[left[i] * right[j] for j in range(3)]
                        for i in range(3)]
    return Source(blocks)


# ---------------------------------------------------------------- bounds

def column_space(matrix):
    columns = [[matrix[i][j] for i in RANGE3] for j in RANGE3]
    return [c for c in columns if any(c)]


def subspace_dim(vectors):
    return rank_of(vectors) if vectors else 0


def sym2_basis_dim(vectors):
    """dim Sym^2 of the span of `vectors` inside Sym^2 C^3."""
    return {0: 0, 1: 1, 2: 3, 3: 6}[subspace_dim(vectors)]


def in_span_of(vectors, target):
    if not vectors:
        return not any(target)
    return solve_in_span(vectors, target)


def axis(colour):
    vector = [Fraction(0)] * 3
    vector[colour] = Fraction(1)
    return vector


# ------------------------------------------------------------ the checks

def check_necessary(frame: PfaffFrame, source: Source):
    """(N): kappa_c^2 in span => e_c in P and e_c in Q."""
    p, q = frame.p, frame.q
    P, Q = [], []
    for x in frame.U:
        P.extend(column_space(source.oriented(p, x)))
        Q.extend(column_space(source.oriented(q, x)))
    out = []
    for colour in RANGE3:
        blocks = frame.in_span(frame.kappa_square(colour))
        necessary = (in_span_of(P, axis(colour))
                     and in_span_of(Q, axis(colour)))
        out.append({"colour": colour, "blocks": blocks,
                    "necessary": necessary,
                    "violation": blocks and not necessary})
    return out, subspace_dim(P), subspace_dim(Q)


def check_rcell(frame: PfaffFrame, cells, source: Source):
    """(C): the explicit six-monomial span and the support criterion."""
    p, q = frame.p, frame.q
    rows_p, rows_q = {}, {}
    for x in frame.U:
        cell_p = cells[(min(p, x), max(p, x))]
        cell_q = cells[(min(q, x), max(q, x))]
        if cell_p is None or cell_q is None:
            return None
        rows_p[x] = cell_p[0] if p < x else cell_p[1]
        rows_q[x] = cell_q[0] if q < x else cell_q[1]
    monomials = []
    for T in combinations(frame.U, 2):
        rest = tuple(x for x in frame.U if x not in T)
        monomials.append((tuple(sorted((rows_p[T[0]], rows_p[T[1]]))),
                          tuple(sorted((rows_q[rest[0]], rows_q[rest[1]])))))
    distinct = len(set(monomials))
    predicted = []
    for colour in RANGE3:
        target = ((colour, colour), (colour, colour))
        predicted.append(target in monomials)
    observed = [frame.in_span(frame.kappa_square(colour))
                for colour in RANGE3]
    return {"span": frame.span, "distinct_monomials": distinct,
            "monomials": monomials, "predicted": predicted,
            "observed": observed,
            "span_le_6": frame.span <= 6,
            "span_matches": frame.span <= distinct,
            "criterion_ok": all(a == b for a, b in zip(predicted, observed))}


def main():
    print("UNAUDITED PROBE (W4, Route F.1) -- the non-generic mode")
    print("pinned HEAD 26ba69f7e643694c6a58464af6e9e1de9ec92f01")
    print()
    rng = random.Random(90210)
    report = {}

    # ---- (N) the necessary condition, across regimes -------------------
    print("(N)  kappa_c^2 in span  =>  e_c in P and e_c in Q")
    stats = {}
    for name, generator, trials in (
            ("R_cell", lambda r: rcell_source(r)[0], 20),
            ("R_mon", rmon_source, 20),
            ("sparse rank-one", sparse_rank_source, 20)):
        violations = tested = blocks = 0
        pdims = {}
        for _ in range(trials):
            source = generator(rng)
            for p, q in PAIRS:
                frame = PfaffFrame(source, p, q)
                rows, dp, dq = check_necessary(frame, source)
                pdims[(dp, dq)] = pdims.get((dp, dq), 0) + 1
                for row in rows:
                    tested += 1
                    blocks += row["blocks"]
                    violations += row["violation"]
        stats[name] = {"tested": tested, "blocking": blocks,
                       "violations": violations,
                       "PQ_dims": {str(k): v for k, v in pdims.items()}}
        print("   %-16s %5d colour-instances, %4d blocking, %d violations"
              % (name, tested, blocks, violations))
    report["necessary"] = stats

    # ---- (C) the coordinate-regime support criterion --------------------
    print()
    print("(C)  R_cell: span is spanned by at most six Segre-Veronese")
    print("     monomials, and kappa_c^2 blocks iff a 2+2 split of U carries")
    print("     colour c on both sides")
    print("     (the coefficients a_x, b_x are FREE exactly when every Xi_x is")
    print("      2-dimensional, i.e. the p-block and the q-block at x use")
    print("      different column colours; then (C) is an equivalence.)")
    total = span_ok = 0
    free = {"pairs": 0, "criterion_ok": 0, "span_exact": 0}
    tied = {"pairs": 0, "criterion_ok": 0, "span_exact": 0}
    span_hist = {}
    for _ in range(40):
        source, cells = rcell_source(rng)
        for p, q in PAIRS:
            frame = PfaffFrame(source, p, q)
            result = check_rcell(frame, cells, source)
            if result is None:
                continue
            total += 1
            span_ok += result["span_matches"]
            span_hist[result["span"]] = span_hist.get(result["span"], 0) + 1
            bucket = (free if all(frame.Xi_rank[x] == 2 for x in frame.U)
                      else tied)
            bucket["pairs"] += 1
            bucket["criterion_ok"] += result["criterion_ok"]
            bucket["span_exact"] += (result["span"]
                                     == result["distinct_monomials"])
    print("   pairs tested                     :", total)
    print("   span <= #distinct monomials      : %d/%d" % (span_ok, total))
    print("   span histogram                   :",
          dict(sorted(span_hist.items())))
    print("   FREE  (every Xi_x 2-dimensional) : %d pairs;"
          " (C) exact %d; span = #distinct monomials %d"
          % (free["pairs"], free["criterion_ok"], free["span_exact"]))
    print("   TIED  (some Xi_x 1-dimensional)  : %d pairs;"
          " (C) holds %d  -- here (C) is only NECESSARY"
          % (tied["pairs"], tied["criterion_ok"]))
    report["rcell"] = {"pairs": total, "span_bound_ok": span_ok,
                       "free": free, "tied": tied,
                       "span_hist": {str(k): v for k, v in span_hist.items()}}

    # ---- where the proper subspan lives --------------------------------
    print()
    print("proper subspan census: pairs with 0 < span < 36 carrying kappa_c^2")
    census = {}
    for name, generator, trials in (
            ("R_cell", lambda r: rcell_source(r)[0], 25),
            ("R_mon", rmon_source, 25),
            ("sparse rank-one", sparse_rank_source, 25)):
        rows = []
        for _ in range(trials):
            source = generator(rng)
            for p, q in PAIRS:
                frame = PfaffFrame(source, p, q)
                if not (0 < frame.span < 36):
                    continue
                for colour in RANGE3:
                    if frame.in_span(frame.kappa_square(colour)):
                        reach, _forced = m2star(frame, colour)
                        rows.append({"span": frame.span, "m2star": reach})
        census[name] = {
            "proper_subspan_blocking": len(rows),
            "explained_by_M2star": sum(1 for r in rows if r["m2star"]),
            "span_hist": {}}
        for r in rows:
            census[name]["span_hist"][str(r["span"])] = \
                census[name]["span_hist"].get(str(r["span"]), 0) + 1
        print("   %-16s %4d proper-subspan blockings, %4d explained by M2*"
              % (name, len(rows), census[name]["explained_by_M2star"]))
        print("      span histogram:",
              dict(sorted(census[name]["span_hist"].items(),
                          key=lambda kv: int(kv[0]))))
    report["proper_subspan"] = census

    with open("results_nongeneric.json", "w") as handle:
        json.dump(report, handle, indent=1, default=str)
    print()
    print("wrote results_nongeneric.json")


if __name__ == "__main__":
    main()
