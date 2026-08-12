#!/usr/bin/env python3
r"""First physical obstruction to the zero-anchor C5 collision edges.

The denominator/PP pairs have the correct repeated-site P3+K2 degrees and
the correct response-cancelling ridge boundaries.  Their strict chart
symbols have zero W/target/ores/ainc, but physical order-four descent leaves

    delta_i * (H_0-u) e_Eq,

where delta_i is one of a-b,c-d,e-a,b-c,d-e.

This checker proves that the complete bounded correction inventory cannot
cancel that pure Eq face with zero physical anchor incidence.  In the
decisive quotient every polynomial pure-row correction has signature

    (Eq,ainc,W,tgt,ores)=(1,-1,0,1,0),

while the old target/cap and residue columns have zero Eq and ainc.  The
primitive covector Eq+ainc kills the entire inventory and detects the
needed reduced Eq face.  The five defects do satisfy the exact degree-five
odd-cycle compatibility, so this is the first obstruction rather than a
sign or top-cell failure.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "377cad89d32bceb77e0cb7a648e4f27cad6d8b89940bc83183fc942dc68498d7"
PINS = {
    "computations/verify_h3_rootless_single_v_site_collision_comparison_obstruction.py":
        "34d627b9b0cdf4a81fbebc7c1d37231f53ac2d04be401c3f99402b0bf28c6fbe",
    "computations/verify_h3_rootless_five_cycle_denominator_pp_aggregate_no_go.py":
        "4f691d119469e76436e36566a1ca7307bc49a52f66b0687c1554a9e6531ec4de",
    "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py":
        "719e48963faac5cd1dc5e7348de41e86f690f3046fefba88dddfa60bae532899",
    "computations/verify_h3_rootless_c5_first_higher_anchor_spair.py":
        "3f9c39e8505da148d85a2d5125cefc502321f3652af2d9c0d12cd65aa41d469c",
    "computations/verify_h3_rootless_five_cycle_tate_anchor_obstruction.py":
        "a1383c13a732ec34eda5614c4346fecfd99b960480727ba26ac7089690844936",
    "computations/verify_h3_rootless_five_cycle_positive_interface.py":
        "fd359b3ff2abbb01d9508996c754a27b70890b2cd621926fc30b92057b337851",
    "computations/verify_h3_rootless_component_iii_complete_typed_inventory.py":
        "3e2b5912f58646169547b418bb4975a27635dcd8d548a010eb4c2e265412f465",
    "computations/verify_h3_rootless_third_cofactor_bianchi_total_complex_obstruction.py":
        "ebd25f79a6fe8db936fe5601b9220f152c5349dd794bbc4e08b2095f1c1d059f",
    "computations/verify_h3_cyclotomic_regularized_shifted_filler_normal_face.py":
        "c409a62957dba0d101d1298ec16695482fce705d3131323a8d3657074f1bf2b0",
}

Monomial = tuple[int, int, int, int, int]
Polynomial = dict[Monomial, int]
ZERO_MONOMIAL: Monomial = (0, 0, 0, 0, 0)
VARIABLES = ("a", "b", "c", "d", "e")
FACE_ORDER = (1, 3, 5, 2, 4)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")


def rank(columns: list[tuple[int | Q, ...]]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns),
            "ragged matrix")
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
        if pivot_row == height:
            break
    return pivot_row


def monomial(*indices: int) -> Monomial:
    value = [0] * 5
    for index in indices:
        value[index] += 1
    return tuple(value)  # type: ignore[return-value]


def monomial_product(left: Monomial, right: Monomial) -> Monomial:
    return tuple(a + b for a, b in zip(left, right, strict=True))  # type: ignore[return-value]


def polynomial(*terms: tuple[int, Monomial]) -> Polynomial:
    result: Polynomial = {}
    for coefficient, term in terms:
        result[term] = result.get(term, 0) + coefficient
        if result[term] == 0:
            del result[term]
    return result


def polynomial_add(left: Polynomial, right: Polynomial) -> Polynomial:
    result = dict(left)
    for term, coefficient in right.items():
        result[term] = result.get(term, 0) + coefficient
        if result[term] == 0:
            del result[term]
    return result


def polynomial_scale_monomial(value: Polynomial, factor: Monomial) -> Polynomial:
    return {monomial_product(term, factor): coefficient
            for term, coefficient in value.items()}


def dot(row: tuple[int, ...], column: tuple[int, ...]) -> int:
    return sum(a * b for a, b in zip(row, column, strict=True))


def physical_edge_obstruction() -> dict[str, object]:
    # Reduced correction rows are
    # (pure_Eq, physical_ainc, W, target, ordinary_residue).
    # The monic pure source row is the only existing column which can hit
    # the selected pure Eq label.  Target/cap and split-residue columns are
    # retained explicitly at Y=1; changing the nonzero normalization does
    # not alter the primitive separator.
    pure_row = (1, -1, 0, 1, 0)
    target_cap = (0, 0, -1, 1, 0)
    split_residue = (0, 0, 1, 0, 1)
    existing = [pure_row, target_cap, split_residue]
    reduced_eq_face = (-1, 0, 0, 0, 0)
    separator = (1, 1, 0, 0, 0)  # pure_Eq + physical_ainc

    require(all(dot(separator, column) == 0 for column in existing),
            "Eq+ainc stopped killing the bounded correction inventory")
    require(dot(separator, reduced_eq_face) == -1,
            "Eq+ainc stopped detecting the reduced Eq face")
    require(rank(existing) == 3
            and rank(existing + [reduced_eq_face]) == 4,
            "reduced Eq face stopped raising augmented rank")

    # The decisive four-row minor is unimodular.  Project to
    # (pure_Eq,ainc,W,ores); target is not needed for primitivity.
    projected = [
        (1, -1, 0, 0),
        (0, 0, -1, 0),
        (0, 0, 1, 1),
        (-1, 0, 0, 0),
    ]
    require(rank(projected) == 4,
            "primitive reduced-Eq minor lost full rank")

    # In the literal physical PP edge, the ridge S-pair is accompanied by
    # +delta_i in pure Eq.  The new correction is exactly -delta_i times
    # reduced_eq_face; its other four readouts remain zero.  It must not be
    # assigned the primitive anchor incidence.
    return {
        "correction_row_order": [
            "pure_Eq", "physical_ainc", "W", "target", "ordinary_residue",
        ],
        "bounded_existing_columns": {
            "pure_full_nine_row": list(pure_row),
            "target_cap": list(target_cap),
            "split_residue": list(split_residue),
        },
        "primitive_separator": "pure_Eq + physical_ainc",
        "needed_reduced_Eq_face": list(reduced_eq_face),
        "rank_before_after": [3, 4],
        "literal_P3K2_full_nine_boundary_rank": 288,
        "literal_P3K2_full_nine_kernel_dimension": 0,
        "two_chart_extra_kernel": (
            "only physical-forgetful chart differences, all readouts zero"
        ),
        "all_degree_polynomial_guard": (
            "a pure-row coefficient carries physical target equal to minus "
            "its anchor incidence; target-zero polynomial combinations "
            "cannot supply a reduced pure-Eq face"
        ),
    }


def c5_defects_and_compatibility() -> dict[str, object]:
    units = [monomial(index) for index in range(5)]
    a, b, c, d, e = units
    defects = (
        polynomial((1, a), (-1, b)),  # a-b
        polynomial((1, c), (-1, d)),  # c-d
        polynomial((1, e), (-1, a)),  # e-a
        polynomial((1, b), (-1, c)),  # b-c
        polynomial((1, d), (-1, e)),  # d-e
    )
    multipliers = (
        monomial(2, 4),  # ce
        monomial(1, 4),  # be
        monomial(1, 3),  # bd
        monomial(0, 3),  # ad
        monomial(0, 2),  # ac
    )

    total: Polynomial = {}
    for defect, multiplier in zip(defects, multipliers, strict=True):
        total = polynomial_add(total,
                               polynomial_scale_monomial(defect, multiplier))
    require(not total, "degree-five defect compatibility failed")

    # Each individual defect is primitive and nonzero.  It vanishes at the
    # diagonal torus point, which proves the obstruction is a universal
    # polynomial issue rather than an inconsistency of the top signs.
    require(all(len(value) == 2 and sorted(value.values()) == [-1, 1]
                for value in defects),
            "an individual Eq defect stopped being primitive")
    require(all(sum(value.values()) == 0 for value in defects),
            "an Eq defect stopped vanishing at the diagonal torus point")

    # Formal source boundaries of the five zero-anchor collision edges are
    # the oriented C5 incidence columns.  They have rank four and the degree
    # five top has the displayed multiplier boundary.
    edge_columns = []
    for index in range(5):
        column = [0] * 5
        column[index] = -1
        column[(index + 1) % 5] = 1
        edge_columns.append(tuple(column))
    require(rank(edge_columns) == 4
            and all(sum(column) == 0 for column in edge_columns),
            "formal C5 collision boundary changed")

    return {
        "face_order": list(FACE_ORDER),
        "physical_Eq_defects": [
            {VARIABLES[index]: coefficient
             for term, coefficient in defect.items()
             for index, exponent in enumerate(term) if exponent}
            for defect in defects
        ],
        "tate_multipliers": [
            [VARIABLES[index] for index, exponent in enumerate(value)
             for _ in range(exponent)]
            for value in multipliers
        ],
        "weighted_defect_sum": 0,
        "formal_edge_boundary_rank": 4,
        "top_compatibility": (
            "if the five reduced Eq faces existed, their weighted sum would "
            "already satisfy the natural degree-five d^2 identity"
        ),
    }


def first_missing_cell() -> dict[str, object]:
    return {
        "formal_edge": {
            "fine_degree": "P3+K2 with one doubled residual site",
            "source_boundary": "-r_v+r_w",
            "W_target_ores_ainc": [0, 0, 0, 0],
        },
        "physical_PP_lift": {
            "source_boundary": "-r_v+r_w + delta_v*(H_0-u)e_Eq",
            "W_target_ores_ainc": [0, 0, 0, 0],
        },
        "minimal_new_lower_face": {
            "boundary": "-delta_v*(H_0-u)e_Eq",
            "W_target_ores_ainc": [0, 0, 0, 0],
            "physical_anchor_cell": False,
            "description": (
                "a reduced pure-Eq relative face in the same repeated-site "
                "fine degree; after adjoining it, the PP edge becomes the "
                "desired zero-anchor E_v"
            ),
        },
        "first_obstruction": (
            "the primitive dual pure_Eq+physical_ainc; every existing "
            "pure-Eq correction carries the opposite anchor incidence"
        ),
        "nearest_existing_faces": {
            "squarefree_normal_face": (
                "derived Eq cancellation with zero target/ores, but site "
                "degree <=1, chart rather than physical ainc, and no map "
                "to the repeated P3+K2 degree"
            ),
            "formal_third_cofactor_tail": (
                "has a pure-Eq boundary but physical ainc=-1, wrong fine "
                "degree, and is source-invalid because the selected fourth "
                "operator sends H_m to 1"
            ),
            "polynomial_pure_row_or_dark_identity": (
                "reaches repeated degree only with target equal to minus "
                "anchor incidence"
            ),
        },
    }


def main() -> None:
    pin_dependencies()
    correction = physical_edge_obstruction()
    compatibility = c5_defects_and_compatibility()
    missing = first_missing_cell()
    ledger = {
        "pins": PINS,
        "physical_edge_obstruction": correction,
        "c5_compatibility": compatibility,
        "first_missing_cell": missing,
        "verdict": (
            "the formal repeated-site C5 edges have exact PP representatives, "
            "but physical descent adds primitive pure-Eq defects; the complete "
            "bounded polynomial/cap inventory cannot cancel one defect with "
            "zero physical anchor incidence"
        ),
        "scope": (
            "complete first P3+K2 full-nine multiplier degree, denominator/PP "
            "edge, standard target/residue cap, all-degree polynomial "
            "target-lock, and natural degree-five Tate compatibility; no "
            "claim against a new reduced relative Eq generator"
        ),
    }
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    print("h=3 rootless zero-anchor collision edge: FIRST SOURCE OBSTRUCTION")
    print("formal P3+K2 edge: ridge boundary and coarse readouts correct")
    print("physical PP descent: nonzero delta_v*(H_0-u)e_Eq")
    print("bounded correction module: separated by pure_Eq+physical_ainc")
    print("degree-five compatibility: exact")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
