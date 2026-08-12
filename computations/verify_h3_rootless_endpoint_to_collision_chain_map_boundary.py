#!/usr/bin/env python3
r"""Endpoint-ridge to rootless-collision chain-map boundary at h=3.

In one selected repeated P3+K2 degree the completed endpoint bar and its
formal rootless retyping have columns

    B_v=(-t_v Omega_v,+Q_v; ores=1),
    P_v=(-r_v,+Q_v; ores=1).

Their formal difference is the clean comparison defect

    C_v=P_v-B_v=t_v Omega_v-r_v.

The two columns are not two independent literal source chains: P_v is the
rootless presentation of the same multiplier route.  The first actual
source-labelled comparison is the adjacent PP/Bianchi square.  It has
boundary C_v-C_w plus the already certified pure-Eq defect.  Existing
full-nine/cap corrections cannot remove that defect at zero physical anchor
incidence.  Even after formally adjoining the required reduced-Eq face, the
five comparison edges have C5 incidence rank four and leave the primitive
aggregate sum C_v.

This checker composes the pinned literal endpoint, first-collision, and
zero-anchor descent theorems.  It is a bounded no-go for the current typed
inventory, not for a new relative comparison generator.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "531f6e1ed9d2bc058ad4fba551e84663e397830de818ce310532a41338b2351c"
PINS = {
    "computations/verify_h3_rootless_five_ridge_response_bianchi_cokernel.py":
        "2e09f9be1ed1b57821c64dd690df7e4d6b2efebe93cb8aae9ff0a58b3190022d",
    "computations/verify_h3_rootless_single_v_site_collision_comparison_obstruction.py":
        "34d627b9b0cdf4a81fbebc7c1d37231f53ac2d04be401c3f99402b0bf28c6fbe",
    "computations/verify_h3_rootless_zero_anchor_collision_edge_source_obstruction.py":
        "8249604a56f7fc8ee8a3c66a33cb905eed6a02202c43ed81283e91c61d748180",
    "computations/verify_h3_rootless_ridge_eq_tail_attachment_composition_gate.py":
        "b1d1a62d229d9ebb3d20abbc7359503af08506fec882f629ee95a886c58490a8",
    "computations/verify_h3_rootless_five_cycle_denominator_pp_aggregate_no_go.py":
        "4f691d119469e76436e36566a1ca7307bc49a52f66b0687c1554a9e6531ec4de",
}

FACE_ORDER = (1, 3, 5, 2, 4)
MIXED = {1: 1, 2: 2, 3: 1, 4: 1, 5: 2}
VARIABLES = ("a=q12", "b=q23", "c=q34", "d=q45", "e=q15")
# h_1=bd, h_3=ad, h_5=ac, h_2=ce, h_4=be.
H_GENERATORS = (
    (0, 1, 0, 1, 0),
    (1, 0, 0, 1, 0),
    (1, 0, 1, 0, 0),
    (0, 0, 1, 0, 1),
    (0, 1, 0, 0, 1),
)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")


def rank(columns: list[tuple[int, ...]]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "ragged matrix")
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


def dot(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    return sum(a * b for a, b in zip(left, right, strict=True))


def endpoint_expansions() -> list[dict[str, object]]:
    records = []
    for v in FACE_ORDER:
        m = MIXED[v]
        # Omega_v=(pq22-pq00)-(xv0m-xv00), hence -t Omega_v
        # has the following four literal endpoint signs.  The fixed residual
        # matching N and selected C5 multiplier t are common factors.
        omega = {
            "pq:22": 1,
            "pq:00": -1,
            f"x{v}:0{m}": -1,
            f"x{v}:00": 1,
        }
        minus_omega = {label: -coefficient
                       for label, coefficient in omega.items()}
        require(sum(omega.values()) == sum(minus_omega.values()) == 0,
                ("endpoint ridge stopped being an interval boundary", v))
        records.append({
            "v": v,
            "mixed_colour": m,
            "Omega_v": omega,
            "endpoint_bar_boundary_after_common_tN_factor": minus_omega,
            "companion": "+Q_(v,N)=+t*q_(v,N)",
            "ordinary_residue": 1,
        })
    return records


def typed_single_face_comparison() -> dict[str, object]:
    # Rows are (tOmega_v, r_v, Q_(v,N), ores).  The second column is a
    # *formal retyping* of the same multiplier route, not another source
    # generator.  It is retained only to compute the chain-map defect.
    endpoint_bar = (-1, 0, 1, 1)
    rootless_retyping = (0, -1, 1, 1)
    defect = tuple(right - left for left, right in
                   zip(endpoint_bar, rootless_retyping, strict=True))
    require(defect == (1, -1, 0, 0),
            "endpoint/rootless companions stopped cancelling")
    return {
        "row_order": ["t_v*Omega_v", "rootless_r_v", "Q_(v,N)", "ores"],
        "literal_endpoint_bar": list(endpoint_bar),
        "formal_rootless_retyping": list(rootless_retyping),
        "formal_difference": list(defect),
        "difference_formula": "t_v*Omega_v-r_v",
        "target_W_ores_on_difference": [0, 0, 0],
        "source_warning": (
            "the two displayed columns are two target presentations of one "
            "multiplier route; subtracting them is precisely the missing "
            "chain homotopy, not an available source combination"
        ),
    }


def adjacent_source_square() -> dict[str, object]:
    # C_v=t_v Omega_v-r_v.  The five first source-valid comparisons are
    # adjacent C5 differences.  Their physical PP lifts carry the pure-Eq
    # defects a-b,c-d,e-a,b-c,d-e.
    edges = []
    records = []
    defects = ("a-b", "c-d", "e-a", "b-c", "d-e")
    for index, defect in enumerate(defects):
        following = (index + 1) % 5
        column = [0] * 5
        column[index] = 1
        column[following] = -1
        edges.append(tuple(column))
        records.append({
            "faces": [FACE_ORDER[index], FACE_ORDER[following]],
            "comparison_boundary": (
                f"C_{FACE_ORDER[index]}-C_{FACE_ORDER[following]}"
            ),
            "physical_PP_extra_face": f"({defect})*(H0-u)*e_Eq",
            "strict_readouts_W_tgt_ores_ainc": [0, 0, 0, 0],
        })

    aggregate = (1, 1, 1, 1, 1)
    require(rank(edges) == 4, "comparison edges stopped being C5 incidence")
    require(all(dot(aggregate, edge) == 0 for edge in edges),
            "comparison aggregate stopped killing all adjacent squares")
    vertex = (1, 0, 0, 0, 0)
    require(rank(edges + [vertex]) == 5 and dot(aggregate, vertex) == 1,
            "one comparison vertex stopped completing the edge module")

    # The closest physical correction block is ordered as
    # (pure_Eq, physical_ainc, W, target, ores).
    pure_row = (1, -1, 0, 1, 0)
    target_cap = (0, 0, -1, 1, 0)
    split_residue = (0, 0, 1, 0, 1)
    reduced_eq = (-1, 0, 0, 0, 0)
    eq_anchor_separator = (1, 1, 0, 0, 0)
    existing = (pure_row, target_cap, split_residue)
    require(all(dot(eq_anchor_separator, column) == 0
                for column in existing),
            "pure_Eq+ainc stopped killing existing corrections")
    require(dot(eq_anchor_separator, reduced_eq) == -1,
            "pure_Eq+ainc stopped detecting the reduced Eq face")

    return {
        "records": records,
        "comparison_edge_rank": rank(edges),
        "comparison_edge_cokernel": "primitive Z generated by sum_v C_v",
        "aggregate_covector": list(aggregate),
        "first_source_descent_obstruction": {
            "row_order": ["pure_Eq", "physical_ainc", "W", "target", "ores"],
            "separator": "pure_Eq+physical_ainc",
            "needed_reduced_Eq_face": list(reduced_eq),
        },
        "after_formally_adjoining_reduced_Eq": {
            "available_comparison_boundaries": [list(edge) for edge in edges],
            "rank": 4,
            "still_missing": "one vertex C_v, equivalently sum_v C_v",
        },
    }


def repeated_degree_audit() -> dict[str, object]:
    # Each neighboring pair of selected C5 face monomials has lcm degree 3
    # and site profile P3+K2 on the five odd sites.  This is exactly where
    # the endpoint companion and collision ridge can first be compared.
    cycle_edges = ((1, 2), (2, 3), (3, 4), (4, 5), (1, 5))
    records = []
    for index in range(5):
        following = (index + 1) % 5
        lcm = tuple(max(a, b) for a, b in
                    zip(H_GENERATORS[index], H_GENERATORS[following], strict=True))
        require(sum(lcm) == 3, "first comparison degree stopped being cubic")
        site_degree = {site: 0 for site in FACE_ORDER}
        for edge_index, exponent in enumerate(lcm):
            require(exponent in (0, 1), "comparison lcm stopped squarefree in edges")
            if exponent:
                for site in cycle_edges[edge_index]:
                    site_degree[site] += 1
        profile = tuple(site_degree[site] for site in sorted(site_degree))
        require(sorted(profile) == [1, 1, 1, 1, 2],
                "comparison degree stopped having P3+K2 site type")
        records.append({
            "faces": [FACE_ORDER[index], FACE_ORDER[following]],
            "cycle_exponents": list(lcm),
            "site_profile_1_to_5": list(profile),
        })
    return {
        "cycle_variables": list(VARIABLES),
        "records": records,
        "all_profiles": "P3+K2=(2,1,1,1,1) up to order",
    }


def main() -> None:
    pin_dependencies()
    ledger = {
        "pins": PINS,
        "literal_endpoint_expansions": endpoint_expansions(),
        "first_common_repeated_degree": repeated_degree_audit(),
        "single_face_comparison": typed_single_face_comparison(),
        "first_source_valid_adjacent_square": adjacent_source_square(),
        "verdict": (
            "the endpoint and rootless presentations have the exact formal "
            "difference t_v*Omega_v-r_v, but the current literal source "
            "contains only adjacent comparison squares; physical descent "
            "first leaves the reduced pure-Eq defect, and after its formal "
            "removal the primitive diagonal comparison aggregate survives"
        ),
        "minimal_new_data_in_order": [
            "zero-anchor reduced pure-Eq face for each adjacent PP square",
            "one source-labelled vertex/aggregate Omega-to-r comparison cell",
        ],
        "scope": (
            "exact endpoint bars, matching/Bianchi companions, first repeated "
            "P3+K2 collision/PP degree, complete bounded full-nine/cap descent; "
            "no claim against an enlarged relative source resolution"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    print("h=3 endpoint-to-collision chain map: TWO-STAGE OBSTRUCTION")
    print("formal single-v defect: t_v*Omega_v-r_v (Q and ores cancel)")
    print("first literal source square: adjacent defect difference + pure Eq")
    print("after reduced Eq: C5 rank 4, primitive comparison aggregate remains")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
