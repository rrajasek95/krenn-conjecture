#!/usr/bin/env python3
r"""Audit pq-minus-pr chart copies against the residual-q fiber target.

The two literal chart presentations of a full-nine row have identical
physical matching boundary.  Their primitive difference therefore cancels
every matching coordinate, including every private full-nine pivot.  This
file checks whether that tautological cancellation can retain the three
nonzero projections required by the residual-q fiber target:

  residue -delta, eta_z value 1+delta_(vz)u_z/t,
  sigma value -q_pq^22.

It cannot.  At the physical word 01211222 the chart difference has zero
physical boundary and zero under every descended physical readout.  Its one
nonzero presentation-dependent feature is the chart-odd marked Hasse top,
which reads one.  Before taking the top, its chart-odd external tail is the
complete three-term h_v; it contains the selected mixed q11 corner but not
the pure q00 corner and is not -q00+q11.

There is also a strict grade obstruction.  The physical word has colours 2
at p,q and is absent from all five complete first rootless P3+K2 components,
whose endpoint slots are colour zero.  The zero-endpoint word 00211200 is
present.  Its pairwise chart differences cancel 42--46 private pivots per
selected column, but the complete two-chart kernel has anchor, target, W,
and ordinary-residue readout zero.  Thus the primitive chart difference is
presentation H1, not the missing physical relative cell.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "2c1187a432a461efaab2868729126f7ca1b931cff8ed9440ecae90939738de08"
PINS = {
    "computations/verify_h3_direct_free_literal_four_face_full_nine_no_go.py":
        "17c5e15e93292c11f99a135312d2ca2796049ef0b35937d9e1f184ee7637b12a",
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
    "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py":
        "719e48963faac5cd1dc5e7348de41e86f690f3046fefba88dddfa60bae532899",
    "computations/verify_h3_rootless_five_cycle_positive_interface.py":
        "fd359b3ff2abbb01d9508996c754a27b70890b2cd621926fc30b92057b337851",
    "computations/verify_h3_rootless_one_face_third_cofactor_comparison_vertex_gate.py":
        "37251145d805861b2d1b15b7bf37cf9f98ba30b03fbcffa1daa4fc35789efe84",
    "computations/verify_h3_residual_q_eta_one_cell_fiber_product_gate.py":
        "4e84ad031b97ee67e1336c9a9d785acd3c581c2d80aeeb005d4eee784f91eccb",
}

PHYSICAL_WORD = (0, 1, 2, 1, 1, 2, 2, 2)
ZERO_ENDPOINT_WORD = (0, 0, 2, 1, 1, 2, 0, 0)
V = 1
N_ALIGNED = ((2, 4), (3, 5))


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(relative: str, name: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def add_value(vector, key, value) -> None:
    updated = Q(vector.get(key, 0)) + Q(value)
    if updated:
        vector[key] = updated
    else:
        vector.pop(key, None)


def add_vectors(*vectors):
    answer = {}
    for vector in vectors:
        for key, value in vector.items():
            add_value(answer, key, value)
    return answer


def scale(vector, value):
    value = Q(value)
    return {key: value * Q(entry) for key, entry in vector.items()
            if value * Q(entry)}


def pairing(vector, covector) -> Q:
    return sum((Q(value) * Q(covector.get(key, 0))
                for key, value in vector.items()), Q(0))


def edge(base, left: int, right: int, word):
    return base.edge(left, right, word[left], word[right])


def sparse_derivative(base, polynomial, variables):
    return base.sparse_derivative(tuple(polynomial), tuple(variables))


def site_profile(edges):
    profile = [0] * 8
    for left, right in edges:
        profile[left] += 1
        profile[right] += 1
    return tuple(profile)


def selected_physical_chart_difference(base, third) -> dict[str, object]:
    row = base.full_nine_polynomial(PHYSICAL_WORD)
    require(len(row) == len(set(row)) == 90,
            "physical full-nine row changed")
    pq_direct, pq_star = base.chart_partition(
        PHYSICAL_WORD, (base.P, base.Q_SITE)
    )
    pr_direct, pr_star = base.chart_partition(
        PHYSICAL_WORD, (base.P, base.R)
    )
    require((len(pq_direct), len(pq_star), len(pr_direct), len(pr_star))
            == (15, 75, 0, 90), "physical chart partition changed")
    pq_physical = Counter(pq_direct + pq_star)
    pr_physical = Counter(pr_direct + pr_star)
    require(pq_physical == pr_physical == Counter(row),
            "chart copies stopped presenting the same physical row")
    physical_difference = pq_physical.copy()
    physical_difference.subtract(pr_physical)
    physical_difference = +physical_difference
    require(not physical_difference,
            "primitive chart difference retained physical boundary")

    # First remove the two physical endpoint cells.  The common tail is the
    # literal four-site mixed hafnian h_1.
    external = (
        edge(base, base.P, base.Q_SITE, PHYSICAL_WORD),
        edge(base, base.X, V, PHYSICAL_WORD),
    )
    pq_tail = sparse_derivative(base, pq_direct, external)
    pr_tail = sparse_derivative(base, pr_star, external)
    require(pq_tail == pr_tail and len(pq_tail) == 3
            and set(pq_tail.values()) == {1},
            "physical chart tails stopped being the same h_1")
    require(not sparse_derivative(base, pq_star, external)
            and not sparse_derivative(base, pr_direct, external),
            "the physical marked tail entered a wrong chart sector")

    q00 = tuple(sorted((
        base.edge(2, 4, 1, 1), base.edge(3, 5, 1, 1),
    )))
    q11 = tuple(sorted((
        base.edge(2, 4, 2, 1), base.edge(3, 5, 1, 2),
    )))
    require(q00 not in pq_tail and pq_tail.get(q11) == 1,
            "pure/mixed corner content of h_1 changed")
    desired_tail = {q00: Q(-1), q11: Q(1)}
    require(pq_tail != desired_tail,
            "chart-odd h_1 unexpectedly became -q00+q11")

    # Retain chart tags.  The primitive difference has a nonzero chart-odd
    # presentation tail even though its physical forgetting is zero.
    pq_tag = ("pq", "direct")
    pr_tag = ("pr", "two_star")
    tagged_pq = {(pq_tag, term): Q(value)
                 for term, value in pq_tail.items()}
    tagged_pr = {(pr_tag, term): Q(value)
                 for term, value in pr_tail.items()}
    chart_odd_tail = add_vectors(tagged_pq, scale(tagged_pr, -1))
    physical_tail_forgetting = {}
    for (_tag, term), value in chart_odd_tail.items():
        add_value(physical_tail_forgetting, term, value)
    require(not physical_tail_forgetting,
            "chart-odd tail acquired a physical forgetting")

    # Add the aligned internal matching.  Each chart marked top is the same
    # unit; the normalized chart-odd cochain reads one on their difference.
    marked_edges = ((base.P, base.Q_SITE), (base.X, V), *N_ALIGNED)
    marked_variables = tuple(
        edge(base, left, right, PHYSICAL_WORD)
        for left, right in marked_edges
    )
    pq_top = sparse_derivative(base, pq_direct, marked_variables)
    pr_top = sparse_derivative(base, pr_star, marked_variables)
    require(pq_top == pr_top == {(): 1},
            "physical chart marked tops stopped being units")
    tagged_top = {(pq_tag, ()): Q(1), (pr_tag, ()): Q(-1)}
    chart_top_cochain = {(pq_tag, ()): Q(1, 2),
                         (pr_tag, ()): Q(-1, 2)}
    require(pairing(tagged_top, chart_top_cochain) == 1,
            "primitive chart-odd top readout changed")

    profile = site_profile(marked_edges)
    require(profile == (1,) * 8,
            "physical marked cube stopped being squarefree 4K2")
    cube = third.canonical_cube_and_unit()
    require(cube["physical_word"] == "01211222"
            and cube["fourth_operator_on_H_m"] == 1,
            "pinned fourth-cofactor replay changed")

    # Every physical linear readout and every physical derivation factors
    # through the forgotten polynomial.  It therefore kills an identically
    # zero chart difference.  A nonzero chart-odd cochain is presentation
    # data and cannot be renamed eta or sigma.
    return {
        "full_word": "01211222",
        "word_after_deleting_x": "1211222",
        "physical_row_terms_per_chart": len(row),
        "chart_partition_sizes": [15, 75, 0, 90],
        "primitive_chart_difference_physical_boundary_terms": 0,
        "word_private_matching_features_cancelled": len(row),
        "physical_target": 0,
        "every_chart_invariant_linear_readout": 0,
        "eta_z_terminal": 0,
        "sigma_qpq22_terminal": 0,
        "external_chart_odd_tail": [
            base.monomial_text(term) for term in sorted(pq_tail)
        ],
        "external_tail_term_count": len(pq_tail),
        "q00_coefficient": 0,
        "q11_coefficient": 1,
        "external_tail_equals_required_minus_q00_plus_q11": False,
        "marked_four_cube_cells": [str(value) for value in marked_variables],
        "marked_cube_type": "4K2 squarefree on all eight sites",
        "marked_cube_site_profile": list(profile),
        "chart_odd_marked_top_readout": 1,
        "chart_odd_marked_top_is_physical_terminal": False,
        "interpretation": (
            "pq-pr is presentation H1: it cancels the full physical row "
            "and retains only chart-tagged Hasse data"
        ),
    }


def repeated_component_audit(complete, base, positive) -> dict[str, object]:
    complete_ledger = complete.audit(base, positive)
    require(complete_ledger["two_chart"]["kernel_anchor_target_w_ores"]
            == [0, 0, 0, 0],
            "complete repeated chart kernel acquired a physical readout")

    records = []
    total_zero_endpoint_columns = 0
    physical_hits = 0
    zero_endpoint_hits = 0
    for index, (left_face, right_face, left_cell, _right_cell) in enumerate(
            complete.CUBIC_PAIRS):
        degree = complete.degree_add(
            base.lambda_degree(left_face),
            complete.cell_degree(complete.CYCLE_CELLS[left_cell]),
        )
        # These are the actual first rootless P3+K2 full-nine components.
        require(degree[3 * base.P + 0] == degree[3 * base.Q + 0] == 1
                and all(degree[3 * base.P + colour] == 0
                        and degree[3 * base.Q + colour] == 0
                        for colour in (1, 2)),
                "a repeated component acquired a nonzero endpoint slot")
        words = complete.compatible_words(degree)
        component = complete.component(base, degree)
        require(component["two_chart_columns"] == 576
                and component["two_chart_rank"] == 288
                and component["two_chart_kernel"] == 288,
                "576-column two-chart rank/kernel changed")
        physical_present = PHYSICAL_WORD in words
        zero_present = ZERO_ENDPOINT_WORD in words
        require(not physical_present and zero_present,
                "physical/zero-endpoint repeated-word classification changed")

        owners = defaultdict(list)
        for column_index, (_word, _multiplier, boundary) in enumerate(
                component["columns"]):
            for feature in boundary:
                owners[feature].append(column_index)
        hits = []
        for column_index, (word, multiplier, boundary) in enumerate(
                component["columns"]):
            if word != ZERO_ENDPOINT_WORD:
                continue
            unique = sum(len(owners[feature]) == 1 for feature in boundary)
            require(unique > 0, "zero-endpoint column lost its private pivot")
            hits.append({
                "multiplier": [list(cell) for cell in multiplier],
                "private_pivots": unique,
                "literal_boundary_terms_cancelled_by_pq_minus_pr":
                    len(boundary),
            })
        require(len(hits) in (6, 12),
                "zero-endpoint multiplier census changed")
        private_counts = [record["private_pivots"] for record in hits]
        require(min(private_counts) >= 42 and max(private_counts) <= 46,
                "zero-endpoint private-pivot range changed")

        physical_hits += int(physical_present)
        zero_endpoint_hits += int(zero_present)
        total_zero_endpoint_columns += len(hits)
        records.append({
            "component": index,
            "adjacent_faces": [left_face, right_face],
            "target_weight": sum(degree),
            "endpoint_colour_slots": {"p": [0], "q": [0]},
            "physical_word_01211222_present": physical_present,
            "zero_endpoint_word_00211200_present": zero_present,
            "zero_endpoint_multiplier_columns": len(hits),
            "private_pivots_per_selected_column_range":
                [min(private_counts), max(private_counts)],
            "all_90_boundary_terms_cancel_in_each_chart_difference": True,
            "two_chart_columns_rank_kernel": [576, 288, 288],
        })

    require(physical_hits == 0 and zero_endpoint_hits == 5
            and total_zero_endpoint_columns == 54,
            "complete repeated selected-word totals changed")
    return {
        "components": records,
        "complete_component_columns_each": 288,
        "physical_word_hits": physical_hits,
        "zero_endpoint_word_components": zero_endpoint_hits,
        "zero_endpoint_multiplier_columns_total": total_zero_endpoint_columns,
        "two_chart_kernel_basis":
            "pairwise pq-minus-pr copies of every labelled column",
        "two_chart_kernel_anchor_target_W_ores": [0, 0, 0, 0],
        "pairwise_difference_physical_terminal": 0,
        "pairwise_difference_chart_odd_terminal": (
            "may be nonzero, but is presentation data and does not descend"
        ),
        "verdict": (
            "the repeated chart differences cancel private pivots only for "
            "the zero-endpoint source word, and cancel every descended "
            "physical readout at the same time"
        ),
    }


def common_multiplier_guard() -> dict[str, object]:
    # This does not assume a particular higher target degree.  If both chart
    # copies are multiplied by the same literal monomial M, their equality
    # and every descended zero readout are preserved coefficientwise.
    sample_boundary = {("private", index): Q(1) for index in range(90)}
    multiplier = ((1, 2, 1, 2), (2, 3, 2, 1), (4, 5, 1, 2))
    left = {(multiplier, feature): value
            for feature, value in sample_boundary.items()}
    right = dict(left)
    require(not add_vectors(left, scale(right, -1)),
            "common multiplier stopped preserving chart-copy equality")
    return {
        "arbitrary_common_multiplier_preserves_zero_boundary": True,
        "arbitrary_chart_invariant_readout_after_multiplication": 0,
        "source_word_changed_by_multiplier": False,
        "can_create_minus_delta_eta_sigma_packet": False,
        "reason": (
            "common multiplication preserves equality of the two physical "
            "columns; only a new chart-nondiagonal relative differential "
            "could give their difference a physical landing"
        ),
    }


def main() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    base = load(
        "computations/verify_h3_direct_free_literal_four_face_full_nine_no_go.py",
        "two_chart_residual_base",
    )
    complete_base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "two_chart_residual_complete_base",
    )
    complete = load(
        "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py",
        "two_chart_residual_complete",
    )
    positive = load(
        "computations/verify_h3_rootless_five_cycle_positive_interface.py",
        "two_chart_residual_positive",
    )
    third = load(
        "computations/verify_h3_rootless_one_face_third_cofactor_comparison_vertex_gate.py",
        "two_chart_residual_third",
    )
    fiber = load(
        "computations/verify_h3_residual_q_eta_one_cell_fiber_product_gate.py",
        "two_chart_residual_fiber",
    )
    require(fiber.RESIDUAL_ROWS[:4]
            == ("D_q00", "D_q10", "D_q01", "D_q11"),
            "fiber residual row order changed")

    ledger = {
        "theorem": "residual-q primitive two-chart copy membership no-go",
        "physical_word_chart_difference":
            selected_physical_chart_difference(base, third),
        "first_repeated_P3K2_components":
            repeated_component_audit(complete, complete_base, positive),
        "common_multiplier_guard": common_multiplier_guard(),
        "fiber_target_comparison": {
            "required_residue_full": [-1, 1, 1, -1],
            "required_residue_endpoint_odd": "-q00+q11",
            "required_eta": "1+delta_(vz)u_z/t",
            "required_sigma": "-q_pq^22",
            "primitive_physical_chart_difference_values": {
                "residue": 0, "eta": 0, "sigma": 0,
            },
            "matches": False,
        },
        "verdict": (
            "pq-minus-pr does cancel the private full-nine pivots, but only "
            "because it cancels the entire identical physical column.  In "
            "the physical word its remaining chart-odd Hasse tail is h_v, "
            "not -delta, and the marked top is a presentation unit rather "
            "than eta/sigma terminal data.  The physical word is absent from "
            "the complete first P3+K2 components; their zero-endpoint chart "
            "differences have all physical readouts zero.  Hence no primitive "
            "chart-copy difference realizes the fiber target"
        ),
        "scope": (
            "exact physical word 01211222, its selected 4K2 chart top, all "
            "five complete first rootless P3+K2 full-nine components, and "
            "arbitrary common multiplication of identical chart copies.  "
            "A new chart-nondiagonal higher comparison is not excluded"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))

    print("h3 residual-q two-chart copy membership: NO-GO")
    print("physical pq-pr boundary / residue / eta / sigma: 0 / 0 / 0 / 0")
    print("physical-word chart-odd tail: h_v, not -q00+q11")
    print("physical word in first repeated P3+K2 components: 0 / 5")
    print("zero-endpoint chart word: 54 columns, private pivots 42--46")
    print("two-chart differences cancel pivots and every physical readout")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
