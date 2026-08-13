#!/usr/bin/env python3
"""Keep tau-plus pure columns separate from endpoint Q-tail Bianchi rows.

The untyped six-tail identity

    B0 + ((B1-B0)+(B4-B0))/2 = (B1+B4)/2

is correct.  Its two sides do not live in the same physical chain row.
Tau-plus sends a collision label to a pure full-nine row/multiplier column;
each such column has a literal 90-term, seven-edge boundary.  Endpoint
matching-Bianchi differences instead have only the Q-tail output of an
endpoint bar; their coefficients are three-edge multiplier monomials.

This checker freezes the direct-sum typing obstruction, the exact primitive
dual, and the independent protected-two-root guard.  It does not exclude a
new relative cell whose *pure-column* boundary is the required difference.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_trace_cartan_tau_plus_site_collapse_gate.py":
        "f0801bfcd5362f2fc8d9a81bf85a84b2d380fd37cbbe7db2252b352b785d5474",
    "computations/verify_h3_trace_cartan_even_repair_denominator_tor_gate.py":
        "673b30ac4b68c8a3af42e9c0803b3d5a39796b366b3ac15b5fd8b31b02d8df5d",
    "computations/verify_h3_rootless_ridge_eq_tail_attachment_composition_gate.py":
        "b1d1a62d229d9ebb3d20abbc7359503af08506fec882f629ee95a886c58490a8",
    "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py":
        "719e48963faac5cd1dc5e7348de41e86f690f3046fefba88dddfa60bae532899",
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
    "computations/verify_h3_cut_swap_support_tail_lift_shared_loop_gate.py":
        "db23eb4e760dd84934426a80516aad355486e947626da1849454718b512efb2d",
    "computations/verify_h3_shared_repair_residue_scope_and_fan_q_independence.py":
        "f78869532f809e1fffabe914521a1e7361815bbe187dbb72140d693975e0c2e7",
    "computations/verify_h3_trace_cartan_even_repair_relative_c4_scope_gate.py":
        "645df036367a7fe60f3ce625dc37710f7e83129a84a3619005945ca6b4f0a486",
}
EXPECTED_LEDGER_SHA256 = (
    "ab24571975754e9d9e1f45ff0a137d0d78990d4d104916ff1568a88055424f1d"
)


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


def add(*vectors):
    return tuple(sum(Q(vector[index]) for vector in vectors)
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def dot(left, right):
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def unit(index: int, size: int = 6):
    return tuple(Q(int(position == index)) for position in range(size))


def typed(*, pure=None, q_tail=None):
    zero = (Q(0),) * 6
    return tuple((zero if pure is None else pure)
                 + (zero if q_tail is None else q_tail))


def graph(multiplier):
    return tuple(sorted((left, right)
                        for left, right, _left_colour, _right_colour
                        in multiplier))


def permute_edge(edge, permutation):
    left, right = edge
    return tuple(sorted((permutation[left], permutation[right])))


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    tau = load(
        "computations/verify_h3_trace_cartan_tau_plus_site_collapse_gate.py",
        "tau_bianchi_typing_tau",
    )
    complete = load(
        "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py",
        "tau_bianchi_typing_complete",
    )
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "tau_bianchi_typing_base",
    )
    ridge = load(
        "computations/verify_h3_rootless_ridge_eq_tail_attachment_composition_gate.py",
        "tau_bianchi_typing_ridge",
    )
    independence = load(
        "computations/verify_h3_shared_repair_residue_scope_and_fan_q_independence.py",
        "tau_bianchi_typing_independence",
    )

    tau_ledger, tau_digest = tau.audit()
    require(tau_digest == tau.EXPECTED_LEDGER_SHA256
            and tau_ledger["canonical_13_label_landing"]["missing_labels"]
                == [[2, [0, 1]], [10, [0, 4]]]
            and tau_ledger["smallest_relative_repair"]
                ["per_omitted_label_image"] == "(B1+B4)/2",
            "the tau-plus omitted-pair target changed")

    left, right, left_cell, _right_cell = complete.CUBIC_PAIRS[1]
    target_degree = complete.degree_add(
        base.lambda_degree(left),
        complete.cell_degree(complete.CYCLE_CELLS[left_cell]),
    )
    component = complete.component(base, target_degree)
    pure = tuple((multiplier, boundary)
                 for word, multiplier, boundary in component["columns"]
                 if word == complete.PURE_WORD)
    require((left, right) == (3, 5)
            and len(component["columns"]) == 288
            and len(pure) == 6,
            "the canonical pure-column component changed")
    pure_graphs = tuple(graph(multiplier) for multiplier, _boundary in pure)
    graph_index = {value: index for index, value in enumerate(pure_graphs)}
    require(len(graph_index) == 6,
            "the canonical pure multiplier graphs collided")

    # A B_i in tau-plus is a source column label.  Its literal differential
    # is a 90-term complete full-nine boundary.  Each feature appends a
    # four-edge matching to the three-edge P3+K2 multiplier.
    for multiplier, boundary in pure:
        require(len(multiplier) == 3
                and len(boundary) == len(set(boundary)) == 90
                and {len(feature) for feature in boundary} == {7}
                and multiplier not in boundary,
                "a pure B column lost its 3-edge/90-by-7-edge typing")

    # Reconstruct the only endpoint routes entering this canonical target.
    # This grants the graph/fine placement used by the proposed translation.
    routes = []
    for position, left_face in enumerate(ridge.FACE_ORDER):
        right_face = ridge.FACE_ORDER[(position + 1) % 5]
        for face, other in ((left_face, right_face),
                            (right_face, left_face)):
            multiplier = ridge.FIRST_TOR_MULTIPLIERS[
                (left_face, right_face)
            ][(face, other)]
            for matching in ridge.perfect_matchings(
                    tuple(site for site in ridge.ODD if site != face)):
                route_graph = tuple(sorted(matching + (multiplier,)))
                if route_graph in graph_index:
                    routes.append((face, graph_index[route_graph]))
    by_face = {}
    for face, target in routes:
        by_face.setdefault(face, set()).add(target)
    require(by_face == {3: {0, 4, 5}, 5: {0, 1, 2}},
            ("the canonical endpoint route packets changed", by_face))

    # Endpoint bars have (-Omega,+Q_tail; ores=1).  Differences on a fixed
    # face cancel Omega and ordinary residue, but remain in the Q_tail row.
    endpoint_bar = ridge.vector(endpoint_Omega=-1, Q_tail=1, ores=1)
    route_difference = add(endpoint_bar, scale(-1, endpoint_bar))
    require(not any(route_difference)
            and ridge.ROWS.index("Q_tail") != ridge.ROWS.index("Eq"),
            "the endpoint route output-row typing changed")

    desired = scale(Q(1, 2), add(unit(1), unit(4)))
    h0 = scale(Q(1, 2), add(
        add(unit(1), scale(-1, unit(0))),
        add(unit(4), scale(-1, unit(0))),
    ))
    h5 = scale(Q(1, 2), add(
        add(unit(1), scale(-1, unit(5))),
        add(unit(4), scale(-1, unit(5))),
    ))
    require(add(unit(0), h0) == desired
            and add(unit(5), h5) == desired,
            "the untyped six-tail arithmetic changed")

    # Typed direct sum: pure full-nine column labels and endpoint Q tails are
    # not identified.  The proposed H0/H5 corrections have zero pure part.
    bypass0 = typed(pure=unit(0))
    bypass5 = typed(pure=unit(5))
    correction0 = typed(q_tail=h0)
    correction5 = typed(q_tail=h5)
    desired_typed = typed(pure=desired)
    require(add(bypass0, correction0) != desired_typed
            and add(bypass5, correction5) != desired_typed,
            "an endpoint Q tail became a pure full-nine column homotopy")

    # Primitive physical-row dual.  It ignores every Q-tail coordinate,
    # kills B0 and B5, and detects the desired fixed-column average by one.
    lambda_fixed = tuple((Q(0), Q(1), Q(0), Q(0), Q(1), Q(0))
                         + (Q(0),) * 6)
    require(dot(lambda_fixed, bypass0) == dot(lambda_fixed, bypass5) == 0
            and dot(lambda_fixed, correction0)
                == dot(lambda_fixed, correction5) == 0
            and dot(lambda_fixed, desired_typed) == 1,
            "the pure-column/Q-tail separator changed")

    # Target involution alone does not type its source lift.  It moves the
    # selected face 5 to face 2 and the normalized C5 to a different cycle.
    site_action = {1: 1, 2: 5, 3: 3, 4: 4, 5: 2}
    cycle = frozenset(((1, 2), (2, 3), (3, 4), (4, 5), (1, 5)))
    moved_cycle = frozenset(permute_edge(edge, site_action) for edge in cycle)
    require(site_action[5] == 2 and moved_cycle != cycle,
            "the target involution unexpectedly fixed the selected C5 chart")

    independent = independence.audit_q_comparison_independence()
    require(independent["q_comparison_defect"] == [0] * 6
            and independent["same_q_data_bad_aggregate_residue_rank"] == 1
            and independent[
                "bad_map_contains_fixed_or_paired_repair_direction"] is False,
            "the protected-two-root/labelled-residue independence guard changed")

    ledger = {
        "theorem": "tau-plus matching-Bianchi tail chain-typing guard",
        "pins": PINS,
        "tau_plus_required_image": {
            "omitted_labels": [[2, [0, 1]], [10, [0, 4]]],
            "local_bypass_pure_columns": ["B0", "B5"],
            "desired_per_label_pure_column": "(B1+B4)/2",
            "module": "pure full-nine row/multiplier columns",
            "literal_boundary_terms_per_B": 90,
            "literal_boundary_edge_degree": 7,
        },
        "endpoint_matching_Bianchi": {
            "face3_targets": sorted(by_face[3]),
            "face5_targets": sorted(by_face[5]),
            "H0": [str(value) for value in h0],
            "H5": [str(value) for value in h5],
            "module": "endpoint Q_tail coefficient monomials",
            "coefficient_edge_degree": 3,
            "Omega_target_anchor_W_ores_on_same_face_difference": 0,
            "untyped_Q6_identity": "B0+H0=B5+H5=(B1+B4)/2",
            "typed_pure_column_identity": False,
        },
        "primitive_typed_dual": {
            "row_order": [
                *(f"pure_B{index}" for index in range(6)),
                *(f"Q_tail_B{index}" for index in range(6)),
            ],
            "lambda": [str(value) for value in lambda_fixed],
            "on_local_B0_B5_bypasses": [0, 0],
            "on_H0_H5_Q_tail_corrections": [0, 0],
            "on_desired_pure_average": 1,
        },
        "source_covariance_guard": {
            "target_action": "(B0 B5)(B2 B3), B1,B4 fixed",
            "site_action": "(2 5)",
            "face5_image": "face2",
            "selected_C5_chart_fixed": False,
            "status": (
                "H5 additionally needs a transformed source-chart theorem; "
                "granting it does not remove the direct-sum row obstruction"
            ),
        },
        "protected_two_root_independence": independent,
        "exact_remaining_cell": (
            "after a local B0/B5 relative-C4 bypass, construct an exact-word/"
            "fine/repeated-grade protected homotopy whose PURE-COLUMN image "
            "is (B1+B4)/2-B0 and its rho mate; equivalently land directly "
            "on (B1+B4)/2.  A Q-tail matching difference is not this cell"
        ),
        "verdict": (
            "matching-Bianchi proves the displayed coefficient/tail equality "
            "only after forgetting the physical output row.  It does not "
            "retire delta-plus or weighted denominator membership, and the "
            "protected two-root Phi/q theorem independently does not supply "
            "a primal pure-column or labelled-residue section"
        ),
        "nonclaims": [
            "a larger relative source resolution may contain the pure-column homotopy",
            "weighted denominator Tor is unnecessary if a direct pure-column repair is separately constructed",
            "the local relative-C4 bypass itself remains a hypothesis",
        ],
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("tau-plus Bianchi typing ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h3 tau-plus Bianchi tail: UNTYPED IDENTITY ONLY")
    print("tau-plus B_i: pure full-nine column with 90 seven-edge boundaries")
    print("matching-Bianchi H_i: endpoint Q-tail, three-edge coefficient row")
    print("typed dual on desired (B1+B4)/2: 1")
    print("delta-plus / weighted Tor retired: NO")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
