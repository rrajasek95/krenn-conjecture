#!/usr/bin/env python3
"""Prove that spectator completion preserves one private-minus-Eq class.

For k labelled residual perfect matchings retain B and Eq copies of the
four balanced operation corners.  Grant, more strongly than the literal
source, every matching-difference column in each corner and block, the four
aggregate physical diagonals B=Eq, and the four aggregate signless K2,2
companions.  The resulting 8k-row map has rank 8k-1.  Its unique left
kernel is the matching-constant extension of

    delta.(B-Eq),  delta=(1,1,-1,-1).

Thus all spectator restriction, reinsertion, shuffle, and overlap columns
whose total private/Eq mismatch is zero already lie in this projected
image.  A single occurrence-local column with nonzero mismatch fills the
projection.  This is a projection theorem, not a construction or repair of
the other augmented faces of such a column.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_uc4_four_site_response_private_eq_local_terminal_gate.py":
        "6c42cd4dc7dca1544dc0b675f5f4543ec348f1fba34b7ea14bf80cc6a20b9cf1",
    "notes/h3-uc4-four-site-response-private-eq-local-terminal-gate.md":
        "a7e10e0397ae3b31b9cce0e6bc2907f0c208634e22a0e3284076304130bd6989",
    "computations/verify_uniform_hyperbolic_collision_pp_augp2_spectator_naturality_gate.py":
        "0eedcb3f03e98ea18b549e2b6e21d7082cf368d8e3bc77fd3f104a178104c25a",
    "notes/uniform-hyperbolic-collision-pp-augp2-spectator-naturality-gate.md":
        "73fd2ff870db0d5344255cee1f2b4008bc19ba5058114f51b312d5a011eb760d",
}
EXPECTED_LEDGER_SHA256 = (
    "1912730a076903a3b51c41ec277d5267adf2938752ac17414961cb748188f3d8"
)

DELTA = tuple(map(Q, (1, 1, -1, -1)))


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def index(block: int, corner: int, matching: int, k: int) -> int:
    return (block * 4 + corner) * k + matching


def vector(k: int, entries: dict[tuple[int, int, int], int | Q]) \
        -> tuple[Q, ...]:
    answer = [Q(0)] * (8 * k)
    for (block, corner, matching), value in entries.items():
        answer[index(block, corner, matching, k)] += Q(value)
    return tuple(answer)


def add(*values: tuple[Q, ...]) -> tuple[Q, ...]:
    require(values and len({len(value) for value in values}) == 1,
            "add width")
    return tuple(sum(entries, Q(0)) for entries in zip(*values, strict=True))


def scale(coefficient: int | Q, value: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(Q(coefficient) * entry for entry in value)


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(height):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def projected_columns(k: int) -> tuple[tuple[Q, ...], ...]:
    columns: list[tuple[Q, ...]] = []

    # Grant every matching-augmentation-zero direction independently.
    for block in range(2):
        for corner in range(4):
            for matching in range(1, k):
                columns.append(vector(k, {
                    (block, corner, 0): -1,
                    (block, corner, matching): 1,
                }))

    # The physical normalized response/cap incidence ties B and Eq.
    for corner in range(4):
        columns.append(vector(k, {
            **{(0, corner, matching): 1 for matching in range(k)},
            **{(1, corner, matching): 1 for matching in range(k)},
        }))

    # Four signless K2,2 companions, aggregated over all tails.
    for direct in (0, 1):
        for endpoint in (2, 3):
            columns.append(vector(k, {
                **{(0, direct, matching): 1 for matching in range(k)},
                **{(0, endpoint, matching): 1 for matching in range(k)},
            }))
    require(len(columns) == 8 * k,
            ("projected column count", k, len(columns)))
    return tuple(columns)


def integral_dual(k: int) -> tuple[Q, ...]:
    return vector(k, {
        (block, corner, matching):
            (DELTA[corner] if block == 0 else -DELTA[corner])
        for block in range(2) for corner in range(4)
        for matching in range(k)
    })


def balanced(k: int, block: int, matching: int | None = None) \
        -> tuple[Q, ...]:
    matchings = range(k) if matching is None else (matching,)
    return vector(k, {
        (block, corner, item): DELTA[corner]
        for corner in range(4) for item in matchings
    })


def finite_rank_audit(k: int) -> dict[str, object]:
    columns = projected_columns(k)
    psi = integral_dual(k)
    expected_rank = 8 * k - 1
    actual_rank = rank(columns)
    require(actual_rank == expected_rank,
            ("uniform projected rank", k, actual_rank, expected_rank))
    require(all(dot(psi, column) == 0 for column in columns),
            ("uniform dual failed", k))

    b_all = balanced(k, 0)
    eq_all = balanced(k, 1)
    tied = add(b_all, eq_all)
    b_one = balanced(k, 0, 0)
    require(dot(psi, b_all) == 4 * k
            and dot(psi, eq_all) == -4 * k
            and dot(psi, tied) == 0
            and dot(psi, b_one) == 4,
            ("control value changed", k))
    require(rank(columns + (b_all,)) == 8 * k
            and rank(columns + (eq_all,)) == 8 * k
            and rank(columns + (tied,)) == expected_rank
            and rank(columns + (b_one,)) == 8 * k,
            ("control rank changed", k))

    # A spectator/window difference has total mismatch zero and is already
    # in the codimension-one image.  This is the exact overlap control.
    if k > 1:
        difference = add(balanced(k, 0, 0), scale(-1, balanced(k, 0, 1)))
        require(dot(psi, difference) == 0
                and rank(columns + (difference,)) == expected_rank,
                ("spectator overlap stopped being dark", k))

    return {
        "matching_count": k,
        "row_count": 8 * k,
        "column_count": 8 * k,
        "rank": actual_rank,
        "cokernel_dimension": 1,
        "B_delta_all_value": 4 * k,
        "Eq_delta_all_value": -4 * k,
        "B_delta_one_occurrence_value": 4,
        "tied_delta_value": 0,
    }


def structural_proof() -> dict[str, object]:
    # The matching-difference columns have disjoint block/corner support and
    # rank 8(k-1).  Quotienting by them replaces each matching fibre by its
    # augmentation.  The remaining 8-dimensional matrix is independent of
    # k: four B=Eq diagonals plus signless K2,2 incidence, rank seven, with
    # unique kernel delta.(B-Eq).  This proves the formula for every k.
    base_columns = projected_columns(1)
    base_dual = integral_dual(1)
    require(rank(base_columns) == 7
            and all(dot(base_dual, column) == 0
                    for column in base_columns),
            "eight-coordinate quotient changed")
    return {
        "matching_difference_rank": "8(k-1)",
        "eight_coordinate_quotient_rank": 7,
        "total_rank": "8(k-1)+7=8k-1",
        "unique_cokernel": "sum_matching delta dot (B-Eq)",
        "image_criterion": "total delta dot (B-Eq) equals zero",
        "filler_criterion": "some admitted column has nonzero total mismatch",
    }


def odd_double_factorial(value: int) -> int:
    answer = 1
    for factor in range(1, value + 1, 2):
        answer *= factor
    return answer


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    finite = [finite_rank_audit(k) for k in (1, 3, 15)]
    counts = {str(h): odd_double_factorial(2 * h - 3)
              for h in range(2, 8)}
    ledger = {
        "theorem": "uniform U_C4 private-minus-Eq spectator projection gate",
        "pins": PINS,
        "structural_proof": structural_proof(),
        "finite_rank_audits": finite,
        "all_order_matching_counts": counts,
        "verdict": (
            "For every number k of spectator matching occurrences, the "
            "projection-complete B/Eq map has rank 8k-1 in dimension 8k. "
            "Its unique cokernel is the matching-constant sum of "
            "delta.(B-Eq).  All restriction, reinsertion, shuffle, and "
            "overlap columns with zero total mismatch already lie in the "
            "image.  One occurrence-local nonzero mismatch fills the "
            "projection.  Spectator completion therefore neither fills nor "
            "proliferates the balanced obstruction."),
        "scope": (
            "Exact all-k B/Eq projection theorem and finite exact rank "
            "audits for k=1,3,15.  It does not construct the missing "
            "cross-profile DQ/PS column, prove that the physical global map "
            "contains no further columns, or repair a bright column's word, "
            "target, q, anchor, residue, W, or ridge faces."),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    print("uniform U_C4 private/Eq spectator projection: PASS")
    print("finite k audits:",
          [item["matching_count"] for item in ledger["finite_rank_audits"]])
    print("all-order rank: 8k-1 / 8k")
    print("unique cokernel: sum_matching delta.(B-Eq)")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
