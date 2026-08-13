#!/usr/bin/env python3
r"""Occurrence-graph tensor audit for the reduced-Eq cone.

Write the literal pure direct-free hafnian as H0=f+G, with f one marked
matching occurrence, and distinguish

    z = the private coordinate of the contractible occurrence graph,
    U = the physical homogenizing target coordinate.

The graph row is E_g=f-z, whereas the physical Eq coefficient is

    F0=H0-U=E_g+G+(z-U).

Thus, if da=E_g and dr0=F0*e_Eq, the honest tensor-cone element
K=r0-a*e_Eq has

    dK=(G+z-U)*e_Eq,

not G*e_Eq.  The missing diagonal (z-U)*e_Eq is a primitive free cokernel
class.  Identifying z with U would impose f=U, which is not a consequence
of H0=U; the checker gives a literal direct-free C8 specialization with
H0=U=2 but f=1.

The final ledger also pins the already certified physical cost of trying to
realize that diagonal through the Hasse/endpoint inventory: endpoint ridge,
wrong residual word, source-descent unit, ordinary residue, and the later C5
comparison aggregate.  This is a sharp reduction, not a construction of a
new physical source cell.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from math import gcd
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_full_hasse_koszul_cap_totalization.py":
        "51940ce0ac8387b68e7725508db6da1a1c055ea036335bbf19750580c69e13fb",
    "computations/verify_h3_trapped_carrier_occurrence_graph_hessian_cone_gate.py":
        "ce28ff5d25bf575c280a21c0e35c6dc1ebef54eb039ac94cdc25932a61b95829",
    "computations/verify_h3_rootless_third_cofactor_bianchi_total_complex_obstruction.py":
        "ebd25f79a6fe8db936fe5601b9220f152c5349dd794bbc4e08b2095f1c1d059f",
    "computations/verify_h3_rootless_zero_anchor_collision_edge_source_obstruction.py":
        "8249604a56f7fc8ee8a3c66a33cb905eed6a02202c43ed81283e91c61d748180",
    "computations/verify_h3_rootless_endpoint_to_collision_chain_map_boundary.py":
        "be39a61df8e3723983eea7a20d405fba7ff0f3822bc90e8d48b8039177f69cfc",
    "computations/verify_h3_tau_plus_full_interface_product_bianchi_extension_gate.py":
        "32be7ef48ad9d35b8863a62889508ccdff0010d8ebff18b366e932aab8b2bf14",
    "computations/verify_h3_reduced_eq_spencer_three_projection_gate.py":
        "315508b572fa0d96b33ba83b8ac4905e59dfbf8f484023891618dbb3c6489d83",
}
EXPECTED_LEDGER_SHA256 = (
    "462cc0b1fbf4508be717109daef03acd0ad2038143c7455a16856cab3dc907ff"
)

SITES = tuple(range(8))
FORBIDDEN = frozenset((3, 6))


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns):
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


def determinant(columns):
    size = len(columns)
    require(size and all(len(column) == size for column in columns),
            "determinant needs a square matrix")
    work = [[Q(columns[column][row]) for column in range(size)]
            for row in range(size)]
    answer = Q(1)
    for column in range(size):
        pivot = next((row for row in range(column, size)
                      if work[row][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        value = work[column][column]
        answer *= value
        work[column] = [entry / value for entry in work[column]]
        for row in range(column + 1, size):
            if not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[column], strict=True)]
    require(answer.denominator == 1, "nonintegral determinant")
    return answer.numerator


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


def direct_free_matchings():
    answer = tuple(
        matching for matching in perfect_matchings(SITES)
        if FORBIDDEN not in {frozenset(edge) for edge in matching}
    )
    require(len(answer) == len(set(answer)) == 90,
            "direct-free pure occurrence count changed")
    return answer


def connected_cycle_union(left, right):
    edges = tuple(sorted(set(left) | set(right)))
    if len(edges) != 8:
        return False
    adjacency = {site: set() for site in SITES}
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    if set(map(len, adjacency.values())) != {2}:
        return False
    seen = {0}
    frontier = [0]
    while frontier:
        site = frontier.pop()
        for neighbor in adjacency[site]:
            if neighbor not in seen:
                seen.add(neighbor)
                frontier.append(neighbor)
    return len(seen) == 8


def literal_selected_occurrence_counterguard():
    occurrences = direct_free_matchings()
    marked = occurrences[0]
    partner = next(item for item in occurrences[1:]
                   if connected_cycle_union(marked, item))
    active_edges = frozenset(marked) | frozenset(partner)
    supported = tuple(
        occurrence for occurrence in occurrences
        if set(occurrence).issubset(active_edges)
    )
    require(set(supported) == {marked, partner},
            ("C8 specialization acquired another matching", supported))

    # Give the eight cycle edges weight one and every other pure edge zero.
    # Exactly the two alternating perfect matchings survive.
    f = 1
    g = len(supported) - f
    h0 = f + g
    physical_target_u = h0
    require((h0, f, g, physical_target_u, f - physical_target_u)
            == (2, 1, 1, 2, -1),
            "selected-occurrence counterguard changed")
    return {
        "literal_pure_occurrences": len(occurrences),
        "marked_matching": [list(edge) for edge in marked],
        "partner_matching": [list(edge) for edge in partner],
        "active_graph": "C8 with all eight edge weights one",
        "supported_hafnian_matchings": len(supported),
        "values": {"H0": h0, "f": f, "G": g,
                   "physical_target_U": physical_target_u,
                   "f_minus_U": f - physical_target_u},
        "conclusion": (
            "H0-U=0 does not imply the selected-occurrence equation f-U=0"
        ),
    }


def honest_graph_tensor_cone():
    # Boundary coordinates are (E_g*Eq, G*Eq, D*Eq), where
    # E_g=f-z and D=z-U.  The physical Eq row has F0=E_g+G+D.
    physical_r0 = (1, 1, 1)
    graph_tensor = (1, 0, 0)
    honest_k = tuple(left - right for left, right in
                     zip(physical_r0, graph_tensor, strict=True))
    hoped_g_only = (0, 1, 0)
    separator = (0, 1, -1)

    require(honest_k == (0, 1, 1),
            "honest graph tensor stopped leaving the diagonal debt")
    require(dot(separator, physical_r0) == 0
            and dot(separator, graph_tensor) == 0
            and dot(separator, hoped_g_only) == 1
            and dot(separator, honest_k) == 0,
            "primitive graph/target diagonal separator changed")
    require(rank((physical_r0, graph_tensor)) == 2
            and rank((physical_r0, graph_tensor, hoped_g_only)) == 3,
            "graph tensor augmented rank changed")
    require(abs(determinant((physical_r0, graph_tensor, hoped_g_only))) == 1,
            "graph tensor obstruction stopped being primitive")
    # The existing two-column lattice is saturated: its (E_g,G) minor is a
    # unit.  Hence the residual is free, not beta torsion.
    unit_minor = physical_r0[0] * graph_tensor[1] - (
        physical_r0[1] * graph_tensor[0]
    )
    require(abs(unit_minor) == 1, "graph tensor image stopped being saturated")

    return {
        "boundary_rows": ["E_g*e_Eq", "G*e_Eq", "(z-U)*e_Eq"],
        "identities": [
            "H0=f+G",
            "E_g=f-z",
            "H0-U=E_g+G+(z-U)",
            "d(a)=E_g",
            "d(r0)=(H0-U)e_Eq",
            "K=r0-a*e_Eq",
            "dK=(G+z-U)e_Eq",
        ],
        "physical_r0_boundary": list(physical_r0),
        "graph_tensor_boundary": list(graph_tensor),
        "honest_K_boundary": list(honest_k),
        "hoped_but_invalid_G_only_boundary": list(hoped_g_only),
        "primitive_separator": list(separator),
        "unit_completion_determinant": determinant(
            (physical_r0, graph_tensor, hoped_g_only)
        ),
        "image_saturated": True,
        "beta_behavior": (
            "the cokernel is primitive and free over Z, hence remains over "
            "Z[beta] and is not the cap packet's beta torsion"
        ),
        "two_interpretations_of_u": {
            "private_occurrence_graph_coordinate": (
                "the honest cone retains (z-U)e_Eq"
            ),
            "physical_target_coordinate": (
                "setting z=U turns E_g into f-U, a false selected-occurrence "
                "equation on the physical source"
            ),
            "define_G_as_H0_minus_U": (
                "then G=F0 and dK=G e_Eq is exactly the original Eq defect"
            ),
        },
    }


def rank_five_c5_edges():
    edges = []
    for index in range(5):
        column = [0] * 5
        column[index] = 1
        column[(index + 1) % 5] = -1
        edges.append(tuple(column))
    aggregate = (1,) * 5
    require(rank(edges) == 4
            and all(dot(aggregate, edge) == 0 for edge in edges),
            "C5 comparison aggregate changed")
    return edges, aggregate


def physical_landing_cost():
    # One complete endpoint route has boundary -Omega+q and ordinary
    # residue one.  This is the smallest source-labelled word-change object.
    endpoint_route = (-1, 1, 1)
    require(endpoint_route == (-1, 1, 1), "endpoint route signs changed")

    # The first physical adjacent comparison square then has a reduced-Eq
    # defect.  The complete bounded correction block is separated by
    # pure_Eq+physical_ainc.
    pure_row = (1, -1, 0, 1, 0)
    target_cap = (0, 0, -1, 1, 0)
    split_residue = (0, 0, 1, 0, 1)
    reduced_eq = (-1, 0, 0, 0, 0)
    eq_anchor = (1, 1, 0, 0, 0)
    require(all(dot(eq_anchor, column) == 0 for column in
                (pure_row, target_cap, split_residue))
            and dot(eq_anchor, reduced_eq) == -1,
            "pure-Eq/anchor separator changed")

    _edges, aggregate = rank_five_c5_edges()
    return {
        "first_source_labelled_endpoint_route": {
            "rows": ["Omega_v", "q_(v,N)", "ordinary_residue"],
            "column": list(endpoint_route),
            "forced_outputs": "-Omega_v, +q_(v,N), ordinary residue +1",
        },
        "formal_hasse_top_cost": {
            "source_valid": False,
            "endpoint_ridge_space_rank": 6,
            "primitive_Omega_rank": 5,
            "selected_midpoint_word_hits": 0,
            "descent_unit": "fourth operator sends H_m to 1",
        },
        "first_repeated_collision_square": {
            "boundary": "C_v-C_w+delta_v*(H0-U)e_Eq",
            "needed_zero_anchor_face": "-delta_v*(H0-U)e_Eq",
            "separator": "pure_Eq+physical_ainc",
        },
        "after_granting_reduced_Eq_faces": {
            "comparison_edge_rank": 4,
            "primitive_survivor": "sum_v C_v",
            "aggregate_covector": list(aggregate),
        },
        "next_physical_theorem": (
            "construct a source-labelled occurrence-to-target diagonal "
            "comparison in the same word/fine/repeated grade whose complete "
            "endpoint ridge, residual word, descent, target, ordinary "
            "residue, W, and anchor faces totalize; after edge transport it "
            "must also hit the primitive C5 comparison aggregate"
        ),
    }


def audit_pinned_statements():
    full = (ROOT / (
        "computations/verify_h3_tau_plus_full_interface_product_bianchi_extension_gate.py"
    )).read_text()
    third = (ROOT / (
        "computations/verify_h3_rootless_third_cofactor_bianchi_total_complex_obstruction.py"
    )).read_text()
    occurrence = (ROOT / (
        "computations/verify_h3_trapped_carrier_occurrence_graph_hessian_cone_gate.py"
    )).read_text()
    require('"source_valid": False' in full
            and '"endpoint_ridge_space_rank": 6' in full
            and '"Omega_obstruction_rank": 5' in full
            and '"selected_midpoint_word_hits": 0' in full,
            "full even-orbit obstruction ledger changed")
    require('"physical_top": "J_M=1"' in third
            and '"identity": "J_M=d_M(d_pq H_m)=d_{pq,xv,N}H_m=1"'
            in third,
            "third-cofactor descent unit ledger changed")
    require('"equation": "R=f+G=0"' in occurrence
            and '"E=f-u=0", "M=G+u=0"' in occurrence,
            "committed occurrence graph stopped being a private-pivot graph")


def main() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative,
                                     actual, expected))
    audit_pinned_statements()
    ledger = {
        "theorem": "reduced-Eq occurrence-graph derived-tensor gate",
        "pins": PINS,
        "literal_counterguard": literal_selected_occurrence_counterguard(),
        "honest_derived_tensor": honest_graph_tensor_cone(),
        "forced_physical_corrections": physical_landing_cost(),
        "verdict": (
            "the Koszul subtraction is valid only with distinct private "
            "graph coordinate z and physical target U, and then gives "
            "dK=(G+z-U)e_Eq.  The hoped dK=G e_Eq silently identifies z=U; "
            "that would impose the false selected-occurrence equation f=U. "
            "The first new obstruction beyond the common Eq coefficient is "
            "the primitive occurrence-to-target diagonal (z-U)e_Eq; the "
            "known physical routes add endpoint-ridge/word/descent debts and "
            "ultimately leave the C5 comparison aggregate"
        ),
        "K_Eq_beta_constructed": False,
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("unexpected ledger digest", digest, EXPECTED_LEDGER_SHA256))
    print("h3 reduced-Eq occurrence-graph tensor gate: PASS")
    print("honest cone: dK=(G+z-U)e_Eq, not G e_Eq")
    print("primitive next obstruction: (z-U)e_Eq")
    print("setting z=U is source-invalid: H0=U does not imply f=U")
    print("physical promotion still forces ridge/word/descent and C5 aggregate")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
