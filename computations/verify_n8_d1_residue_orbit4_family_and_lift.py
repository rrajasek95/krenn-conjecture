#!/usr/bin/env python3
"""Exact residue family and pure-fibre lift frontier for maximal orbit O4."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import hashlib
import importlib
import itertools
import os
import sys
from time import monotonic

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED_CANDIDATE_SHA256 = (
    "28b5de217d61dbe41c699657fb7ad3d7f29d0a42521a2e9b99926d135cf8b8ca"
)
SOURCE = os.path.join(HERE, "verify_n8_d1_m10_334_branch63_candidate.py")
with open(SOURCE, "rb") as handle:
    require(hashlib.sha256(handle.read()).hexdigest()
            == PINNED_CANDIDATE_SHA256,
            "the pinned D1 candidate source changed")
C = importlib.import_module("verify_n8_d1_m10_334_branch63_candidate")
D, V = C.D, C.V

RESIDUE_HOLES = frozenset({
    (4, 7, 0, 0), (4, 7, 0, 1), (4, 7, 1, 0), (4, 7, 1, 1),
    (4, 7, 2, 0), (4, 7, 2, 1),
    (5, 7, 0, 0), (5, 7, 0, 1), (5, 7, 1, 0), (5, 7, 1, 1),
    (5, 7, 2, 0), (5, 7, 2, 1),
    (6, 7, 0, 0), (6, 7, 0, 1), (6, 7, 0, 2),
    (6, 7, 1, 0), (6, 7, 1, 1), (6, 7, 1, 2),
    (6, 7, 2, 0), (6, 7, 2, 1),
})
LIFT_RECORDS = {
    4144: "x_02_20",
    4738: "x_02_21",
    6815: "x_13_20",
    6842: "x_13_21",
}
EXPECTED_LEDGER_SHA256 = (
    "b7826813c8dcd00eb86739e2c9a6e7428eeab4d0d6c1df266763dccdad785c28"
)


def var(name):
    return D.p_var(name)


def vector_scale(scalar, vector):
    return tuple(D.p_mul(scalar, entry) for entry in vector)


def outer(left, right):
    return tuple(tuple(D.p_mul(a, b) for b in right) for a in left)


def matrix_add(*matrices):
    zero = D.p_const(0)
    out = tuple(tuple(zero for _ in range(3)) for _ in range(3))
    for matrix in matrices:
        out = tuple(tuple(D.p_add(a, b) for a, b in zip(left, right))
                    for left, right in zip(out, matrix))
    return out


def symbolic_family_audit():
    c = tuple(var("c%d" % index) for index in range(3))
    e = tuple(var("e%d" % index) for index in range(3))
    b2 = tuple(var("b%d" % index) for index in range(3))
    d2 = tuple(var("d%d" % index) for index in range(3))
    alpha = (var("alpha0"), var("alpha1"))
    zero, one = D.p_const(0), D.p_const(1)
    target_matrix = tuple(tuple(one if (i, j) == (2, 2) else zero
                                 for j in range(3)) for i in range(3))
    A = matrix_add(target_matrix,
                   tuple(tuple(D.p_neg(entry) for entry in row)
                         for row in outer(b2, e)),
                   tuple(tuple(D.p_neg(entry) for entry in row)
                         for row in outer(c, d2)))
    B = tuple(tuple((vector_scale(alpha[column], c)[row]
                     if column < 2 else b2[row])
                    for column in range(3)) for row in range(3))
    C47 = tuple(tuple(c[row] if column == 2 else zero
                      for column in range(3)) for row in range(3))
    D56 = tuple(tuple((vector_scale(D.p_neg(alpha[column]), e)[row]
                       if column < 2 else d2[row])
                      for column in range(3)) for row in range(3))
    E57 = tuple(tuple(e[row] if column == 2 else zero
                      for column in range(3)) for row in range(3))
    F67 = tuple(tuple(one if (row, column) == (2, 2) else zero
                      for column in range(3)) for row in range(3))
    blocks = {(4, 5): A, (4, 6): B, (4, 7): C47,
              (5, 6): D56, (5, 7): E57, (6, 7): F67}
    nonzero = 0
    coefficient_hashes = []
    for colours in itertools.product(V.COLORS, repeat=4):
        word = dict(zip(V.RESIDUE, colours))
        value = D.p_const(0)
        for matching in V.MATCHINGS[V.RESIDUE]:
            term = D.p_const(1)
            for u, v in matching:
                term = D.p_mul(term, blocks[(u, v)][word[u]][word[v]])
            value = D.p_add(value, term)
        expected = one if colours == (2, 2, 2, 2) else zero
        require(value == expected,
                "the orbit-O4 residue family failed word %s" % (colours,))
        nonzero += bool(value)
        coefficient_hashes.append(D.content_hash([
            [list(monomial), str(coefficient)]
            for monomial, coefficient in sorted(value.items())
        ]))
    require(nonzero == 1, "the O4 residue family coefficient census changed")
    return {
        "gauge": "F67_22=1",
        "parameters": 14,
        "C47": "c tensor e2",
        "E57": "e tensor e2",
        "F67": "e2 tensor e2",
        "B46_columns": ["alpha0*c", "alpha1*c", "b"],
        "D56_columns": ["-alpha0*e", "-alpha1*e", "d"],
        "A45": "E22-b tensor e-c tensor d",
        "coefficients_checked": len(coefficient_hashes),
        "coefficient_trace_sha256": D.content_hash(coefficient_hashes),
    }


def explicit_point_audit():
    values = {}
    c, e = (1, 1, 1), (1, 1, 1)
    b, d = (1, 2, 3), (4, 5, 6)
    for i, j in itertools.product(range(3), repeat=2):
        values[(4, 5, i, j)] = Fraction(
            (1 if (i, j) == (2, 2) else 0) - b[i] - d[j]
        )
    for i in range(3):
        values[(4, 6, i, 0)] = Fraction(c[i])
        values[(4, 6, i, 1)] = Fraction(c[i])
        values[(4, 6, i, 2)] = Fraction(b[i])
        values[(4, 7, i, 2)] = Fraction(c[i])
    for j in range(3):
        values[(5, 6, j, 0)] = Fraction(-e[j])
        values[(5, 6, j, 1)] = Fraction(-e[j])
        values[(5, 6, j, 2)] = Fraction(d[j])
        values[(5, 7, j, 2)] = Fraction(e[j])
    values[(6, 7, 2, 2)] = Fraction(1)
    require(len(values) == 34 and all(values.values())
            and values[(4, 5, 2, 2)] == -8,
            "the O4 rational residue point changed")
    histogram = Counter()
    for colours in itertools.product(V.COLORS, repeat=4):
        word = dict(zip(V.RESIDUE, colours))
        coefficient = Fraction(0)
        for matching in V.MATCHINGS[V.RESIDUE]:
            term = Fraction(1)
            for u, v in matching:
                term *= values.get(V.cell(u, v, word[u], word[v]), 0)
            coefficient += term
        expected = Fraction(1 if colours == (2, 2, 2, 2) else 0)
        require(coefficient == expected,
                "the O4 rational point failed word %s" % (colours,))
        histogram[str(coefficient)] += 1
    return {
        "localized_coordinates": len(values),
        "point": [[list(cell), str(value)]
                  for cell, value in sorted(values.items())],
        "coefficient_histogram": dict(sorted(histogram.items())),
    }


def full_frontier_audit():
    _state, _extras, _base_support, admissible, _stats = C.candidate_input()
    support = set(admissible) - set(RESIDUE_HOLES)
    require(len(admissible) == 217 and len(support) == 197,
            "the maximal O4 full-support frontier changed")
    shadow = C.support_shadow_audit(support)
    records = C.coefficient_generators(support)
    histogram = Counter(len(record["terms"]) for record in records)
    require(len(records) == 7237 and not histogram[1]
            and D.content_hash(records)
            == "10bcf6a8aae8028d7dcad5e7cca6cfd3df44070abd28d7964fd30d95d6dd2fd3",
            "the O4 full coefficient input changed")

    residue_terms = [
        ["x_45_22", "x_67_22"],
        ["x_46_22", "x_57_22"],
        ["x_47_22", "x_56_22"],
    ]
    for record_index, factor in LIFT_RECORDS.items():
        record = records[record_index]
        expected_terms = [[[factor] + term, "1"] for term in residue_terms]
        require(record["families"] == ["lemma_F_six_site"]
                and record["terms"] == expected_terms,
                "an O4 six-site pure-fibre record changed")

    # Exact ordinary-polynomial unit identity g-m*(R-1)=m.
    R = D.p_const(0)
    for first, second in residue_terms:
        R = D.p_add(R, D.p_mul(var(first), var(second)))
    q = D.p_sub(R, D.p_const(1))
    for factor in LIFT_RECORDS.values():
        m = var(factor)
        g = D.p_mul(m, R)
        require(D.p_sub(g, D.p_mul(m, q)) == m,
                "an O4 pure-fibre unit identity changed")
    return {
        "admissible_cells": len(admissible),
        "maximal_localized_cells": len(support),
        "residue_cells": 34,
        "residue_holes": [list(cell) for cell in sorted(RESIDUE_HOLES)],
        "complete_fibres_checked": shadow["fibres_checked"],
        "coefficient_generators": len(records),
        "term_count_histogram": {str(count): multiplicity
                                 for count, multiplicity in sorted(histogram.items())},
        "generator_sha256": D.content_hash(records),
        "six_site_lift_records": [[index, factor]
                                  for index, factor in LIFT_RECORDS.items()],
    }


def audit():
    started = monotonic()
    ledger = {
        "pinned_candidate_sha256": PINNED_CANDIDATE_SHA256,
        "residue_family": symbolic_family_audit(),
        "explicit_rational_point": explicit_point_audit(),
        "full_frontier": full_frontier_audit(),
        "pure_fibre_identity": "g-m*(R2222-1)=m",
        "boundary_implication": (
            "every O4 support containing any of x02_20,x02_21,x13_20,x13_21 "
            "is empty; a surviving boundary subcube must omit all four"
        ),
        "base_ring_scope": (
            "the residue parametrization and lift identities are polynomial "
            "over Z after the harmless F67_22 edge gauge"
        ),
        "characteristic_scope": "lift obstruction valid over every field",
        "status": (
            "O4 is residue-feasible, but its maximal full-support chart and "
            "four boundary-factor subcubes are empty"
        ),
    }
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the O4 residue/lift ledger changed")
    return ledger, digest, monotonic() - started


def main():
    ledger, digest, seconds = audit()
    print("n8 D1 residue orbit O4 family/lift: PASS (exact)")
    print("residue point cells:",
          ledger["explicit_rational_point"]["localized_coordinates"])
    print("full generators:", ledger["full_frontier"]["coefficient_generators"])
    print("lift records:", ledger["full_frontier"]["six_site_lift_records"])
    print("ledger sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()
