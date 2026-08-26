#!/usr/bin/env python3
"""UNAUDITED PROBE (W2) -- the regime definition and its forcing chain (task A).

Pinned HEAD: 26ba69f7e643694c6a58464af6e9e1de9ec92f01

PART 1 (exact, exhaustive).  P2's FACT 2 says which degree-2 splitting
patterns can lie in W = Sym^2 (x) Sym^2:

    kappa_c kappa_c'  (c != c')  never;
    s^2                          iff rank A_pq <= 1;
    s kappa_c                    iff A_pq is supported in row c U column c;
    kappa_c^2                    always (no condition on the source).

This script derives, exhaustively over all 512 zero/one supports of a 3x3
block and over random values, the CONSEQUENCE OF COMBINED patterns -- the
step P2 did not take, and the step that turns blocking into the coordinate
regime:

    cross(c) := row c U column c.
    cross(c) ^ cross(c')            = {(c,c'), (c',c)}          (c != c')
    cross(c) ^ cross(c') ^ cross(c'') = empty                   (distinct)
    rank <= 1 and support in cross(c)  =>  A = u (x) e_c or e_c (x) v.
    rank <= 1 and support in cross(c) ^ cross(c') => A is ONE coordinate cell.

PART 2 (data mining).  What does kappa_c^2-blocking correlate with?  P2's
runs a (generic), b (census strata) and b2 (anchored coordinate strata)
record, per live pair, the pattern list and the witness verdict.  We join
those against the block structure of the pair recomputed from the stored
sources where available, and otherwise report the pattern co-occurrence
statistics that decide whether kappa_c^2 carries structural information.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import product
import json
import os
import sys

P2 = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-witness-splitting-p2-2026-08-15"
sys.path.insert(0, P2)

from wsplit_core import (KAPPA_VARS, in_sym_square, lin_mul,  # noqa: E402
                         lin_zero, matrix_rank)


def s_form(matrix):
    return [matrix[i][j] for i in range(3) for j in range(3)]


def kappa_form(colour):
    form = lin_zero()
    form[KAPPA_VARS[colour]] = Fraction(1)
    return form


def cross(colour):
    return {(i, j) for i in range(3) for j in range(3)
            if i == colour or j == colour}


def structure_class(matrix):
    """Classify a 3x3 block for the regime vocabulary."""
    cells = [(i, j) for i in range(3) for j in range(3) if matrix[i][j]]
    rank = matrix_rank(matrix)
    if not cells:
        return "zero"
    rows = {i for i, _ in cells}
    columns = {j for _, j in cells}
    if len(cells) == 1:
        return "coordinate-cell"
    if rank == 1 and len(rows) == 1:
        return "coordinate-row"       # e_a (x) v, v noncoordinate
    if rank == 1 and len(columns) == 1:
        return "coordinate-column"    # u (x) e_b, u noncoordinate
    if rank == 1:
        return "rank1-noncoordinate"
    if len(rows) == len(cells) and len(columns) == len(cells):
        return "monomial-matrix"      # partial permutation pattern, rank >= 2
    return f"rank{rank}-general"


def part1_exhaustive():
    """All 512 supports x sign patterns: verify the combined-pattern chain."""
    results = Counter()
    witnesses = {}
    for support in product((0, 1), repeat=9):
        matrix = [[Fraction(support[3 * i + j]) for j in range(3)]
                  for i in range(3)]
        s = s_form(matrix)
        rank = matrix_rank(matrix)
        cells = {(i, j) for i in range(3) for j in range(3) if support[3 * i + j]}
        ss = in_sym_square(lin_mul(s, s)) if any(s) else None
        skappa = {c: in_sym_square(lin_mul(s, kappa_form(c)))
                  for c in range(3)} if any(s) else {}
        # Claim A: s*kappa_c in W  <=>  cells subset cross(c).
        for c in range(3):
            if not any(s):
                continue
            assert skappa[c] == cells.issubset(cross(c)), (support, c)
        # Claim B: s^2 in W <=> rank <= 1.
        if any(s):
            assert ss == (rank <= 1), support
        # Claim C: two distinct s*kappa  =>  cells subset {(c,c'),(c',c)}.
        live = [c for c in range(3) if skappa.get(c)]
        if len(live) >= 2:
            c, d = live[0], live[1]
            assert cells.issubset({(c, d), (d, c)}), (support, live)
        if len(live) >= 3:
            assert not cells, support
        # Claim D: s^2 and one s*kappa_c  =>  coordinate row or column.
        if any(s) and ss and len(live) >= 1:
            klass = structure_class(matrix)
            assert klass in ("coordinate-cell", "coordinate-row",
                             "coordinate-column"), (support, klass)
            witnesses.setdefault(("s2+skappa", klass), support)
        # Claim E: s^2 and two s*kappa  =>  one coordinate cell.
        if any(s) and ss and len(live) >= 2:
            assert structure_class(matrix) == "coordinate-cell", support
        key = (bool(ss), len(live), structure_class(matrix))
        results[key] += 1
    return {"classes": {str(k): v for k, v in sorted(results.items(),
                                                     key=lambda kv: str(kv[0]))},
            "claims": ["A: s*kappa_c in W <=> support in cross(c)",
                       "B: s^2 in W <=> rank <= 1",
                       "C: s*kappa_c and s*kappa_c' (c != c') => support in "
                       "{(c,c'),(c',c)}; three colours => block is zero",
                       "D: s^2 and s*kappa_c => A = e_c (x) v or u (x) e_c",
                       "E: s^2 and two s*kappa => A is one coordinate cell"],
            "status": "all claims verified exhaustively over 512 supports"}


def part1_values(trials=2000, seed=7):
    """Random rational values: the support-level claims are value-independent."""
    import random
    from wsplit_core import random_rank_matrix
    rng = random.Random(seed)
    checked = 0
    for _ in range(trials):
        rank = rng.choice([0, 1, 1, 2, 3])
        matrix = random_rank_matrix(rng, rank)
        s = s_form(matrix)
        if not any(s):
            continue
        cells = {(i, j) for i in range(3) for j in range(3) if matrix[i][j]}
        assert in_sym_square(lin_mul(s, s)) == (matrix_rank(matrix) <= 1)
        live = []
        for c in range(3):
            value = in_sym_square(lin_mul(s, kappa_form(c)))
            assert value == cells.issubset(cross(c))
            if value:
                live.append(c)
        if in_sym_square(lin_mul(s, s)) and len(live) >= 2:
            assert structure_class(matrix) == "coordinate-cell"
        checked += 1
    return checked


def load(name):
    path = os.path.join(P2, name)
    with open(path) as handle:
        return json.load(handle)


def part2_pattern_statistics():
    """Pattern co-occurrence over every recorded live pair of P2's runs."""
    out = {}
    for name, key in (("results_a.json", "a-generic"),
                      ("results_b.json", "b-strata-generic"),
                      ("results_b2.json", "b2-anchored-coordinate")):
        try:
            blob = load(name)
        except (FileNotFoundError, json.JSONDecodeError):
            continue
        rows = blob.get("results", blob)
        if isinstance(rows, dict):
            rows = rows.get("results", [])
        pattern_counter = Counter()
        joint = Counter()
        status_by_pattern = Counter()
        for row in rows:
            for record in row.get("pairs", []):
                if record.get("status") == "dead":
                    continue
                patterns = tuple(sorted(record.get("patterns") or []))
                pattern_counter[patterns] += 1
                kinds = set()
                for pattern in patterns:
                    left, right = pattern.split("*")
                    if left == "s" and right == "s":
                        kinds.add("s2")
                    elif left == "s" or right == "s":
                        kinds.add("s*kappa")
                    elif left == right:
                        kinds.add("kappa2")
                    else:
                        kinds.add("kappa*kappa'")
                joint[(tuple(sorted(kinds)), record.get("witness"))] += 1
                status_by_pattern[(tuple(sorted(kinds)),
                                   record.get("status"))] += 1
        out[key] = {
            "live_pairs": sum(pattern_counter.values()),
            "top_pattern_sets": {str(k): v for k, v
                                 in pattern_counter.most_common(12)},
            "kind_by_witness": {str(k): v for k, v in sorted(joint.items(),
                                                            key=lambda kv: -kv[1])},
            "kind_by_status": {str(k): v for k, v
                               in sorted(status_by_pattern.items(),
                                         key=lambda kv: -kv[1])[:20]},
        }
    return out


def main():
    print("UNAUDITED PROBE (W2) -- regime forcing chain, HEAD 26ba69f",
          flush=True)
    report = {"part1": part1_exhaustive()}
    report["part1"]["random_value_checks"] = part1_values()
    print(json.dumps(report["part1"], indent=1), flush=True)
    report["part2"] = part2_pattern_statistics()
    print(json.dumps(report["part2"], indent=1)[:4000], flush=True)
    with open("regime.json", "w") as handle:
        json.dump(report, handle, indent=1)


if __name__ == "__main__":
    main()
