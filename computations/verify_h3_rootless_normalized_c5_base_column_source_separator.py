#!/usr/bin/env python3
r"""Primitive source separator for the normalized-C5 physical base column.

The exact R_v=0 normalization makes the five collision edges clean, but it
does not manufacture a vertex column.  In one repeated P3+K2 grade, the
closest existing physical cap combination is r0-T.  Its signature is

    (Eq,W,target,ores,ainc)=(1,1,0,0,-1),

so it retains the source-conormal Eq component.  The clean C5 edges can
change only ridge differences.  The desired comparison base has

    (-ridge_v,Eq,W,target,ores,ainc)=(-1,0,1,0,0,-1).

Two primitive covectors, total ridge and Eq+ainc, kill the complete existing
coarse source/cap/edge image and both read -1 on the desired column.  The
squarefree derived normal face would cancel Eq only after a nonphysical
degree/chart identification; the pinned complete P3+K2 source theorem and
single-face collision theorem exclude that identification in the existing
literal inventory.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "e90edede01f8008725630a630c2a8ec1ac54eff68fecbaa12b97664a5198766c"
PINS = {
    "computations/verify_h3_rootless_normalized_c5_augmented_comparison_gate.py":
        "fd6e94cd52a9f6950bf752887f9bea129373f6686b12704f6d2eaf29b7fa0dca",
    "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py":
        "719e48963faac5cd1dc5e7348de41e86f690f3046fefba88dddfa60bae532899",
    "computations/verify_h3_rootless_single_v_site_collision_comparison_obstruction.py":
        "34d627b9b0cdf4a81fbebc7c1d37231f53ac2d04be401c3f99402b0bf28c6fbe",
    "computations/verify_h3_rootless_zero_anchor_collision_edge_source_obstruction.py":
        "8249604a56f7fc8ee8a3c66a33cb905eed6a02202c43ed81283e91c61d748180",
    "computations/verify_h3_cyclotomic_regularized_shifted_filler_normal_face.py":
        "c409a62957dba0d101d1298ec16695482fce705d3131323a8d3657074f1bf2b0",
    "computations/verify_h3_shifted_denominator_chart_filler_augmented_commutator.py":
        "7d9e49f34da84772f6e0863a9bfe56cb9a90e0cfd3fceb76da59175ffea36c50",
}

FACES = (1, 3, 5, 2, 4)
ROWS = tuple(f"ridge_{face}" for face in FACES) + (
    "Eq", "W", "target", "ores", "ainc",
)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def vector(**entries: int) -> tuple[int, ...]:
    require(set(entries).issubset(ROWS), ("unknown row", entries))
    return tuple(entries.get(row, 0) for row in ROWS)


def add(*values: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sum(value[index] for value in values)
                 for index in range(len(ROWS)))


def scale(coefficient: int, value: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(coefficient * entry for entry in value)


def dot(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    return sum(a * b for a, b in zip(left, right, strict=True))


def rank(columns: list[tuple[int, ...]]) -> int:
    if not columns:
        return 0
    matrix = [[Q(column[row]) for column in columns]
              for row in range(len(ROWS))]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [left - value * right for left, right in
                           zip(matrix[row], matrix[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")

    # Clean physical collision edges on the exact normalized specialization.
    edges = []
    for index, face in enumerate(FACES):
        following = FACES[(index + 1) % len(FACES)]
        edges.append(vector(**{f"ridge_{face}": -1,
                               f"ridge_{following}": 1}))
    require(add(*edges) == vector() and rank(edges) == 4,
            "normalized C5 edge lattice changed")

    # Complete old cap/conormal block.  These are the literal coarse rows
    # pinned by the zero-anchor source obstruction.
    r0 = vector(Eq=1, target=1, ainc=-1)
    cap_T = vector(W=-1, target=1)
    cap_rho = vector(W=1, ores=1)
    closest = add(r0, scale(-1, cap_T))
    require(closest == vector(Eq=1, W=1, ainc=-1),
            "closest r0-T physical cap candidate changed")

    desired = vector(**{f"ridge_{FACES[0]}": -1,
                        "W": 1, "ainc": -1})
    required_repair = add(desired, scale(-1, closest))
    require(required_repair == vector(**{
        f"ridge_{FACES[0]}": -1, "Eq": -1,
    }), "base-column repair split changed")

    old_columns = edges + [r0, cap_T, cap_rho]
    old_rank = rank(old_columns)
    require(old_rank == 7, "coarse existing augmented rank changed")
    require(rank(old_columns + [desired]) == old_rank + 1,
            "desired base stopped raising augmented rank primitively")

    ridge_aggregate = vector(**{f"ridge_{face}": 1 for face in FACES})
    conormal_anchor = vector(Eq=1, ainc=1)
    for separator in (ridge_aggregate, conormal_anchor):
        require(all(dot(separator, column) == 0 for column in old_columns),
                ("primitive separator stopped killing old image", separator))
        require(dot(separator, desired) == -1,
                ("primitive separator stopped detecting base", separator))

    # The reduced Eq correction fixes only the conormal separator, and a
    # primitive ridge vertex fixes only the aggregate separator.  Both are
    # required in one source-valid column (or as separately constructed cells).
    reduced_eq = vector(Eq=-1)
    ridge_vertex = vector(**{f"ridge_{FACES[0]}": -1})
    require(add(closest, reduced_eq, ridge_vertex) == desired,
            "formal two-repair decomposition changed")
    require(dot(conormal_anchor, add(closest, reduced_eq)) == -1,
            "reduced Eq repair unexpectedly supplied physical anchor typing")
    require(dot(ridge_aggregate, add(closest, ridge_vertex)) == -1,
            "ridge vertex unexpectedly supplied the reduced Eq correction")

    ledger = {
        "pins": PINS,
        "fine_degree": "one normalized repeated-site P3+K2 component",
        "row_order": list(ROWS),
        "complete_admissible_coarse_image_after_boundary_constraints": {
            "clean_collision_edges": [list(column) for column in edges],
            "old_cap_conormal_columns": {
                "r0": list(r0), "T": list(cap_T), "rho": list(cap_rho),
            },
            "rank": old_rank,
            "complete_literal_scope": (
                "the pins include every polynomial full-nine row/multiplier "
                "in all five P3+K2 components, both chart copies, the literal "
                "first collision/PP routes, and the old cap block"
            ),
        },
        "closest_existing_candidate": {
            "name": "r0-T",
            "column": list(closest),
            "good_readouts": {"W": 1, "ainc": -1,
                              "target": 0, "ores": 0},
            "defects": ["pure Eq conormal +1", "no primitive ridge vertex"],
        },
        "desired_base": list(desired),
        "desired_rank_jump": 1,
        "primitive_duals": {
            "ridge_aggregate": list(ridge_aggregate),
            "Eq_plus_ainc": list(conormal_anchor),
            "values_on_existing_image": [0, 0],
            "values_on_desired": [-1, -1],
        },
        "formal_repairs": {
            "reduced_Eq": list(reduced_eq),
            "primitive_ridge_vertex": list(ridge_vertex),
            "sum_with_r0_minus_T": list(desired),
        },
        "normal_face_status": (
            "the derived normal face cancels the Eq term only in the "
            "squarefree indexed/chart presentation; it has no physical ainc "
            "or ridge-vertex value, and the pinned site-collision theorem "
            "shows that multiplying into P3+K2 forces the adjacent zero-anchor edge"
        ),
        "verdict": (
            "no existing physical source/Hasse/cap column in the complete "
            "audited repeated-site inventory realizes the normalized base; "
            "the earliest missing datum is a source-valid reduced-Eq plus "
            "primitive-ridge attachment (possibly one combined higher cell)"
        ),
        "scope": (
            "exact bounded theorem for the currently complete first P3+K2 "
            "source/PP/cap inventory after R_v=0 normalization; it does not "
            "exclude a genuinely new higher relative generator"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h=3 normalized C5 physical base-column source gate: SEPARATED")
    print("closest old column r0-T: Eq=1, W=1, ainc=-1")
    print("missing: reduced Eq + primitive ridge vertex")
    print("primitive duals: ridge aggregate; Eq+ainc")
    print("existing cap/normal-face correction: NO")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
