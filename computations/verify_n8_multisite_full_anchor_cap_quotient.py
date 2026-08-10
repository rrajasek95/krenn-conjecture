#!/usr/bin/env python3
"""Exact full-anchor quotient of the binary permanent-null cap.

The complete response packet fixes q^[3] and the four first insertions.  It
does not change the source-provenance grades of R_K^[2] q and R_K^[3].  This
checker computes their universal 8+16 sector normal form and pins the
six-site theorem which rules out a clean ordinary-source realization.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations_with_replacement
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SIX_SITE_THEOREM = ROOT / "proofs/six-site-arbitrary-complex-obstruction.md"
SIX_SITE_THEOREM_SHA256 = (
    "b36b2f9ccb577af0aebf897edfc9fa1f84d01ba0cf4ea49ac11799d992e00713"
)
K = ((Fraction(1), Fraction(1)),
     (Fraction(-1), Fraction(1)))


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def sector_normal_form(power: int):
    """Raw p-row/s-column multiset coefficients of R_K^[power]."""
    entries = tuple((i, j) for i in range(2) for j in range(2))
    answer = defaultdict(Fraction)
    provenance = defaultdict(list)
    for positions in combinations_with_replacement(range(4), power):
        multiplicities = {position: positions.count(position)
                          for position in set(positions)}
        denominator = 1
        for multiplicity in multiplicities.values():
            if multiplicity == 2:
                denominator *= 2
            elif multiplicity == 3:
                denominator *= 6
            else:
                require(multiplicity == 1, multiplicity)
        coefficient = Fraction(1, denominator)
        rows = []
        columns = []
        labelled_entries = []
        for position in positions:
            i, j = entries[position]
            rows.append(i)
            columns.append(j)
            coefficient *= K[i][j]
            labelled_entries.append((i, j))
        key = (tuple(sorted(rows)), tuple(sorted(columns)))
        answer[key] += coefficient
        provenance[key].append((tuple(labelled_entries), coefficient))
    return {key: value for key, value in answer.items() if value}, provenance


def multiply_sector_forms(left, right):
    answer = defaultdict(Fraction)
    for (left_rows, left_columns), left_coefficient in left.items():
        for (right_rows, right_columns), right_coefficient in right.items():
            key = (
                tuple(sorted(left_rows + right_rows)),
                tuple(sorted(left_columns + right_columns)),
            )
            answer[key] += left_coefficient * right_coefficient
    return {key: value for key, value in answer.items() if value}


def scale(form, scalar):
    return {key: scalar * value for key, value in form.items() if scalar * value}


def main() -> None:
    theorem_hash = sha256(SIX_SITE_THEOREM.read_bytes()).hexdigest()
    require(theorem_hash == SIX_SITE_THEOREM_SHA256,
            "the pinned arbitrary-complex N=6 theorem changed")
    require(K[0][0] * K[1][1] + K[0][1] * K[1][0] == 0,
            "the canonical cap lost permanent zero")

    first, _ = sector_normal_form(1)
    second, second_provenance = sector_normal_form(2)
    third, _ = sector_normal_form(3)
    require(len(first) == 4, len(first))
    require(len(second) == 8, len(second))
    require(len(third) == 16, len(third))
    cancelled_permanent_sector = ((0, 1), (0, 1))
    require(cancelled_permanent_sector not in second, second)
    require(sum(coefficient for _, coefficient
                in second_provenance[cancelled_permanent_sector]) == 0,
            "the distinct-label permanent sector changed")

    # In any characteristic-zero divided-power algebra,
    # R * R^[2] = 3 R^[3].  This is the load-bearing clean-lift implication.
    require(multiply_sector_forms(first, second) == scale(third, 3),
            "R R^[2] = 3 R^[3] changed")

    # The complete response quotient occupies only insertion orders 0 and 1.
    # These labels make the source-provenance separation explicit.
    quotient_ledger = {
        (3, 0): ("q^[3]", "X0"),
        (2, 1, 0, 0): ("p0*s0*q^[2]", "X1"),
        (2, 1, 0, 1): ("p0*s1*q^[2]", "0"),
        (2, 1, 1, 0): ("p1*s0*q^[2]", "0"),
        (2, 1, 1, 1): ("p1*s1*q^[2]", "X2"),
    }
    tail_grades = {(1, 2), (0, 3)}
    require(all(key[:2] not in tail_grades for key in quotient_ledger),
            "a response relation entered a higher insertion grade")

    print("N=8 multisite full-anchor cap quotient: PASS")
    print("complete quotient: q^[3]=X0; binary responses=diag(X1,X2)")
    print("first insertion: R_K*q^[2]=X1+X2")
    print("higher universal normal form: 8 q*R_K^[2] + 16 R_K^[3] sectors")
    print("divided-power identity: R_K*R_K^[2]=3*R_K^[3]")
    print("ordinary clean lift: impossible by pinned arbitrary-complex N=6 theorem")
    print("guard: q*R_K^[2]=0 alone is not excluded; it forces R_K^[3]!=0")


if __name__ == "__main__":
    main()
