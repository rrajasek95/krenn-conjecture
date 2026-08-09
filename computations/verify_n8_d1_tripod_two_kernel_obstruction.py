#!/usr/bin/env python3
"""Exact tripod lemma: two fully projected syzygies forbid a pure slice."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


EXPECTED_LEDGER_SHA256 = (
    "56685443cf11a8657f2674b4b3af8cd91644ab8609ea33734173ce65c9683dd9"
)


def relation_matrix():
    """Matrix for e_s F + e_s E + e_s D = 0, s=0,1."""
    names = (["D%d%d" % (i, j) for i in range(3) for j in range(3)]
             + ["E%d%d" % (i, k) for i in range(3) for k in range(3)]
             + ["F%d%d" % (j, k) for j in range(3) for k in range(3)])
    index = {name: position for position, name in enumerate(names)}
    rows = []
    for s, i, j, k in itertools.product(range(2), range(3), range(3), range(3)):
        row = [0] * len(names)
        if i == s:
            row[index["F%d%d" % (j, k)]] += 1
        if j == s:
            row[index["E%d%d" % (i, k)]] += 1
        if k == s:
            row[index["D%d%d" % (i, j)]] += 1
        rows.append(row)
    return names, rows


def unit_pivot_rank(matrix):
    """Fraction-free elimination, recording a unit pivot in every column used."""
    rows = [list(row) for row in matrix]
    pivot_row = 0
    pivot_columns = []
    for column in range(len(rows[0])):
        selected = next((row for row in range(pivot_row, len(rows))
                         if abs(rows[row][column]) == 1), None)
        if selected is None:
            require(not any(rows[row][column]
                            for row in range(pivot_row, len(rows))),
                    "a nonunit pivot appeared in the tripod elimination")
            continue
        rows[pivot_row], rows[selected] = rows[selected], rows[pivot_row]
        if rows[pivot_row][column] == -1:
            rows[pivot_row] = [-value for value in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or not rows[row][column]:
                continue
            factor = rows[row][column]
            rows[row] = [left - factor * right
                         for left, right in zip(rows[row], rows[pivot_row])]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivot_columns, rows


def audit_syzygy_kernel():
    names, matrix = relation_matrix()
    pivots, reduced = unit_pivot_rank(matrix)
    require(len(matrix) == 54 and len(names) == 27 and len(pivots) == 26,
            "the two-syzygy tripod rank changed")

    candidate = Counter({
        "D01": -1, "D10": 1,
        "E01": 1, "E10": -1,
        "F01": -1, "F10": 1,
    })
    vector = [candidate[name] for name in names]
    require(all(sum(coefficient * value
                    for coefficient, value in zip(row, vector)) == 0
                for row in matrix),
            "the alternating tripod generator left the kernel")
    require(any(vector) and len(pivots) + 1 == len(names),
            "the alternating generator no longer spans the kernel")
    return {
        "equations": len(matrix),
        "unknown_matrix_entries": len(names),
        "unit_pivot_rank": len(pivots),
        "kernel_dimension": 1,
        "pivot_columns": [names[column] for column in pivots],
        "kernel_generator": dict(sorted(candidate.items())),
        "reduced_matrix_sha256": hashlib.sha256(
            json.dumps(reduced, separators=(",", ":")).encode()
        ).hexdigest(),
    }


def linear_add(*terms):
    out = Counter()
    for term in terms:
        out.update(term)
    return {name: coefficient for name, coefficient in out.items()
            if coefficient}


def linear_var(name, coefficient=1):
    return {} if not coefficient else {name: coefficient}


def audit_companion_cube():
    """The arbitrary companion slice has the same forbidden cube ledger."""
    a = [linear_var("a0"), linear_var("a1")]
    b = [linear_var("b0"), linear_var("b1")]
    c = [linear_var("c0"), linear_var("c1")]
    D = ((0, -1), (1, 0))
    E = ((0, 1), (-1, 0))
    F = ((0, -1), (1, 0))
    cube = {}
    for i, j, k in itertools.product(range(2), repeat=3):
        cube[(i, j, k)] = linear_add(
            {name: F[j][k] * coefficient
             for name, coefficient in a[i].items()},
            {name: E[i][k] * coefficient
             for name, coefficient in b[j].items()},
            {name: D[i][j] * coefficient
             for name, coefficient in c[k].items()},
        )
    require(not cube[(0, 0, 0)] and not cube[(1, 1, 1)],
            "the alternating companion lost its zero opposite corners")
    for weight in (1, 2):
        total = linear_add(*(value for word, value in cube.items()
                             if sum(word) == weight))
        require(not total,
                "the alternating companion lost a zero middle-layer sum")
    expected = {
        "000": {}, "001": {"a0": -1, "b0": 1},
        "010": {"a0": 1, "c0": -1},
        "011": {"b1": 1, "c1": -1},
        "100": {"b0": -1, "c0": 1},
        "101": {"a1": -1, "c1": 1},
        "110": {"a1": 1, "b1": -1}, "111": {},
    }
    actual = {"".join(map(str, word)): value
              for word, value in sorted(cube.items())}
    require(actual == expected, "the alternating companion cube changed")
    return actual


def audit_pure_cube_support():
    cases = []
    for zero_at_zero in range(3):
        for zero_at_one in range(3):
            if zero_at_zero == zero_at_one:
                continue
            support = [word for word in itertools.product(range(2), repeat=3)
                       if word[zero_at_zero] and not word[zero_at_one]]
            counts = Counter(map(sum, support))
            require(len(support) == 2 and counts == {1: 1, 2: 1},
                    "the decomposable-cube support edge changed")
            cases.append({
                "zero_at_000_factor": zero_at_zero,
                "zero_at_111_factor": zero_at_one,
                "possible_support": [list(word) for word in support],
            })
    require(len(cases) == 6, "the pure-cube support census changed")
    return cases


def audit():
    ledger = {
        "two_syzygy_kernel": audit_syzygy_kernel(),
        "companion_cube": audit_companion_cube(),
        "pure_cube_support_cases": audit_pure_cube_support(),
        "theorem": (
            "Let X,Y,Z be three-dimensional vector spaces over a field. "
            "If the tripod map (x,y,z)->x tensor F+y tensor E+z tensor D "
            "contains a two-plane in its kernel whose three coordinate "
            "projections are injective, then no further tripod slice is a "
            "nonzero decomposable tensor."
        ),
        "proof": (
            "Normalize the three injective projections of a common K^2 to "
            "the first two coordinate vectors. The 54 relation coordinates "
            "have field-independent rank 26, so D,E,F are the unique common "
            "alternating two-forms up to scale. Projection to the three "
            "one-dimensional complements forces any alleged decomposable "
            "companion and its three slice vectors back into those planes. "
            "Its 2x2x2 cube then has zero opposite corners and zero weight-one "
            "and weight-two layer sums. A nonzero decomposable cube with the "
            "two corner zeros is supported on one complementary edge, whose "
            "two entries are killed by the two layer sums."
        ),
        "characteristic_scope": "every field",
        "status": "injective two-kernel residue tripod cannot carry the pure target slice",
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the tripod two-kernel ledger changed")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("n8 D1 tripod two-kernel obstruction: PASS (exact)")
    print("unit-pivot rank:",
          ledger["two_syzygy_kernel"]["unit_pivot_rank"], "/ 27")
    print("scope:", ledger["characteristic_scope"])
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
