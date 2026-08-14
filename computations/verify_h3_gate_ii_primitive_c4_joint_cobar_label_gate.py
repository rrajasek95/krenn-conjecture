#!/usr/bin/env python3
"""Audit the proposed Gate-II joint primitive-C4/two-root carrier.

After granting the termwise-PP-natural selected ``db01`` carrier and the
same-grade direct ``U_C4`` cap, the remaining direction half of ``dL01`` is

    2 d(D q01) H - d(p0 s1) H - d(p1 s0) H,

with six terms in each chart.  At coefficient level there is a canonical
face-complete C4 shadow: duplicate the direct chart for the two root orders
and pair each copy once with each endpoint chart.  Its alternating charge
projects to ``(2,-1,-1)``.

This checker tests the extra datum needed to promote that shadow to one
physical source-labelled two-root cobar orbit.  Literal site-root edges
preserve the structural occurrence tag and the D/P/S/Q operation profile.
Every edge of the proposed C4 instead changes ``DQ`` to ``PS``.  The exact
complete-row quotient retains the resulting charge, with a normalized
dual detector.  Thus primitive-C4 boundary completion supplies the formal
mate graph but not the two physical chart-switch arrows.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_gate_ii_uniform_response_relative_carrier_landing_gate.py":
        "9b9c05a6789d2ade9359934f279eeb429591b2e85651ebaba8485195050417eb",
    "computations/verify_h3_h2_l01_three_cap_first_pp_curvature_gate.py":
        "59babf6e706973f2eaa8a8fdd7cdb624ddf88560c08243c5fcd05c3a5425a5d7",
    "computations/verify_h2_labelled_two_direction_occurrence_hasse_cobar_square_gate.py":
        "77d13c31df34efa26b575497bdd7bb2cc9173e8d1907030541444551c7417804",
    "computations/verify_uniform_signed_matching_holonomy_boundary_counterguard.py":
        "12bb763f3ca2f2dde30f6a8f932fd6d8b9fa3c970e1e3aab2f46592bcde93547",
    "computations/verify_uniform_boundary_complete_flat_even_component_theorem.py":
        "08db6dd78869d5d236d43fe8ae91e1e944d2b60d16a7f5f7a684f766a4187530",
    "computations/verify_uniform_primitive_c4_source_label_wandering_counterguard.py":
        "f5a780c40f7be8a959e56e47ce06ff04ae644694d0f30c20180df0bd1259491b",
}
EXPECTED_LEDGER_SHA256 = (
    "595771f49fd81aa9ce0dfaa29d03a848905f10f976b96fd3cf6107b6ecc642e2"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def vector(width: int, values: dict[int, int | Q]):
    return tuple(Q(values.get(index, 0)) for index in range(width))


def dot(left, right):
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def rank(columns) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank width")
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


def direction_face_inventory() -> dict[str, object]:
    curvature = load(
        "computations/verify_h3_h2_l01_three_cap_first_pp_curvature_gate.py",
        "gate_ii_joint_curvature",
    )
    matchings, directions, tails, l01, _r01, _ah = curvature.polynomial_data()
    differential = curvature.differential(l01)
    selected_sites = {0, 1, 6, 7}
    direction_half = {
        label: coefficient for label, coefficient in differential.items()
        if set(label[1]).issubset(selected_sites)
    }
    coefficients = (Q(2), Q(-1), Q(-1))
    chart_names = ("A=D*q01", "B=p0*s1", "C=p1*s0")
    records = []
    union = set()
    for name, chart, coefficient in zip(
            chart_names, directions, coefficients, strict=True):
        chart_matchings = {
            tuple(sorted(chart + tail)) for tail in tails
        }
        labels = tuple(sorted(
            (label for label in direction_half if label[0] in chart_matchings),
            key=repr,
        ))
        require(len(labels) == 6
                and all(direction_half[label] == coefficient
                        for label in labels),
                ("direction chart census changed", name, labels))
        union.update(labels)
        records.append({
            "chart": name,
            "operation_profile_DPSQ": (
                [1, 0, 0, 1] if name.startswith("A=")
                else [0, 1, 1, 0]
            ),
            "residual_C4_tails": len(tails),
            "direction_factors_per_tail": 2,
            "support": len(labels),
            "coefficient": str(coefficient),
        })
    require(len(matchings) == 105 and len(direction_half) == 18
            and union == set(direction_half),
            "the 18-term direction packet changed")
    edge_marginals = {}
    for (_matching, edge), coefficient in direction_half.items():
        edge_marginals[edge] = edge_marginals.get(edge, Q(0)) + coefficient
    ordered_edges = ((6, 7), (0, 1), (0, 6), (1, 7), (1, 6), (0, 7))
    marginals = tuple(edge_marginals[edge] for edge in ordered_edges)
    require(marginals == tuple(map(Q, (6, 6, -3, -3, -3, -3))),
            ("direction marginals changed", marginals))
    return {
        "support": len(direction_half),
        "charts": records,
        "direction_edge_order": ["dD", "dq01", "dp0", "ds1", "dp1", "ds0"],
        "direction_marginals": [str(value) for value in marginals],
        "primitive_marginals": [2, 2, -1, -1, -1, -1],
        "chart_charge": [2, -1, -1],
    }


def formal_primitive_c4_shadow() -> dict[str, object]:
    # Two ordered direct-chart copies and the two endpoint charts.
    vertices = ("A_[a|b]", "A_[b|a]", "B", "C")
    tau_a = (2, 3, 0, 1)  # (Aab B)(Aba C)
    tau_b = (3, 2, 1, 0)  # (Aab C)(Aba B)
    flat = load(
        "computations/verify_uniform_boundary_complete_flat_even_component_theorem.py",
        "gate_ii_joint_flat",
    )
    components = flat.audit_family(4, (tau_a, tau_b))
    require(len(components) == 1 and components[0]["bipartite"]
            and components[0]["rank"] == 3
            and components[0]["shore_sizes"] == [2, 2],
            ("formal C4 stopped being flat", components))

    mate_edges = ((0, 2), (1, 3), (0, 3), (1, 2))
    mate_rows = tuple(vector(4, {left: 1, right: 1})
                      for left, right in mate_edges)
    charge = tuple(map(Q, (1, 1, -1, -1)))
    require(rank(mate_rows) == 3
            and sum(charge, Q(0)) == 0
            and all(dot(charge, row) == 0 for row in mate_rows),
            "the formal primitive-C4 charge changed")
    projection = (
        (Q(1), Q(1), Q(0), Q(0)),
        (Q(0), Q(0), Q(1), Q(0)),
        (Q(0), Q(0), Q(0), Q(1)),
    )
    projected_charge = tuple(dot(row, charge) for row in projection)
    projected_rows = tuple(
        tuple(dot(row, mate) for row in projection) for mate in mate_rows
    )
    require(projected_charge == tuple(map(Q, (2, -1, -1)))
            and set(projected_rows) == {
                tuple(map(Q, (1, 1, 0))),
                tuple(map(Q, (1, 0, 1))),
            },
            ("the matching shadow projection changed", projected_charge,
             projected_rows))
    return {
        "vertices": list(vertices),
        "mate_involutions": {
            "tau_a": [[vertices[0], vertices[2]], [vertices[1], vertices[3]]],
            "tau_b": [[vertices[0], vertices[3]], [vertices[1], vertices[2]]],
        },
        "face_complete_flat_component": True,
        "incidence_rank": rank(mate_rows),
        "alternating_charge": [str(value) for value in charge],
        "projection_A_B_C": [str(value) for value in projected_charge],
        "projected_mate_row_types": ["A+B", "A+C"],
        "meaning": (
            "this is a smallest coefficient shadow of L01; its "
            "alternating charge is the relative Tate class, not yet a "
            "physical source-labelled top cell"
        ),
    }


def physical_source_label_gate() -> dict[str, object]:
    square = load(
        "computations/verify_h2_labelled_two_direction_occurrence_hasse_cobar_square_gate.py",
        "gate_ii_joint_labelled_square",
    )
    square_ledger, square_digest = square.audit()
    require(square_digest == square.EXPECTED_LEDGER_SHA256
            and square_ledger["occurrence_tag_preserved_at_all_vertices"]
            and square_ledger["ordered_bar_realization"]["d_squared"] == 0,
            "the literal two-root tag-preservation theorem changed")

    profiles = {
        "A_[a|b]": (1, 0, 0, 1),
        "A_[b|a]": (1, 0, 0, 1),
        "B": (0, 1, 1, 0),
        "C": (0, 1, 1, 0),
    }
    mate_edges = (
        ("A_[a|b]", "B"), ("A_[b|a]", "C"),
        ("A_[a|b]", "C"), ("A_[b|a]", "B"),
    )
    violations = tuple((left, right) for left, right in mate_edges
                       if profiles[left] != profiles[right])
    require(violations == mate_edges,
            ("a proposed mate unexpectedly preserved its physical tag",
             violations))

    signed = load(
        "computations/verify_uniform_signed_matching_holonomy_boundary_counterguard.py",
        "gate_ii_joint_signed_boundary",
    )
    boundary = signed.audit_exact_boundary_counterguard()
    uniform_boundary = signed.audit_uniform_identity()
    require(boundary["boundary_identity"] == "L*R=B*D=-B*F=-1"
            and boundary["closed_holonomy_circuits"] == 0
            and uniform_boundary["free_monoid_identity"] == "L*R=B*D",
            "the exact signed primitive-C4 boundary identity changed")

    wandering = load(
        "computations/verify_uniform_primitive_c4_source_label_wandering_counterguard.py",
        "gate_ii_joint_wandering",
    )
    packet = wandering.audit_exact_packet()
    require(packet["retained_tail_cycle"] == ["01", "23", "45"]
            and packet["common_window_sites"] == []
            and not packet["common_ordered_endpoint_pair"]
            and not packet["is_complete_ternary_source"],
            "the exact primitive-C4 source-label counterguard changed")
    return {
        "literal_two_root_invariant": (
            "each root recolours one literal factor while preserving its "
            "structural occurrence tag and D/P/S/Q operation profile"
        ),
        "proposed_vertex_profiles_DPSQ": {
            key: list(value) for key, value in profiles.items()
        },
        "proposed_mate_edges": [list(edge) for edge in mate_edges],
        "profile_violations": len(violations),
        "root_cobar_edges_realized": 0,
        "first_missing_physical_labels": [
            "Hasse[2](D,Q01) <-> Hasse[2](P0,S1)",
            "Hasse[2](D,Q01) <-> Hasse[2](P1,S0)",
        ],
        "primitive_completion_guard": {
            "exact_boundary_identity": boundary["boundary_identity"],
            "top_binomial_closed_holonomy_circuits":
                boundary["closed_holonomy_circuits"],
            "retained_tail_cycle": packet["retained_tail_cycle"],
            "C4_windows": packet["C4_windows"],
            "common_window_sites": packet["common_window_sites"],
            "conclusion": (
                "unique signed mates for the top and both boundary faces "
                "do not force one common physical source placement"
            ),
        },
    }


def complete_row_counterguard() -> dict[str, object]:
    words = ("00", "10", "01", "11")
    charts = ("A", "B", "C")
    coordinates = tuple((word, chart) for chart in charts for word in words)
    index = {coordinate: position
             for position, coordinate in enumerate(coordinates)}
    width = len(coordinates)

    complete_rows = tuple(vector(width, {
        index[(word, chart)]: 1 for chart in charts
    }) for word in words)
    square_edges = (("00", "10"), ("00", "01"),
                    ("10", "11"), ("01", "11"))
    root_rows = []
    for chart in charts:
        for source, target in square_edges:
            root_rows.append(vector(width, {
                index[(source, chart)]: -1,
                index[(target, chart)]: 1,
            }))
    root_rows = tuple(root_rows)
    base_rows = root_rows + complete_rows
    candidate = vector(width, {
        index[("00", "A")]: 2,
        index[("00", "B")]: -1,
        index[("00", "C")]: -1,
    })
    detector = tuple(Q((2, -1, -1)[charts.index(chart)])
                     for chart in charts for _word in words)
    require(rank(root_rows) == 9 and rank(base_rows) == 10
            and rank(base_rows + (candidate,)) == 11
            and all(dot(detector, row) == 0 for row in base_rows)
            and dot(detector, candidate) == 6,
            "the exhaustive complete-row counterguard changed")

    switch_ab = vector(width, {
        index[("00", "A")]: 1, index[("00", "B")]: 1,
    })
    switch_ac = vector(width, {
        index[("00", "A")]: 1, index[("00", "C")]: 1,
    })
    one_ab_rank = rank(base_rows + (switch_ab,))
    one_ab_with_candidate = rank(base_rows + (switch_ab, candidate))
    one_ac_rank = rank(base_rows + (switch_ac,))
    one_ac_with_candidate = rank(base_rows + (switch_ac, candidate))
    both_rank = rank(base_rows + (switch_ab, switch_ac))
    both_with_candidate = rank(base_rows + (switch_ab, switch_ac, candidate))
    require((one_ab_rank, one_ab_with_candidate) == (11, 12)
            and (one_ac_rank, one_ac_with_candidate) == (11, 12)
            and (both_rank, both_with_candidate) == (12, 12),
            "the two chart-switch necessity gate changed")
    return {
        "coordinates": "four two-root words times three physical chart tags",
        "root_edge_rank": rank(root_rows),
        "rank_after_complete_response_rows": rank(base_rows),
        "rank_after_L01_direction_charge": rank(base_rows + (candidate,)),
        "dual": {
            "constant_chart_values_A_B_C": [2, -1, -1],
            "kills_every_tag_preserving_root_edge": True,
            "kills_every_complete_response_row": True,
            "value_on_candidate": str(dot(detector, candidate)),
            "normalized_value": "1",
        },
        "chart_switch_test": {
            "only_A_plus_B_rank_then_with_candidate": [
                one_ab_rank, one_ab_with_candidate,
            ],
            "only_A_plus_C_rank_then_with_candidate": [
                one_ac_rank, one_ac_with_candidate,
            ],
            "both_switches_rank_then_with_candidate": [
                both_rank, both_with_candidate,
            ],
            "conclusion": (
                "both projected mate types A+B and A+C are necessary and "
                "sufficient at coefficient level; neither is supplied by "
                "the exhaustive tag-preserving two-root/complete-row map"
            ),
        },
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h3 Gate-II primitive-C4 joint cobar source-label gate",
        "pins": PINS,
        "eighteen_direction_faces": direction_face_inventory(),
        "formal_primitive_C4_shadow": formal_primitive_c4_shadow(),
        "physical_source_label_gate": physical_source_label_gate(),
        "smallest_complete_row_counterguard": complete_row_counterguard(),
        "verdict": (
            "The granted selected db01 carrier and same-grade U_C4 cap have "
            "a canonical coefficient-level primitive-C4 mate shadow.  Its "
            "alternating charge projects to 2A-B-C and hence has exactly the "
            "required eighteen direction-factor faces.  It is not one "
            "source-labelled two-root cobar orbit: literal root edges "
            "preserve occurrence and D/P/S/Q tags, whereas every required "
            "mate edge changes the direct DQ chart to an endpoint PS chart. "
            "Complete response rows plus every tag-preserving root edge leave "
            "this charge detected.  Primitive signed boundary completion "
            "does not cure the defect, because its unique mates need not "
            "share one physical C4 window or endpoint pair"
        ),
        "first_physical_label_obstruction": (
            "the two independent source-provenant mixed chart arrows "
            "DQ<->P0S1 and DQ<->P1S0, together with their primitive boundary "
            "mates in one common action-site C4 window"
        ),
        "shortest_positive_datum": (
            "a source-provenant chart-switch bicomplex containing both mixed "
            "arrows DQ<->P0S1 and DQ<->P1S0, natural for the two site-root PP "
            "operators, with all four mixed commutator faces and signed mates "
            "on one fixed tail/window.  Its formal C4 charge then projects to "
            "L01 and closes the eighteen-term packet; the committed word-0102 "
            "and dq/Q/ores descent can then start"
        ),
        "accepted_terminal_now": False,
        "scope": (
            "exact canonical h=3 local K8 direction packet, rational complete-"
            "row/two-root quotient, pinned literal occurrence square, and "
            "pinned Gaussian-integer primitive-C4 wandering guard.  A formal "
            "matching mate is not promoted to a physical chart-switch map"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("joint primitive-C4/cobar ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    print("h3 Gate-II primitive-C4 joint cobar label gate: PASS")
    print("direction-factor packet: 18 = 6 DQ + 6 P0S1 + 6 P1S0")
    print("formal flat C4 charge projects to (2,-1,-1): PASS")
    print("physical two-root orbit: OBSTRUCTED BY D/P/S/Q SOURCE TAG")
    print("complete-row rank: 10 -> 11 after L01 direction charge")
    print("needed mixed chart arrows: DQ<->P0S1 and DQ<->P1S0")
    print("accepted terminal: " + str(ledger["accepted_terminal_now"]).upper())
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
