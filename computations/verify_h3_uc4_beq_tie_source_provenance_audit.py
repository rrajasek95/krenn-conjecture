#!/usr/bin/env python3
"""Audit the source provenance of the load-bearing B=Eq tie.

There are two different statements which must not be conflated.

1.  The already constructed cap generator r_0 is internally tied: its
    literal full-nine response boundary is the private B packet and its
    cap differential has the reduced-Eq face (H_0-u)e_Eq.
2.  A response-side four-site Hasse row has no constructed cross-word map
    to that cap generator.  The four tied rows used in the 126/127 local
    supermap are therefore a conditional choice of its missing image, not
    a derivation of the mixed mapping-cylinder incidence.

The finite sensitivity calculation is decisive.  Four tied diagonal rows
together with the signless K2,2 companions have rank 7 in B+Eq and unique
left kernel delta.(B-Eq).  If just one diagonal row loses its Eq component,
the rank remains 7 but the unique kernel becomes the unused Eq coordinate;
the desired private delta packet is no longer detected.  With two or more
untied rows the rank drops below 7 and the cokernel is non-unique.

Thus the local terminal theorem is exact conditional on all four ties, but
the tie for the cross-word response image is precisely part of the eight
still-undecided kappa_mix incidences, not an earlier physical theorem.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_full_hasse_koszul_cap_totalization.py":
        "51940ce0ac8387b68e7725508db6da1a1c055ea036335bbf19750580c69e13fb",
    "computations/verify_h3_residual_q_literal_mapping_cone_private_boundary_gate.py":
        "b890195a8fc0c4e90c9c9c0c03c41a95690228c81026f4c2ea1fa95908564e38",
    "computations/verify_h3_uc4_four_site_response_private_eq_local_terminal_gate.py":
        "6c42cd4dc7dca1544dc0b675f5f4543ec348f1fba34b7ea14bf80cc6a20b9cf1",
    "computations/verify_h3_balanced_square_private_eq_projection_gate.py":
        "bbfb690a73844169574351ad019171a6d9c5fe332e59cc9694a1f67dcf31cf8e",
    "computations/verify_h3_gamma_star_source_operation_essential_surjectivity_census.py":
        "e5f2664b99c5ba58e0be385ca52dc52c6d2f6d6d0b793e655ebe297542dce291",
}
EXPECTED_LEDGER_SHA256 = (
    "1ba9269700cead684c84fc90642da8dab3676e3d12a93826d43dfc190542978f"
)

DELTA = (Q(1), Q(1), Q(-1), Q(-1))
EDGES = ((0, 2), (0, 3), (1, 2), (1, 3))


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative,
                                     expected, actual))


def dot(left, right) -> Q:
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(height):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def left_nullspace(columns: tuple[tuple[Q, ...], ...]) \
        -> tuple[tuple[Q, ...], ...]:
    """Return a rational basis for vectors annihilating every column."""
    width = len(columns[0])
    matrix = [[Q(entry) for entry in column] for column in columns]
    rows = len(matrix)
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(width):
        pivot = next((row for row in range(pivot_row, rows)
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [left - value * right for left, right in
                           zip(matrix[row], matrix[pivot_row], strict=True)]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break
    free = tuple(column for column in range(width)
                 if column not in pivot_columns)
    basis = []
    for free_column in free:
        vector = [Q(0)] * width
        vector[free_column] = Q(1)
        for row, pivot_column in reversed(tuple(enumerate(pivot_columns))):
            vector[pivot_column] = -sum(
                (matrix[row][column] * vector[column]
                 for column in free), Q(0))
        basis.append(tuple(vector))
    require(all(all(dot(vector, column) == 0 for column in columns)
                for vector in basis), "left-nullspace computation failed")
    return tuple(basis)


def projected_columns(mask: tuple[int, int, int, int]) \
        -> tuple[tuple[Q, ...], ...]:
    columns = []
    for corner, tied in enumerate(mask):
        column = [Q(0)] * 8
        column[corner] = Q(1)
        column[4 + corner] = Q(tied)
        columns.append(tuple(column))
    for direct, endpoint in EDGES:
        column = [Q(0)] * 8
        column[direct] = column[endpoint] = Q(1)
        columns.append(tuple(column))
    return tuple(columns)


def cap_r0_provenance_audit() -> dict[str, object]:
    total = load(
        "computations/verify_h3_full_hasse_koszul_cap_totalization.py",
        "beq_totalization",
    )
    _chain, _boundary, differential, target, _ores = \
        total.translated_totalization({})
    require(differential["r_0"] == {"eq": total.F_PURE},
            "the constructed cap r_0 lost its reduced-Eq differential")
    require(target["r_0"] == {"target": total.constant()},
            "the constructed cap r_0 lost its normalized target")

    literal = load(
        "computations/verify_h3_residual_q_literal_mapping_cone_private_boundary_gate.py",
        "beq_literal_r0",
    )
    literal_ledger, _literal_digest = literal.audit()
    require(literal_ledger["verdict"].endswith(
                "its physical source membership remains open"),
            "the literal r_0 gate no longer records the open image membership")
    return {
        "constructed_cap_generator": "r_0",
        "literal_response_boundary": "private full-nine B packet",
        "internal_cap_differential": "d r_0=(H_0-u)e_Eq",
        "normalized_target": 1,
        "internal_B_equals_Eq_tie": True,
        "cross_word_response_to_cap_membership": "OPEN",
    }


def local_row_constructor_audit() -> dict[str, object]:
    local = load(
        "computations/verify_h3_uc4_four_site_response_private_eq_local_terminal_gate.py",
        "beq_local_terminal",
    )
    normalized = tuple(
        column for name, column in local.top_projection_columns()
        if name.startswith("normalized-response:r0:")
    )
    require(len(normalized) == 4, "local checker lost four normalized rows")
    for corner, column in enumerate(normalized):
        b = tuple(column[local.INDEX[local.top_label("B", corner, matching)]]
                  for matching in range(3))
        eq = tuple(column[local.INDEX[local.top_label("Eq", corner, matching)]]
                   for matching in range(3))
        require(b == eq == (Q(1), Q(1), Q(1)),
                ("local tied row changed", corner, b, eq))

    census = load(
        "computations/verify_h3_gamma_star_source_operation_essential_surjectivity_census.py",
        "beq_gamma_census",
    )
    ledger, _digest = census.audit()
    operation = ledger["quotient"]
    require(operation["not_decided"]
            == "the eight physical lambda_i=Psi(d kappa_i)",
            "the mixed kappa incidence is no longer recorded as undecided")
    return {
        "local_supermap_rows": 4,
        "constructor_used_there": "B=Eq=(1,1,1) inserted cornerwise",
        "literal_response_word": "11:110000",
        "literal_cap_word": "01211222",
        "constructed_cross_word_map": False,
        "undecided_mixed_incidences": 8,
        "interpretation": (
            "the tied local row is the cap r_0 image conditional on the "
            "missing cross-word/K_Eq comparison, not a construction of it"
        ),
    }


def sensitivity_audit() -> dict[str, object]:
    chi = DELTA + tuple(-entry for entry in DELTA)
    balanced_private = DELTA + (Q(0),) * 4
    rows = []
    for raw_mask in product((0, 1), repeat=4):
        mask = tuple(raw_mask)
        columns = projected_columns(mask)
        kernel = left_nullspace(columns)
        record = {
            "mask": "".join(map(str, mask)),
            "rank": rank(columns),
            "cokernel_dimension": len(kernel),
            "chi_annihilates": all(dot(chi, column) == 0
                                   for column in columns),
            "balanced_private_values": [str(dot(vector, balanced_private))
                                         for vector in kernel],
        }
        if sum(mask) == 3:
            missing = mask.index(0)
            require(record["rank"] == 7 and len(kernel) == 1,
                    ("one-untied control lost rank seven", record))
            require(all(kernel[0][index] == 0 for index in range(4))
                    and kernel[0][4 + missing] != 0,
                    ("one-untied kernel is not the unused Eq row", record,
                     kernel))
            require(dot(kernel[0], balanced_private) == 0,
                    "one-untied kernel unexpectedly detects private delta")
        rows.append(record)

    tied = next(record for record in rows if record["mask"] == "1111")
    require(tied["rank"] == 7 and tied["cokernel_dimension"] == 1
            and tied["chi_annihilates"]
            and tied["balanced_private_values"] not in (("0",), []),
            ("all-tied terminal control failed", tied))
    require(all(record["rank"] < 7 for record in rows
                if record["mask"].count("1") <= 2),
            "a two-or-fewer-tied mask retained the claimed rank-seven setup")
    return {
        "all_tied": tied,
        "one_untied_controls": [record for record in rows
                                 if record["mask"].count("1") == 3],
        "rank_histogram": {
            str(value): sum(record["rank"] == value for record in rows)
            for value in sorted({record["rank"] for record in rows})
        },
        "conclusion": (
            "all four ties are load-bearing: losing one preserves rank 7 "
            "but replaces delta.(B-Eq) by an Eq-only kernel which is blind "
            "to the desired private delta packet"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 U_C4 B=Eq source-provenance audit",
        "constructed_cap_r0": cap_r0_provenance_audit(),
        "four_site_cross_word_row": local_row_constructor_audit(),
        "exact_tie_sensitivity": sensitivity_audit(),
        "verdict": (
            "B=Eq is a theorem for the already constructed cap generator "
            "r_0.  It is not yet a theorem for the response-side four-site "
            "row, because the source-labelled 11:110000 to 01211222 map and "
            "its mixed K_Eq incidence are open.  The rank-126 local terminal "
            "therefore remains exact only conditional on that image being "
            "tied.  The eight kappa_mix scalars are exactly the missing test."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, ledger))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h=3 U_C4 B=Eq source provenance: SHARP CONDITIONAL")
    print("constructed cap r0 is tied: YES")
    print("cross-word four-site image is tied: NOT PROVED")
    print("one untied row preserves rank 7 but kills private-delta detection")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
