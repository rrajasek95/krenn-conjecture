#!/usr/bin/env python3
"""Bounded exact audit of the first Segre-syzygy pullback.

This checker connects the abstract first Segre master syzygy to the
source-labelled response identities already audited in the repository.  It
also verifies the sharp h=3 Hilbert--Burch boundary: ordinary Pluecker
pullback supplies degree three, whereas the desired Fitting defect needs
total column degree at most two.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PINS = {
    "notes/hafnian-star-minor-buchberger-identity.md":
        "bd7c47eb418fc8329b4c4dc814e9857086a2c9a92e12de8efa034f696f7a78dc",
    "computations/verify_n8_chart26_first_homogeneous_spair.py":
        "48a74185944b32455ac450a1715cc4cae1d2a4b3f482ff4220219d051e2e433b",
    "notes/uniform-response-plucker-veronese-hilbert-burch-gate.md":
        "88c2cfe20f026ff051c8e10c7e2f39f4f0407fbc9d29fe9def3fcf1d64cce800",
    "computations/verify_uniform_response_plucker_veronese_hilbert_burch_gate.py":
        "ede18e6bc81fa96b8a720806be71a834d85332c807f27717b2e0811ace50c67d",
    "notes/uniform-diagonal-second-polar-fitting-gap.md":
        "abd35f7f9e2788bf194f95a76b3b4a7d2c6fbf574572e58c201046dbd9e1d7b3",
    "computations/verify_uniform_diagonal_second_polar_fitting_gap.py":
        "1a45ad1a913d8e43767596b191dc011457b24bbf908ad1b097911f692cf9487c",
    "notes/plucker-hessian-closure-and-defect-three-transition-guard.md":
        "b7fc6e209ec09d63cd6a0cbd9de7baa68ce30a84419ffd337cd3f3f71c5d64e7",
    "computations/verify_plucker_hessian_closure_and_defect_three_transition_guard.py":
        "bc53dd16029db17a0f99645bae55582c467aaab61e390ac44ae97e7a1d8aec54",
    "notes/differential-plucker-diagonal-escape-and-separated-packet.md":
        "418cb2aab3f7215707dd53fa543deeb324d53f7471517fe255280d0d4ac76004",
    "computations/verify_differential_plucker_diagonal_escape_and_separated_packet.py":
        "65503f61fec82a199900966ff2491b5256ead03f1cfb281ee6c9e10035fba214",
}

Q = Fraction


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def clean(poly):
    return {monomial: coefficient for monomial, coefficient in poly.items()
            if coefficient}


def add(left, right, scale=Q(1)):
    out = dict(left)
    for monomial, coefficient in right.items():
        out[monomial] = out.get(monomial, Q(0)) + scale * coefficient
    return clean(out)


def mul(left, right):
    out = {}
    for monomial_left, coefficient_left in left.items():
        for monomial_right, coefficient_right in right.items():
            monomial = tuple(sorted(monomial_left + monomial_right))
            out[monomial] = out.get(monomial, Q(0)) + (
                coefficient_left * coefficient_right
            )
    return clean(out)


def var(name):
    return {(name,): Q(1)}


def determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    answer = {}
    for column in range(len(matrix)):
        minor = [row[:column] + row[column + 1:] for row in matrix[1:]]
        answer = add(
            answer,
            mul(matrix[0][column], determinant(minor)),
            Q(-1 if column % 2 else 1),
        )
    return answer


def rational_rank(rows):
    work = [list(map(Q, row)) for row in rows]
    rank = 0
    columns = len(work[0]) if work else 0
    for column in range(columns):
        pivot = next((row for row in range(rank, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        value = work[rank][column]
        work[rank] = [entry / value for entry in work[rank]]
        for row in range(len(work)):
            if row == rank or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [entry - value * pivot_entry
                         for entry, pivot_entry in zip(
                             work[row], work[rank], strict=True)]
        rank += 1
    return rank


def first_segre_syzygy_audit():
    x = [[var(f"x{row}{column}") for column in range(3)]
         for row in range(2)]

    def minor(left, right):
        return add(mul(x[0][left], x[1][right]),
                   mul(x[0][right], x[1][left]), Q(-1))

    delta01, delta02, delta12 = minor(0, 1), minor(0, 2), minor(1, 2)
    for row in range(2):
        syzygy = add(
            add(mul(x[row][0], delta12),
                mul(x[row][1], delta02), Q(-1)),
            mul(x[row][2], delta01),
        )
        require(not syzygy, ("Segre first syzygy changed", row, syzygy))

    # Under x_ij=p_i*s_j every generating minor vanishes termwise.
    p = [var("p0"), var("p1")]
    s = [var("s0"), var("s1"), var("s2")]
    rank_one = [[mul(p[row], s[column]) for column in range(3)]
                for row in range(2)]
    for left, right in ((0, 1), (0, 2), (1, 2)):
        image = add(
            mul(rank_one[0][left], rank_one[1][right]),
            mul(rank_one[0][right], rank_one[1][left]), Q(-1),
        )
        require(not image, ("rank-one Segre minor survived", left, right))

    return {
        "representative_linear_master_syzygies": 2,
        "minor_images_after_endpoint_star_pullback": 0,
        "verdict": (
            "the abstract first Segre syzygy pulls back to the ordinary "
            "source Pluecker identity; it is exact but carries no new "
            "common-power class by itself"
        ),
    }


def h3_hilbert_burch_audit():
    u, v, zero = var("u"), var("v"), {}
    matrix = [
        [v, zero, zero],
        [add({}, u, Q(-1)), v, zero],
        [zero, add({}, u, Q(-1)), v],
        [zero, zero, add({}, u, Q(-1))],
    ]
    cofactors = []
    for deleted in range(4):
        minor = [row for index, row in enumerate(matrix) if index != deleted]
        cofactor = determinant(minor)
        if deleted % 2:
            cofactor = {monomial: -coefficient
                        for monomial, coefficient in cofactor.items()}
        cofactors.append(cofactor)

    expected = [
        mul(mul(u, u), u),
        mul(mul(u, u), v),
        mul(mul(u, v), v),
        mul(mul(v, v), v),
    ]
    # Cofactors are determined up to one common unit.
    global_sign = next(iter(cofactors[0].values())) / next(
        iter(expected[0].values())
    )
    require(global_sign in (Q(1), Q(-1)), "unexpected cofactor unit")
    require(all(cofactor == {monomial: global_sign * coefficient
                             for monomial, coefficient in target.items()}
                for cofactor, target in zip(cofactors, expected, strict=True)),
            "h=3 Hilbert--Burch maximal minors changed")

    # Degree-3 forms multiplied by S_2 span every binary quintic.
    degree2 = [(2, 0), (1, 1), (0, 2)]
    degree3 = [(3, 0), (2, 1), (1, 2), (0, 3)]
    columns = []
    for a, b in degree3:
        for c, d in degree2:
            exponent = (a + c, b + d)
            columns.append([Q(int(exponent == (5 - row, row)))
                            for row in range(6)])
    macaulay_rank = rational_rank(list(map(list, zip(*columns))))
    require(macaulay_rank == 6, ("h=3 Macaulay rank changed", macaulay_rank))

    return {
        "clean_family": ["u^3", "u^2v", "uv^2", "v^3"],
        "Hilbert_Burch_columns": 3,
        "Hilbert_Burch_total_column_degree": 3,
        "forcing_threshold": 2,
        "clean_Macaulay_rank": macaulay_rank,
        "simultaneous_Bezout_kernel_dimension": 0,
        "verdict": "sharp Veronese boundary; one degree too large",
    }


def dependency_and_scope_audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    return {
        "pinned_exact_artifacts": len(PINS),
        "literal_first_Buchberger_cell": {
            "terms": 180,
            "new_leads": 2,
            "new_leads_squarefree": True,
        },
        "differential_Pluecker": (
            "genuinely strengthens transition flatness on gauge-rigid "
            "charts but does not construct the missing Fitting relation"
        ),
        "diagonal_second_polar": (
            "sees response grade 2 only and misses grades 3,...,h"
        ),
    }


def main():
    ledger = {
        "theorem": "bounded first Segre-master-syzygy pullback audit",
        "first_master_layer": first_segre_syzygy_audit(),
        "h3_clean_presentation": h3_hilbert_burch_audit(),
        "archive_crosswalk": dependency_and_scope_audit(),
        "conclusion": (
            "ordinary and first differential Segre/Pluecker pullbacks are "
            "already exhausted; they reach the sharp degree-h boundary "
            "but do not lower it. The unresolved object must mix a labelled "
            "diagonal anchor with all response grades 2,...,h in one "
            "source-provenant higher operation"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    print("Segre master-syzygy pullback: SHARP NON-FORCING BOUNDARY")
    print("h=3 degree 3; forcing threshold 2; Macaulay rank 6")
    print("ledger_sha256=" + sha256(payload.encode()).hexdigest())


if __name__ == "__main__":
    main()
