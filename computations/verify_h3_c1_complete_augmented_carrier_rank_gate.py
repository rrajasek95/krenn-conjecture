#!/usr/bin/env python3
"""Evaluate the smallest available h=3 augmented carrier rank gate.

The canonical reduced-Eq output packet has 45 literal augmented rows and
19 unconditional independent columns (20 after a conditional primitive
anchor).  It is not the degree-two carrier boundary D_Q: the desuspension
chi and its physical q/input comparison are missing, so L1 is not yet
defined.  Conditionally adjoining the first primitive/common-carrier cell,
the strongest one-R-generator package still misses the pure beta*c1 face by
one rank.  A second filtered column is necessary even with zero leakage on
all 45 physical rows.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "notes/h3-reduced-eq-full-physical-augmentation-matrix.md":
        "465010f65fb479998a9436fb4fdcc605fd91f9165c641493b00bb75f561e4355",
    "computations/verify_h3_reduced_eq_full_physical_augmentation_matrix.py":
        "f66752bd3a44a9506b4a31467ce52dcb16e52f841b0f29ce66066a38ec7f97c1",
    "notes/h3-direct-free-normals-e14-pointed-composition-gate.md":
        "aa927470ffc926bc5639be94c76ab66c00cdabfa0082a0b94f6d117d7add0942",
    "computations/verify_h3_direct_free_normals_e14_pointed_composition_gate.py":
        "ea8cb46d5ee84b1973cb062df73b75c0704a0a31823b53e7187e737175964d53",
    "notes/scalar-unit-c1-weighted-endpoint-bockstein-gate.md":
        "c954f7c6d70368b7aee98208f68dc4c53ff6dae93e49cfa3862939707d00f7a3",
    "computations/verify_scalar_unit_c1_weighted_endpoint_bockstein_gate.py":
        "11fda4d929d1b064fe49ff9f45e077a2dd9bffdaec23a85b4be8a55d44561fa8",
    "notes/h3-literal-mv-odd-reduced-eq-projection-scope.md":
        "b1ad2a43e110a91ed1d0e29afc9a09076b3ef9633ef3015785a914848b06b2cf",
    "computations/verify_h3_literal_mv_odd_reduced_eq_projection_scope.py":
        "deb0ad5e35d42428d7440310af24951d3cb29deb55116fb5ab8eacef5fa1f729",
}
EXPECTED_LEDGER_SHA256 = (
    "c7001ff897e3c3088c7a17809377ff8df82998ab3c949204e38b3e7d40be0d5e"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def load_module(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot load module", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def rank(columns: list[list[Fraction] | tuple[Fraction, ...]]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [
        [Fraction(columns[column][row]) for column in range(len(columns))]
        for row in range(height)
    ]
    rank_value = 0
    for column in range(len(columns)):
        pivot = next(
            (row for row in range(rank_value, height) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank_value], rows[pivot] = rows[pivot], rows[rank_value]
        pivot_value = rows[rank_value][column]
        rows[rank_value] = [entry / pivot_value for entry in rows[rank_value]]
        for row in range(height):
            if row == rank_value or not rows[row][column]:
                continue
            coefficient = rows[row][column]
            rows[row] = [
                entry - coefficient * pivot_entry
                for entry, pivot_entry in zip(
                    rows[row], rows[rank_value], strict=True
                )
            ]
        rank_value += 1
        if rank_value == height:
            break
    return rank_value


def dot(left, right) -> Fraction:
    require(len(left) == len(right), "dot width")
    return sum((
        Fraction(a) * Fraction(b)
        for a, b in zip(left, right, strict=True)
    ), Fraction(0))


def physical_output_packet_audit() -> dict[str, object]:
    physical = load_module(
        "computations/verify_h3_reduced_eq_full_physical_augmentation_matrix.py",
        "h3_reduced_eq_full_augmented",
    )
    r0, cap, response, cartan, anchor = physical.old_full_columns()
    unconditional = list(r0 + cap + response + [cartan])
    with_anchor = unconditional + [anchor]
    require(physical.ROWS == 45, "full augmented row count changed")
    require(rank(unconditional) == 19,
            "unconditional full-output column rank changed")
    require(rank(with_anchor) == 20,
            "conditionally anchored full-output rank changed")

    q_covector = physical.physical_q_covector()
    require(all(dot(q_covector, column) == 0 for column in with_anchor),
            "known output column violated physical q")

    # The full-alpha M_v output is already a combination and does not raise
    # this rank.  Recompute its exact completed column.
    _b, _nearest, _records, completed_alpha = physical.sign_and_membership_audit(
        r0, cap, response, cartan, anchor
    )
    require(rank(unconditional + [completed_alpha]) == 19,
            "completed alpha output stopped being in the known span")
    return {
        "row_count": physical.ROWS,
        "row_order": (
            "lower_6, Eq_6, Yw_6, physical_W_6, target_6, ores_6, "
            "ainc, eta/sigma_7, q"
        ),
        "unconditional_columns": {
            "r0": 6, "T": 6, "rho": 6, "placed_Cartan": 1,
        },
        "unconditional_rank": rank(unconditional),
        "conditional_anchor_columns": 1,
        "rank_after_granted_anchor": rank(with_anchor),
        "physical_q_relation": "q+sum(lower)+ainc=0",
        "full_alpha_Mv_adds_rank": 0,
        "scope": (
            "complete output-side reduced-Eq augmentation; not the "
            "degree-two carrier boundary D_Q"
        ),
    }


def first_missing_map_audit() -> dict[str, object]:
    direct_free = (ROOT / (
        "notes/h3-direct-free-normals-e14-pointed-composition-gate.md"
    )).read_text()
    mv_scope = (ROOT / (
        "notes/h3-literal-mv-odd-reduced-eq-projection-scope.md"
    )).read_text()
    c_one = (ROOT / (
        "notes/scalar-unit-c1-weighted-endpoint-bockstein-gate.md"
    )).read_text()
    require("The smallest missing column is one source-labelled residue section (7)" in direct_free
            and r"p=(-Q,-\operatorname {ores})" in direct_free,
            "primitive pointed column frontier changed")
    require("input comparison / physical q" in mv_scope
            and "OPEN" in mv_scope,
            "physical input/q scope changed")
    require("Let (V) be a finite cycle basis" in c_one
            and r"\operatorname {rank}D_Q" in c_one,
            "c1 finite criterion changed")
    return {
        "D_Q_available": False,
        "reason": (
            "the 45-row packet is an output-side reduced-Eq map; no "
            "source-labelled degree-two carrier desuspension chi or its "
            "vertical kernel is present"
        ),
        "L1_available": False,
        "reason_L1": (
            "L1=(r-2q)chi|ker(pi) cannot be evaluated before pi and chi "
            "are physical chain maps"
        ),
        "first_absent_source_column_before_c1": (
            "the pointed common-carrier/primitive residue section "
            "p=(-Q,-ores) in word 01211222, repeated P3+K2, together "
            "with the input comparison and physical-q transport"
        ),
        "first_absent_source_map": (
            "chi: ordered four-star carrier -> one complete augmented "
            "degree-two carrier module Q_1"
        ),
        "ordinary_residue_guard": (
            "all currently relevant Eq corrections have ores=0, while p "
            "has ores=-1"
        ),
    }


def conditional_second_cell_rank_audit() -> dict[str, object]:
    """Evaluate the coarse second-cell rank after granting the first cell."""
    # The physical packet has 45 rows.  Add the four filtered coordinates
    # (p,beta*p,c1,beta*c1).  Giving every formal filtered column zero on all
    # 45 rows is the strongest optimistic no-leakage assumption: protected,
    # anchor, terminal, and q are all zero there.
    physical_rows = 45
    filtered_rows = 4
    total_rows = physical_rows + filtered_rows

    def filtered(vector):
        require(len(vector) == filtered_rows, "filtered vector width")
        return tuple([Fraction(0)] * physical_rows + list(map(Fraction, vector)))

    g = filtered((1, 0, 0, 1))       # dG=p+beta*c1
    beta_g = filtered((0, 1, 0, 0))  # beta*dG=beta*p
    p = filtered((1, 0, 0, 0))
    weighted = filtered((0, 0, 0, 1))
    c1_unshifted = filtered((0, 0, 1, 0))

    require(len(g) == total_rows, "complete optimistic row width changed")
    first_family = [g, beta_g]
    require(rank(first_family) == 2, "one-R family rank changed")
    require(rank(first_family + [p]) == 3
            and rank(first_family + [weighted]) == 3,
            "one-R family unexpectedly killed an individual face")
    require(rank(first_family + [p, weighted]) == 3,
            "p and beta*c1 stopped differing by the family relation")

    anti_diagonal = tuple(
        [Fraction(0)] * physical_rows
        + [Fraction(1), Fraction(0), Fraction(0), Fraction(-1)]
    )
    require(all(dot(anti_diagonal, column) == 0 for column in first_family)
            and dot(anti_diagonal, p) == 1
            and dot(anti_diagonal, weighted) == -1,
            "second-cell primitive dual changed")

    second_cell = weighted
    require(rank(first_family + [second_cell]) == 3
            and rank(first_family + [second_cell, p]) == 3,
            "pure weighted second cell did not close the coarse packet")

    # c1 itself is not the beta face.  This prevents a grade-forgetting
    # substitution of the unshifted carrier for the required second cell.
    require(rank(first_family + [c1_unshifted]) == 3
            and rank(first_family + [c1_unshifted, weighted]) == 4,
            "unshifted c1 became the beta face after forgetting grade")
    return {
        "complete_row_count_in_optimistic_guard": total_rows,
        "physical_rows_set_to_zero_on_formal_faces": physical_rows,
        "physical_zero_rows": (
            "all lower/Eq/Yw/W/target/ores/ainc/eta/sigma/q rows"
        ),
        "filtered_basis": ["p", "beta*p", "c1", "beta*c1"],
        "one_R_generator_columns": [
            [1, 0, 0, 1], [0, 1, 0, 0],
        ],
        "one_R_image_rank": 2,
        "rank_after_p": 3,
        "rank_after_beta_c1": 3,
        "surviving_primitive_dual": [1, 0, 0, -1],
        "minimum_additional_filtered_columns": 1,
        "second_column_coarse_signature": [0, 0, 0, 1],
        "second_column_meaning": (
            "a source-valid desuspended first-moment nullhomotopy Gamma_1 "
            "whose boundary is L1(z)=-(1/6)(r-2q)chi(z)"
        ),
        "unshifted_c1_is_not_beta_c1": True,
        "scope": (
            "necessary coarse rank under zero physical leakage; the actual "
            "45-row dressing of Gamma_1 remains to be constructed"
        ),
    }


def actual_rank_interface_audit() -> dict[str, object]:
    # This is the exact finite interface once chi and pi are constructed.
    # A universal two-dimensional boundary plus one independent L1 column
    # verifies both sides of the rank/cokernel alternative.
    d_q = [
        [Fraction(1), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(0)],
    ]
    l_one = [Fraction(0), Fraction(0), Fraction(1)]
    require(rank(d_q + [l_one]) == rank(d_q) + 1,
            "unrepaired L1 did not raise rank")
    separator = [Fraction(0), Fraction(0), Fraction(1)]
    require(all(dot(separator, column) == 0 for column in d_q)
            and dot(separator, l_one) == 1,
            "L1 cokernel dual changed")
    require(rank(d_q + [l_one]) == rank(d_q + [l_one, l_one]),
            "explicit L1 correction did not close membership")
    return {
        "finite_test_after_construction": (
            "rank(D_Q)=rank([D_Q|L1])"
        ),
        "failure": (
            "lambda*D_Q=0, lambda*L1(z)!=0 for one vertical cycle z"
        ),
        "success_column": (
            "Gamma_1(z) with d Gamma_1(z)=L1(z), for each basis z of ker pi"
        ),
        "terminal_scope": (
            "lambda is physical only because D_Q is required to include all "
            "45 protected/anchor/terminal/q rows"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 complete augmented c1 carrier rank gate",
        "pins": PINS,
        "available_output_packet": physical_output_packet_audit(),
        "first_missing_map": first_missing_map_audit(),
        "conditional_second_cell": conditional_second_cell_rank_audit(),
        "actual_rank_interface": actual_rank_interface_audit(),
        "verdict": (
            "The smallest committed 45-row h3 output packet has all known "
            "protected/anchor/terminal/q rows, but it is not the carrier "
            "boundary D_Q. The pointed common-carrier desuspension chi, its "
            "vertical kernel, and physical q input comparison are missing, "
            "so the actual L1 rank cannot yet be numerically evaluated. "
            "Conditionally granting that first cell, the strongest one-R "
            "package misses the pure beta*c1 face by exactly one rank even "
            "when all 45 physical readouts are set to zero. The second "
            "necessary source column is Gamma_1 with boundary "
            "-(1/6)(r-2q)chi(z); its full augmented dressing is the next "
            "finite membership problem."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("h3 c1 complete augmented ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("available h3 augmented output: 45 rows, rank 19 (20 conditional)")
    print("actual carrier D_Q/L1: NOT YET TYPED")
    print("conditional one-R package: beta*c1 raises rank by 1")
    print("first second-cell column: d Gamma_1=-(1/6)(r-2q)chi(z)")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
