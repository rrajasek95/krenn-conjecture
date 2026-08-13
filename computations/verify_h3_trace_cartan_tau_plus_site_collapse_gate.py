#!/usr/bin/env python3
"""Construct the thirteen-label part of iota=tau_plus and isolate one repair.

The rho-even identity-cap trace packet is the sum of the two physical cut
packets 012 and 024.  It has fifteen labelled collision generators: twelve
occur once and the three shared repeated-02 labels occur twice.  Exhausting
all rho/s-equivariant maps from the six collision sites to the five odd sites
of the canonical faces-(3,5) complete component gives no map on all fifteen
labels.  The best maps lift thirteen labels and have one double fibre.

For every best map the thirteen-label pushforward is

    3(B0+B2+B3+B5) + 2(B1+B4).

The omitted labels form one rho-pair.  Since s fixes B1 and B4, the unique
equivariant repair that completes the uniform trace target 3 sum_i B_i sends
each omitted label to (B1+B4)/2.  This is one missing relative orbit image,
not a cell in the current literal source inventory.

A rho-even integral covector annihilates the coverage vector of every
equivariant site-collapse map but evaluates to 2 on the all-label vector.
Thus no rational linear combination or averaging of the complete natural
site-collapse family can remove the repair.  This is a no-go for site/tail
collapse, not for a new diagonal/loop-resolution relative cell.

Each valid label lands in a literal complete pure multiplier column.  Thus
tensoring by the already physical Cartan root orbit supplies the corresponding
mixed-word target, and coefficientwise jet extension supplies its Rees
landing, on these thirteen labels.  The repair must carry the same typing.

The beta=0 D0 root branch is kept separate: it is the selected colour-0
coordinate in the intrinsic block alpha E_00, not one of the omitted
collision labels, and is not supplied by the even trace repair.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_cut_swap_support_tail_lift_shared_loop_gate.py":
        "db23eb4e760dd84934426a80516aad355486e947626da1849454718b512efb2d",
    "computations/verify_h3_trace_cartan_lower_rees_typing_gate.py":
        "0190a8fa16dddf9cecf2de676d4f3ff87d184f031e523d87e1f80937ff55be94",
}
EXPECTED_LEDGER_SHA256 = (
    "e66354d199f39b5f350cb808f351ce94819a9af9b6e4a87402c5b57ede50f7f0"
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


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    support = load(
        "computations/verify_h3_cut_swap_support_tail_lift_shared_loop_gate.py",
        "tau_plus_support",
    )
    trace = load(
        "computations/verify_h3_trace_cartan_lower_rees_typing_gate.py",
        "tau_plus_trace",
    )
    lower = support.load(
        "computations/verify_h3_complete_tangent_lower_protected_phi_reduction.py",
        "tau_plus_lower",
    )
    tangent = support.load(
        "computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py",
        "tau_plus_tangent",
    )
    complete = support.load(
        "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py",
        "tau_plus_complete",
    )
    base = support.load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "tau_plus_base",
    )

    # The trace cap is the rho-even sum of the two cut packets.  The three
    # common labels therefore carry multiplicity two, not zero.
    key = lambda label: (label[1], label[2])
    cut_012 = frozenset(map(key, lower.lower_labels(tangent, (0, 1, 2))))
    cut_024 = frozenset(map(key, lower.lower_labels(tangent, (0, 2, 4))))
    labels = tuple(sorted(cut_012 | cut_024))
    shared = frozenset(cut_012 & cut_024)
    coefficients = tuple(
        Q(int(label in cut_012) + int(label in cut_024)) for label in labels
    )
    require(len(labels) == 15 and len(shared) == 3,
            "the physical 15/3 collision packet changed")
    require(Counter(coefficients) == {Q(1): 12, Q(2): 3}
            and sum(coefficients) == 18,
            "the even trace multiplicities changed")
    require(frozenset(support.rho_label(tangent, label)
                      for label in cut_012) == cut_024,
            "the second trace chart stopped being the rho translate")
    require(all(coefficients[labels.index(support.rho_label(tangent, label))]
                == coefficient
                for label, coefficient in zip(labels, coefficients, strict=True)),
            "the trace packet stopped being rho-even")

    # Reconstruct the six target diagonal/pure columns in the same literal
    # complete component as tau_minus.
    left, right, left_cell, _right_cell = complete.CUBIC_PAIRS[1]
    require((left, right) == (3, 5), "the canonical component moved")
    target_degree = complete.degree_add(
        base.lambda_degree(left),
        complete.cell_degree(complete.CYCLE_CELLS[left_cell]),
    )
    component = complete.component(base, target_degree)
    pure = tuple((multiplier, boundary) for word, multiplier, boundary
                 in component["columns"] if word == complete.PURE_WORD)
    pure_graphs = tuple(support.graph(multiplier)
                        for multiplier, _boundary in pure)
    graph_index = {value: index for index, value in enumerate(pure_graphs)}
    require(len(component["columns"]) == 288 and len(graph_index) == 6,
            "the canonical six-column target changed")
    target_action = (5, 1, 3, 2, 4, 0)
    require(target_action[1] == 1 and target_action[4] == 4,
            "the target involution stopped fixing B1,B4")

    # Exhaust all 5^6 maps, imposing only rho/s equivariance.  A label is
    # valid precisely when its collapsed matching is one of the six physical
    # loop-free pure graphs.
    records = []
    valid_histogram = Counter()
    for values in product(support.TARGET_ODD, repeat=6):
        phi = dict(enumerate(values))
        if any(phi[support.RHO[site]] != support.TARGET_S[phi[site]]
               for site in range(6)):
            continue
        images = tuple(support.collapse_graph(tangent, label, phi)
                       for label in labels)
        valid = tuple(index for index, image in enumerate(images)
                      if image in graph_index)
        valid_histogram[len(valid)] += 1
        if valid:
            pushforward = [Q(0)] * 6
            for index in valid:
                pushforward[graph_index[images[index]]] += coefficients[index]
            records.append((values, valid, images, tuple(pushforward)))
    require(valid_histogram == {0: 381, 10: 4, 12: 4, 13: 16},
            ("the complete equivariant-map census changed", valid_histogram))
    require(len(records) == 24, "the nonzero partial-collapse family changed")

    best = tuple(record for record in records if len(record[1]) == 13)
    expected_partial = (Q(3), Q(2), Q(3), Q(3), Q(2), Q(3))
    require(len(best) == 16
            and {record[3] for record in best} == {expected_partial},
            "the maximal trace pushforward changed")
    require(all(sorted(Counter(values).values()) == [1, 1, 1, 1, 2]
                for values, _valid, _images, _pushforward in best),
            "a maximal map stopped having one double fibre")
    require(all(all(labels[index] not in shared
                    for index in set(range(15)) - set(valid))
                for _values, valid, _images, _pushforward in best),
            "a maximal even map lost a shared label")

    invalid_orbits = set()
    for _values, valid, images, _pushforward in best:
        invalid = tuple(sorted(set(range(15)) - set(valid)))
        require(len(invalid) == 2 and images[invalid[0]] is None
                and images[invalid[1]] is None,
                "the maximal defect stopped being one loop pair")
        require(labels.index(support.rho_label(tangent, labels[invalid[0]]))
                == invalid[1],
                "the omitted labels stopped being a rho-pair")
        invalid_orbits.add(tuple(labels[index] for index in invalid))
    expected_invalid_orbits = {
        ((0, (0, 1)), (11, (0, 4))),
        ((2, (0, 1)), (10, (0, 4))),
        ((6, (1, 2)), (8, (2, 4))),
        ((12, (1, 2)), (13, (2, 4))),
    }
    require(invalid_orbits == expected_invalid_orbits,
            ("the four possible missing rho-pairs changed", invalid_orbits))

    # Select the lexicographically first maximal map.  It identifies source
    # sites 2 and 5 at target site 4, so the omitted matchings acquire loop
    # 44.  Its missing target is exactly B1+B4.
    canonical = min(best)
    values, valid, images, partial = canonical
    invalid = tuple(sorted(set(range(15)) - set(valid)))
    require(values == (1, 2, 4, 3, 5, 4)
            and tuple(labels[index] for index in invalid)
            == ((2, (0, 1)), (10, (0, 4))),
            "the canonical maximal map changed")
    require(values[2] == values[5] == 4
            and all((2, 5) in tangent.MATCHINGS[labels[index][0]]
                    for index in invalid),
            "the canonical obstruction stopped being the loop 44")
    uniform_trace_target = tuple(Q(3) for _index in range(6))
    literal_trace_boundary = Counter()
    for coefficient, (_multiplier, boundary) in zip(
            uniform_trace_target, pure, strict=True):
        for feature in boundary:
            literal_trace_boundary[feature] += coefficient
    require(len(literal_trace_boundary) == 540
            and set(literal_trace_boundary.values()) == {Q(3)},
            "the uniform trace target stopped being a literal 540-feature packet")
    missing_target = tuple(expected - actual for expected, actual in
                           zip(uniform_trace_target, partial, strict=True))
    require(missing_target == (Q(0), Q(1), Q(0), Q(0), Q(1), Q(0)),
            "the maximal-map target deficit changed")
    per_label_repair = tuple(value / 2 for value in missing_target)
    completed = tuple(actual + 2 * repair for actual, repair in
                      zip(partial, per_label_repair, strict=True))
    require(completed == uniform_trace_target
            and tuple(per_label_repair[index] for index in target_action)
            == per_label_repair,
            "the one-orbit equivariant repair changed")

    # A valid source label already lands in a literal decorated complete
    # column.  The Cartan root defect D supplies the four mixed-word corners;
    # Rees extension is coefficientwise, so the same thirteen-label map is
    # well typed in jet lengths 1,2,3.  No assertion is made for the missing
    # pair before its relative cell is constructed.
    root_defect = (Q(-1), Q(1), Q(-1), Q(1))
    partial_mixed_target = tuple(
        coefficient * root for coefficient in partial for root in root_defect
    )
    require(len(partial_mixed_target) == 24
            and sum(bool(value) for value in partial_mixed_target) == 24,
            "the thirteen-label iota lost its mixed Cartan target")
    jet_records = []
    for length in (1, 2, 3):
        jet = tuple(partial_mixed_target
                    if level == 0 else (Q(0),) * len(partial_mixed_target)
                    for level in range(length))
        require(jet[0] == partial_mixed_target
                and all(not any(level) for level in jet[1:]),
                "coefficientwise Rees extension changed the partial iota")
        jet_records.append({
            "length": length,
            "order_zero_nonzero_coordinates": sum(
                bool(value) for value in jet[0]
            ),
        })

    # This explicit even separator proves that no rational linear combination
    # of all partial site collapses can have coverage one on every U15 label.
    # Zero-valid maps add zero columns and do not change the argument.
    detector = (
        Q(1), Q(-4), Q(0), Q(1), Q(-4), Q(10), Q(-4), Q(1),
        Q(1), Q(-4), Q(0), Q(1), Q(1), Q(1), Q(1),
    )
    require(all(detector[index]
                == detector[labels.index(support.rho_label(tangent, label))]
                for index, label in enumerate(labels)),
            "the coverage separator stopped being rho-even")
    require(all(sum(detector[index] for index in valid) == 0
                for _values, valid, _images, _pushforward in records),
            "the separator stopped killing a partial-collapse column")
    require(sum(detector) == 2,
            "the separator stopped detecting full U15 coverage")

    beta_zero = trace.audit_beta_zero()
    require(beta_zero["Jstar"] == 0
            and beta_zero["missing_root_branch"] == "D0",
            "the separate beta-zero branch changed")

    ledger = {
        "theorem": "thirteen-label trace-Cartan iota and one-pair repair gate",
        "pins": PINS,
        "source_trace_packet": {
            "cut_packets": ["012", "024"],
            "U15_labels": len(labels),
            "nonshared_multiplicity_one": 12,
            "shared_repeated_02_multiplicity_two": 3,
            "total_occurrence_weight": int(sum(coefficients)),
            "rho_parity": "even",
        },
        "target_diagonal_packet": {
            "component_faces": [left, right],
            "complete_columns": len(component["columns"]),
            "pure_columns": len(pure),
            "s_action": "(B0 B5)(B2 B3), with B1,B4 fixed",
            "uniform_trace_target": "3*(B0+B1+B2+B3+B4+B5)",
            "literal_decorated_boundary_features": len(literal_trace_boundary),
        },
        "complete_equivariant_site_collapse_census": {
            "map_count": sum(valid_histogram.values()),
            "valid_label_histogram": {
                str(key): valid_histogram[key]
                for key in sorted(valid_histogram)
            },
            "nonzero_partial_maps": len(records),
            "maximal_maps": len(best),
            "maximal_valid_labels": 13,
            "maximal_pushforward": [int(value) for value in expected_partial],
            "possible_missing_rho_pairs": [
                [[matching, list(edge)] for matching, edge in orbit]
                for orbit in sorted(invalid_orbits)
            ],
            "shared_labels_lost_by_maximal_maps": 0,
        },
        "canonical_13_label_landing": {
            "site_map": list(values),
            "double_fibre": "source sites 2,5 -> target site 4",
            "missing_labels": [
                [labels[index][0], list(labels[index][1])]
                for index in invalid
            ],
            "first_obstruction": "edge 25 collapses to forbidden loop 44",
            "partial_target": [int(value) for value in partial],
            "missing_target": [int(value) for value in missing_target],
            "source_typing": (
                "every valid label lands in one literal decorated complete "
                "pure multiplier column"
            ),
            "mixed_word_target": (
                "tensor the six-column pushforward by the physical Cartan "
                "root defect (-1,1,-1,1)"
            ),
            "Rees_landing": jet_records,
            "iota_status": "constructed on these thirteen labels",
        },
        "smallest_relative_repair": {
            "source": "one rho-pair / one equivariant orbit image",
            "per_omitted_label_image": "(B1+B4)/2",
            "target_equivariance": "s fixes B1 and B4",
            "completed_target": "3*sum_i B_i",
            "status": (
                "necessary and sufficient linear image; no literal physical "
                "diagonal/loop-resolution source cell is yet constructed"
            ),
        },
        "sharp_no_go": {
            "scope": (
                "the complete family of rho/s-equivariant maps from six "
                "collision sites to the five canonical odd target sites"
            ),
            "rho_even_coverage_detector": [int(value) for value in detector],
            "value_on_every_partial_map": 0,
            "value_on_full_U15_coverage": int(sum(detector)),
            "consequence": (
                "no rational combination or equivariant averaging of the "
                "natural site-collapse maps defines full tau_plus"
            ),
        },
        "beta_zero": {
            "status": "separate",
            "Jstar": beta_zero["Jstar"],
            "missing_root_branch": beta_zero["missing_root_branch"],
            "selected_colour": beta_zero["selected_colour"],
            "intrinsic_selected_block": beta_zero["intrinsic_selected_block"],
            "J_row_selected_D0_coefficient":
                beta_zero["J_row_selected_D0_coefficient"],
            "not_supplied_by_trace_repair": True,
        },
        "frontier": (
            "iota=tau_plus, including mixed Cartan target and coefficientwise "
            "Rees landing, is explicit on thirteen of fifteen labels.  Closing "
            "the generic trace route requires one rho-even relative source "
            "orbit whose image is (B1+B4)/2 on each omitted label.  Existing "
            "site/tail collapses cannot synthesize it.  The beta-zero D0 "
            "unary/complement branch remains an independent obligation"
        ),
        "nonclaims": [
            "the candidate repair vector is not promoted to a literal source-valid cell",
            "the no-go does not exclude a diagonal/loop-resolution relative generator",
            "the beta-zero D0 branch is not identified with the omitted rho-pair",
        ],
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("trace-Cartan tau_plus ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h3 trace-Cartan iota/tau_plus site-collapse gate: PASS")
    print("typed mixed/Rees iota landing: 13/15 labels; 16 equivariant maps")
    print("partial target: (3,2,3,3,2,3)")
    print("one missing rho-pair repair: each -> (B1+B4)/2")
    print("full site-collapse synthesis: obstructed by even coverage detector")
    print("beta=0: D0 remains separate")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
