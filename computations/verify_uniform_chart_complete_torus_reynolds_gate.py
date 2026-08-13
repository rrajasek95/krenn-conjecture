#!/usr/bin/env python3
"""Obstruct a chart-complete Spencer cell built by diagonal torus projection.

Let R be the complete hafnian on an even complete graph.  A diagonal
one-parameter source gauge assigns an additive weight w_ij to every edge.
It makes R homogeneous exactly when all perfect matchings have the same
weight.  The matching-exchange equations force

                         w_ij = a_i + a_j.

Consequently D*q01, p0*s1 and p1*s0 have the same weight, even after every
q-variable compensation.  The same is true after tensoring with a tail and
after passing to Kahler direction flags, because dx_ij has weight w_ij.

Thus no fibre-preserving torus/Reynolds projector isolates R01, L01, or the
endpoint-even kappa=(2,2,-1,-1,-1,-1) Spencer packet.  A weight that
distinguishes A from B or C violates the first four-cycle homogeneity
equation.  Its normal face is the already isolated pointed L01 chart reset,
not a new physical boundary.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_response_h2_chart_direction_spencer_packet_gate.py":
        "46b53933a080d0b8eeceee695ecd0d4c6d72224d7d0fea4352176b410b8b7fe4",
    "notes/uniform-response-h2-chart-direction-spencer-packet-gate.md":
        "d57b734cbbb99f5088cdd01e803522ffcd5b55dc2123525ae6d744de6e9a0445",
    "computations/verify_h3_h2_l01_endpoint_flag_s4_cplus_span_gate.py":
        "3ab94cb5293deeef5777588c15e308e4ac8974ffcff4272ee021432b6633089d",
    "notes/h3-h2-l01-endpoint-flag-s4-cplus-span-gate.md":
        "dcbb22545c23d209f2ee3cf654f00d4d76cae8b200dc886214abda9a7016c29f",
    "computations/verify_h3_h2_fixed_chart_l01_reset_augmented_gate.py":
        "6acd2eec727e1030c58d14da6a2c8b26f884bb0ed5ada02b904c5e4c54d6ca6f",
    "notes/h3-h2-fixed-chart-l01-reset-augmented-gate.md":
        "110e850f43b4520a5a47e53d74f190ae7012547ff87d27da1e27ba4c5568f701",
    "computations/verify_h3_h2_full_site_chart_swap_pointed_scalar_guard.py":
        "bc35781e0f57bbd1202711e2dc818417d76fa87c69e33d3d4b01540e06865557",
    "notes/h3-h2-full-site-chart-swap-pointed-scalar-guard.md":
        "77771f8eee2a4bbaeb5a9575961efb9c7728833e28bca86d33102806aeffa6c2",
}
EXPECTED_LEDGER_SHA256 = (
    "f43adf164b65b124cde6d69032d8ed98b45b896adcd9bc686d17fc5f972a7e20"
)

Edge = tuple[int, int]
Vector = tuple[Q, ...]


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


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
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def rank(rows: tuple[Vector, ...]) -> int:
    if not rows:
        return 0
    work = [list(map(Q, row)) for row in rows]
    width = len(work[0])
    require(all(len(row) == width for row in work), "rank width")
    pivot = 0
    for column in range(width):
        selected = next((row for row in range(pivot, len(work))
                         if work[row][column]), None)
        if selected is None:
            continue
        work[pivot], work[selected] = work[selected], work[pivot]
        value = work[pivot][column]
        work[pivot] = [entry / value for entry in work[pivot]]
        for row in range(len(work)):
            if row == pivot or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right
                         in zip(work[row], work[pivot], strict=True)]
        pivot += 1
        if pivot == len(work):
            break
    return pivot


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


def complete_graph_audit(number_vertices: int) -> dict[str, object]:
    require(number_vertices >= 6 and number_vertices % 2 == 0,
            number_vertices)
    vertices = tuple(range(number_vertices))
    edges = tuple((left, right) for left in vertices
                  for right in vertices if left < right)
    edge_position = {edge: index for index, edge in enumerate(edges)}
    matchings = tuple(perfect_matchings(vertices))
    incidence = tuple(tuple(Q(edge in matching) for edge in edges)
                      for matching in matchings)
    base = incidence[0]
    differences = tuple(tuple(value - base[index]
                              for index, value in enumerate(row))
                        for row in incidence[1:])

    number_edges = len(edges)
    expected_difference_rank = number_edges - number_vertices
    require(rank(differences) == expected_difference_rank,
            (number_vertices, rank(differences), expected_difference_rank))

    # Vertex gauges w_ij=a_i+a_j span the entire common-matching-weight
    # space.  The map is injective for a complete graph with >=3 vertices.
    vertex_gauges = tuple(tuple(Q(vertex in edge) for edge in edges)
                          for vertex in vertices)
    require(rank(vertex_gauges) == number_vertices
            and all(sum(difference[index] * gauge[index]
                        for index in range(number_edges)) == 0
                    for difference in differences
                    for gauge in vertex_gauges)
            and rank(differences + vertex_gauges) == number_edges,
            "common matching weights stopped being vertex gauges")
    require(all(len({sum(row[index] * gauge[index]
                         for index in range(number_edges))
                     for row in incidence}) == 1
                for gauge in vertex_gauges),
            "a vertex gauge stopped giving one matching character")

    # Every vertex gauge has matching weight sum_i a_i.  Requiring the
    # common character to be zero cuts its dimension from n to n-1; this is
    # the exact condition for the normalized affine equation R=1.
    affine_constraint = base
    require(rank(differences + (affine_constraint,))
            == expected_difference_rank + 1,
            "the affine fibre character constraint changed")

    # The distinguished four direction vertices are P,S,0,1 = 0,1,2,3.
    p_site, s_site, zero_site, one_site = 0, 1, 2, 3
    a_pair = ((p_site, s_site), (zero_site, one_site))
    b_pair = ((p_site, zero_site), (s_site, one_site))
    c_pair = ((p_site, one_site), (s_site, zero_site))
    pair_vectors = []
    for pair in (a_pair, b_pair, c_pair):
        vector = [Q(0)] * number_edges
        for edge in pair:
            vector[edge_position[tuple(sorted(edge))]] += 1
        pair_vectors.append(tuple(vector))
    ab_exchange = tuple(left - right for left, right
                        in zip(pair_vectors[0], pair_vectors[1], strict=True))
    ac_exchange = tuple(left - right for left, right
                        in zip(pair_vectors[0], pair_vectors[2], strict=True))
    require(all(sum(exchange[index] * gauge[index]
                        for index in range(number_edges)) == 0
                for exchange in (ab_exchange, ac_exchange)
                for gauge in vertex_gauges),
            "a vertex gauge began distinguishing A,B,C")

    # Completing the three two-edge pairings by one common tail makes three
    # literal response matchings.  Their differences are exactly two rows
    # in the homogeneity-relation space.
    tail_vertices = vertices[4:]
    tail = next(perfect_matchings(tail_vertices))
    local_matchings = tuple(tuple(sorted(pair + tail))
                            for pair in (a_pair, b_pair, c_pair))
    local_incidence = tuple(tuple(Q(edge in matching) for edge in edges)
                            for matching in local_matchings)
    local_relations = tuple(tuple(left - right for left, right
                                 in zip(local_incidence[0], row, strict=True))
                            for row in local_incidence[1:])
    require(rank(local_relations) == 2
            and rank(differences + local_relations) == rank(differences),
            "the A/B/C four-cycle relations left response homogeneity")

    return {
        "vertices": number_vertices,
        "edges": number_edges,
        "perfect_matchings": len(matchings),
        "matching_difference_rank": rank(differences),
        "common_weight_space_dimension": number_edges - rank(differences),
        "vertex_gauge_rank": rank(vertex_gauges),
        "common_weights_equal_vertex_gauges": True,
        "normalized_affine_fibre_weight_dimension": (
            number_edges - rank(differences + (affine_constraint,))
        ),
        "local_pairings": [repr(pair) for pair in (a_pair, b_pair, c_pair)],
        "local_AB_exchange_is_homogeneity_relation": True,
        "local_AC_exchange_is_homogeneity_relation": True,
    }


def h3_reynolds_audit() -> dict[str, object]:
    # Write the explicit compensating gauge law.  It proves directly that
    # endpoint rescalings and arbitrary residual q compensations do not
    # distinguish the three direction pairings.
    names = ("P", "S", "0", "1", "2", "3", "4", "5")
    potentials = tuple(Q(index + 1) for index in range(8))
    potential = dict(zip(names, potentials, strict=True))
    weight = lambda left, right: potential[left] + potential[right]
    a_weight = weight("P", "S") + weight("0", "1")
    b_weight = weight("P", "0") + weight("S", "1")
    c_weight = weight("P", "1") + weight("S", "0")
    require(a_weight == b_weight == c_weight,
            "the explicit endpoint/q compensation stopped balancing")
    tail_weight = weight("2", "3") + weight("4", "5")
    require(a_weight + tail_weight == sum(potentials, Q(0)),
            "the full matching gauge weight changed")

    # In Kahler/PP degree, dx transforms by the same character as x.  Each
    # differentiated matching therefore retains the full matching weight.
    direction_terms = (
        ("dD", ("0", "1")),
        ("dq01", ("P", "S")),
        ("dp0", ("S", "1")),
        ("ds1", ("P", "0")),
        ("dp1", ("S", "0")),
        ("ds0", ("P", "1")),
    )
    varied_edge = {
        "dD": ("P", "S"), "dq01": ("0", "1"),
        "dp0": ("P", "0"), "ds1": ("S", "1"),
        "dp1": ("P", "1"), "ds0": ("S", "0"),
    }
    pp_weights = tuple(
        weight(*varied_edge[label]) + weight(*survivor) + tail_weight
        for label, survivor in direction_terms
    )
    require(len(set(pp_weights)) == 1
            and pp_weights[0] == sum(potentials, Q(0)),
            "the PP flag acquired a new torus character")

    # A Reynolds character projector is scalar on one character space.  In
    # the homogeneous R=0 fibre it returns the whole response row or zero.
    # In an affine R=1 fibre the common character must be trivial, so its
    # invariant projector is the identity on every occurrence and PP flag.
    return {
        "edge_weight_law": {
            "D": "a_P+a_S",
            "p_i": "a_P+a_i",
            "s_i": "a_S+a_i",
            "q_ij": "a_i+a_j",
        },
        "A_weight": "a_P+a_S+a_0+a_1",
        "B_weight": "a_P+a_S+a_0+a_1",
        "C_weight": "a_P+a_S+a_0+a_1",
        "all_six_PP_flag_weights_equal": True,
        "homogeneous_zero_fibre_Reynolds": "whole response character or zero",
        "normalized_affine_fibre_Reynolds": "identity on every occurrence",
        "R01_is_weight_subspace": False,
        "L01_is_obtained_from_complete_R_by_Reynolds": False,
        "kappa_packet_is_obtained_from_complete_dR_by_Reynolds": False,
        "first_failed_tangency": (
            "wt(Dq01)-wt(p0s1) and wt(Dq01)-wt(p1s0), the two K4 "
            "four-cycle exchange conormals"
        ),
        "endpoint_even_minimum": (
            "under endpoint/root transpose the two exchange conormals agree; "
            "their centered combination is the single pointed L01 face"
        ),
    }


def pinned_scope_audit() -> dict[str, object]:
    uniform = load(
        "computations/verify_uniform_response_h2_chart_direction_spencer_packet_gate.py",
        "torus_uniform_spencer",
    )
    uniform_ledger, uniform_digest = uniform.audit()
    require(uniform_digest == uniform.EXPECTED_LEDGER_SHA256,
            "the uniform Spencer packet changed")
    packet = uniform_ledger["direction_packet"]
    require(packet["kappa"] == [2, 2, -1, -1, -1, -1]
            and packet["tail_matrix_rank"] == 1,
            "the uniform kappa packet changed")

    endpoint = load(
        "computations/verify_h3_h2_l01_endpoint_flag_s4_cplus_span_gate.py",
        "torus_endpoint_flag",
    )
    endpoint_ledger, endpoint_digest = endpoint.audit()
    require(endpoint_digest == endpoint.EXPECTED_LEDGER_SHA256
            and endpoint_ledger["candidate_span"]
                ["equals_L01_direction_primitive"],
            "the endpoint flag theorem changed")

    # The committed 3c60c7e file is content-pinned above.  Its own older
    # transitive pins were superseded later in the shared history, so do not
    # execute that historical checker here.  The theorem it froze has ledger
    # 94f11d... and the present matching calculation independently recovers
    # its Euler rank 21 as difference-rank 20 plus the complete row.
    fixed_ledger_digest = (
        "94f11da21af93ef6d07b68b6d4d42c3362e4095360798b1decb4aecdacf5e6fe"
    )
    return {
        "uniform_Spencer_ledger": uniform_digest,
        "endpoint_flag_ledger": endpoint_digest,
        "fixed_chart_Euler_ledger": fixed_ledger_digest,
        "compatibility": (
            "the torus homogeneity no-go is stronger than failure of one "
            "chosen site gauge and compatible with the 12-occurrence Euler "
            "dual: every fibre-preserving torus is already vertex gauge"
        ),
        "augmented_scope": (
            "failure occurs at complete-response tangency before physical "
            "q, anchor, W, ridge, or eta/sigma can be transported"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    # K10 already gives 945 matching rows.  The proof is the four-cycle
    # identity above; these three exact instances guard the formula without
    # making every checker mode eliminate a 10395 by 66 rational matrix.
    orders = tuple(complete_graph_audit(number_vertices)
                   for number_vertices in (6, 8, 10))
    require(orders[1] == {
        "vertices": 8,
        "edges": 28,
        "perfect_matchings": 105,
        "matching_difference_rank": 20,
        "common_weight_space_dimension": 8,
        "vertex_gauge_rank": 8,
        "common_weights_equal_vertex_gauges": True,
        "normalized_affine_fibre_weight_dimension": 7,
        "local_pairings": [
            "((0, 1), (2, 3))", "((0, 2), (1, 3))",
            "((0, 3), (1, 2))",
        ],
        "local_AB_exchange_is_homogeneity_relation": True,
        "local_AC_exchange_is_homogeneity_relation": True,
    }, orders[1])
    ledger = {
        "theorem": "uniform chart-complete torus/Reynolds no-go",
        "pins": PINS,
        "complete_matching_weight_spaces": orders,
        "h3_physical_gauge_and_PP": h3_reynolds_audit(),
        "pinned_scope": pinned_scope_audit(),
        "verdict": (
            "Every diagonal torus that preserves a complete response row is "
            "a vertex gauge.  Endpoint scalings with arbitrary compensating "
            "q scalings therefore give identical characters to A=Dq01, "
            "B=p0s1 and C=p1s0, and to all six Kahler direction flags.  No "
            "Reynolds/weight projector isolates R01, L01, or kappa tensor H. "
            "A separating weight violates the first four-cycle response "
            "homogeneity relation and leaves the already known pointed L01 "
            "normal face."
        ),
        "minimal_no_go": (
            "the endpoint-even K4 four-cycle conormal "
            "wt(Dq01)-wt(p0s1)=wt(Dq01)-wt(p1s0).  Setting it nonzero is "
            "exactly leaving the fixed response fibre; setting it zero makes "
            "the torus action scalar on the desired packet"
        ),
        "shortest_positive_theorem": (
            "a non-diagonal, source-labelled Spencer/cobar comparison whose "
            "complete lower face includes the cross-chart C2+/C4/P2 "
            "companions.  Diagonal gauge and Reynolds constructions are "
            "exhausted before augmented readouts"
        ),
        "scope": (
            "exact diagonal algebraic-torus actions on complete even "
            "hafnian response rows, their Kahler flags, and the pinned h3 "
            "physical coefficient interface.  It does not exclude the "
            "required non-diagonal higher Spencer comparison."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("complete-response homogeneous torus: VERTEX GAUGE ONLY")
    print("A/B/C and all six PP flags: ONE COMMON CHARACTER")
    print("R01/L01/kappa Reynolds isolation: IMPOSSIBLE")
    print("first failed tangency: endpoint-even K4 four-cycle = L01")
    print("non-diagonal chart-complete Spencer family: STILL REQUIRED")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
