#!/usr/bin/env python3
r"""Exact augmented comparison gate on the normalized rootless C5.

On the R_v=0 specialization of the target-preserving C5 slice, the five
physical collision edges are the saturated oriented incidence lattice of
C5 and the five derived fillers satisfy d n_v=Yw.  A physical comparison
would have to send

    (Yw, -S_v, marked=-1) -> (W, -r_v, ainc=-1).

The edge relations propagate one such physical vertex column around the
whole pentagon.  Conversely the clean edge lattice has W=ainc=0, so it
cannot construct even one base vertex column.  Thus the exact remaining
datum is one physical augmented base column (equivalently the comparison
on one n_v), not another collision edge.  Once it exists, the pinned
zero-indeterminacy-or-generator dichotomy makes Fredholm applicable; the
comparison itself is not supplied by etale normalization.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "2aa83dd425550fbcd632d0f1c18063ba3e940e0904517e3344fe0a80be469ad2"
PINS = {
    "computations/verify_h3_rootless_target_preserving_c5_etale_gauge.py":
        "02c2cc44c4d849e9db5d98c3c28882e93772dcc01cab286bba7d94cf8a8502be",
    "computations/verify_h3_component_iv_collision_family_normal_jet_interface.py":
        "a777687ed775c73b10129c0bee32b59f12fa3b579de39e6c4154e5ed94634651",
    "computations/verify_h3_derived_terminal_indeterminacy_or_relative_generator.py":
        "9327b57598a5264c11e5c3085e1afceaec8fd72c408f5fc1f1eaa2490a13a8b1",
}

FACES = (1, 3, 5, 2, 4)
ROWS = tuple(f"ridge_{face}" for face in FACES) + (
    "W", "ainc", "target", "ores",
)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def vector(**entries: int) -> tuple[int, ...]:
    require(set(entries).issubset(ROWS), ("unknown augmented row", entries))
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


def determinant(matrix: list[list[int]]) -> int:
    if len(matrix) == 1:
        return matrix[0][0]
    return sum(
        (-1) ** column * entry * determinant([
            row[:column] + row[column + 1:] for row in matrix[1:]
        ])
        for column, entry in enumerate(matrix[0])
    )


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")

    # E_i=-r_i+r_(i+1), with zero augmented readouts, is the exact clean
    # physical edge delivered by the normalized R_v=0 specialization.
    edges = []
    for index, face in enumerate(FACES):
        following = FACES[(index + 1) % len(FACES)]
        edges.append(vector(**{f"ridge_{face}": -1,
                               f"ridge_{following}": 1}))
    require(add(*edges) == vector(), "oriented C5 boundary stopped closing")
    require(rank(edges) == 4, "clean C5 edge rank changed")
    incidence_minor = [
        [edges[column][row] for column in range(4)] for row in range(4)
    ]
    require(abs(determinant(incidence_minor)) == 1,
            "clean C5 edge lattice stopped being saturated")
    require(all(column[ROWS.index("W")] == 0 and
                column[ROWS.index("ainc")] == 0 and
                column[ROWS.index("target")] == 0 and
                column[ROWS.index("ores")] == 0
                for column in edges),
            "a clean collision edge acquired an augmented readout")

    # The derived filler has d n_v=Yw, chart terminal -S_v, and marked
    # value -1.  A physical comparison preserving all typing must therefore
    # have this signature on its image p_v.
    physical_vertices = [
        vector(**{f"ridge_{face}": -1, "W": 1, "ainc": -1})
        for face in FACES
    ]
    for index, edge in enumerate(edges):
        following = (index + 1) % len(FACES)
        require(add(physical_vertices[index],
                    scale(-1, physical_vertices[following])) == edge,
                ("comparison stopped respecting a clean edge", index))
    require(rank(edges + [physical_vertices[0]]) == 5,
            "one base comparison column stopped completing the vertex family")

    # Starting with p_0, the edge equations recursively construct all p_i;
    # the final consistency equation is exactly sum E_i=0.
    propagated = [physical_vertices[0]]
    for index in range(4):
        propagated.append(add(propagated[-1], scale(-1, edges[index])))
    require(propagated == physical_vertices,
            "one base comparison column no longer propagates around C5")
    require(add(propagated[-1], scale(-1, edges[4])) == propagated[0],
            "degree-five C5 compatibility stopped closing the propagation")

    w_covector = vector(W=1)
    require(all(dot(w_covector, edge) == 0 for edge in edges),
            "W covector stopped killing the clean collision complex")
    require(dot(w_covector, physical_vertices[0]) == 1,
            "W covector stopped detecting the missing base comparison")

    # The marked chart sign and physical anchor sign are both -1.  This is
    # the typing required by the pinned physical dichotomy, not an assertion
    # that chart -S has already become physical ainc.
    derived_vertices = [
        {
            "face": face,
            "boundary": "Yw",
            "chart_terminal": f"-S_{face}",
            "marked_readout": -1,
            "target": 0,
            "ores": 0,
        }
        for face in FACES
    ]

    ledger = {
        "pins": PINS,
        "normalized_exact_C5": {
            "condition": "selected cycle cells are 1 and every R_v=0",
            "h_v_values": [1] * 5,
            "physical_clean_edges": [list(edge) for edge in edges],
            "edge_rank": rank(edges),
            "edge_lattice_saturated": True,
            "degree_five_compatibility": "sum E_v=0",
        },
        "derived_fillers": derived_vertices,
        "required_physical_images": {
            "rows": list(ROWS),
            "columns": [list(column) for column in physical_vertices],
            "typing": (
                "Yw->W, -S_v->-ridge_v, marked(-1)->ainc(-1), "
                "target->0, ores->0 in the same fine grade"
            ),
        },
        "minimality": {
            "one_base_column_suffices": True,
            "base_signature": list(physical_vertices[0]),
            "propagation": "p_(v+1)=p_v-E_v",
            "edge_only_rank": 4,
            "edge_plus_base_rank": 5,
            "primitive_edge_subcomplex_separator": "W",
            "normalization_constructs_base_column": False,
        },
        "fredholm_status": {
            "invocable_now": False,
            "reason": (
                "the etale gauge constructs the clean edge relations but no "
                "physical image of one n_v and hence no augmented polar P"
            ),
            "after_base_column": (
                "yes: edge propagation defines all five columns, and the "
                "pinned physical zero-indeterminacy-or-relative-generator "
                "dichotomy removes any separate ambiguity hypothesis"
            ),
            "primitive_anchor_as_input": (
                "not needed to invoke the alternative; a relative anchor is "
                "one possible output, while the other output is the separator"
            ),
        },
        "scope": (
            "exact normalized R_v=0 C5 specialization; this identifies the "
            "necessary-and-sufficient one-column comparison interface but "
            "does not construct that physical column or rename chart -S as ainc"
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
    print("h=3 normalized C5 augmented comparison gate: PASS")
    print("clean collision lattice: saturated rank 4")
    print("remaining datum: one physical augmented base column")
    print("etale normalization does not supply Yw -> W")
    print("Fredholm now: NO; after base column: YES")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
