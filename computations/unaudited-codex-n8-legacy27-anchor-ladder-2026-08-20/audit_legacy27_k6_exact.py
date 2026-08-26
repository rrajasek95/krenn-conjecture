#!/usr/bin/env python3
"""Exact labelled K^6 lift attempt for zero-chart 30 / legacy chart 27.

The full minimum-K-degree-five component is reduced under the complete
six-element stabilizer of the twelve named anchors.  Literal multiplicities
are retained.  A successful quotient certificate is expanded as a group
average and accepted only after a characteristic-zero replay on labelled
monomial rows.  This proves filtered membership only, never chart closure.
"""

from __future__ import annotations

from collections import Counter, defaultdict, deque
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROBE_PATH = HERE / "probe_legacy27_k6_orbits.py"
SPEC = importlib.util.spec_from_file_location("legacy27_probe", PROBE_PATH)
PROBE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROBE)
BASE = PROBE.BASE
OUT = HERE / "results_k6_exact.json"
LOWER_RESULTS = (
    HERE.parent / "unaudited-codex-n8-other27-kadic-2026-08-20"
    / "results_k5_probe.json"
)
AUGMENTED_RESULTS = HERE / "k6_augmented_solution_exact.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


@lru_cache(maxsize=None)
def row_orbit(row):
    return tuple(sorted({bytes(sorted(transform[cell] for cell in row))
                         for transform in PROBE.TRANSFORMS}))


@lru_cache(maxsize=None)
def row_orbit_size(row):
    return len(row_orbit(row))


def parse_fraction(text):
    return Fraction(text)


def parse_lower_certificate(lower_columns=None):
    if lower_columns is not None and AUGMENTED_RESULTS.exists():
        payload = json.loads(AUGMENTED_RESULTS.read_text())
        require(payload["exact_augmented_replay"],
                "augmented lower solution lacks an exact replay")
        require(payload["matrix_sha256"] ==
                "78a62528fc5dce57f5c20f4000b3b35bfe0b2f6679ebd1285f7de97fb9d0fb92",
                "augmented lower solution matrix changed")
        return tuple((Fraction(value), lower_columns[index])
                     for index, value in payload["solution"])
    payload = json.loads(LOWER_RESULTS.read_text())
    record = next(item for item in payload["records"]
                  if item["chart"] == PROBE.CHART)
    require(record["legacy_one_based_chart"] == 27,
            "lower certificate legacy numbering changed")
    require(record["cutoff"] == 5, "lower certificate cutoff changed")
    require(record["exact_membership"]["exact_replay"],
            "lower certificate was not exactly replayed upstream")
    name_to_id = {
        BASE.cell_name(cell): index for index, cell in enumerate(BASE.CELLS)
    }
    compressed = Counter()
    for item in record["exact_membership"]["exact_certificate"]:
        word = tuple(map(int, item["word"]))
        multiplier = bytes(sorted(name_to_id[name]
                                  for name in item["multiplier"]))
        column = PROBE.canonical_column((word, multiplier))
        compressed[column] += parse_fraction(item["coefficient"])
    return tuple((value, column) for column, value in
                 sorted(compressed.items(), key=lambda item: repr(item[0]))
                 if value)


def expand_average(certificate, degrees):
    """Expand coefficients on group-average columns to labelled rows."""
    answer = Counter()
    group_order = len(PROBE.STABILIZER)
    for coefficient, column in certificate:
        for action in range(group_order):
            transformed = PROBE.transform_column(column, action)
            for row in BASE.column_rows(transformed):
                if BASE.row_degree(row, PROBE.ANCHORS) in degrees:
                    answer[row] += coefficient / group_order
    return Counter({row: value for row, value in answer.items() if value})


def target_actual(cutoff):
    return Counter({row: Fraction(value) for row, value in
                    BASE.filtered_target(PROBE.MATCHINGS, cutoff).items()})


def check_invariance(vector):
    for row, value in vector.items():
        for transform in PROBE.TRANSFORMS:
            image = bytes(sorted(transform[cell] for cell in row))
            require(vector[image] == value,
                    "symmetrized labelled vector lost invariance")


def solve_graph_quotient(non_rows, unary, edge_columns, right_hand_side):
    """Complete exact echelon for columns of weights one and two.

    The weight-two matrix is an unsigned graph incidence matrix.  A unary
    column roots a component.  An unrooted non-bipartite component is solved
    with one odd-cycle chord; an unrooted bipartite component exposes its
    exact alternating-sum obstruction.  All components and all input columns
    are inspected, so this is a common echelon rather than an early rank stop.
    """
    adjacency = defaultdict(list)
    for pair, column in edge_columns.items():
        u, v = pair
        adjacency[u].append((v, pair, column))
        adjacency[v].append((u, pair, column))
    for row in non_rows:
        adjacency[row]  # retain isolated quotient rows

    unseen = set(non_rows)
    solution = Counter()
    component_records = []
    exact_obstructions = []
    while unseen:
        start = min(unseen)
        component = {start}
        queue = deque((start,))
        while queue:
            vertex = queue.popleft()
            for other, _pair, _column in adjacency[vertex]:
                if other not in component:
                    component.add(other)
                    queue.append(other)
        unseen -= component
        unary_vertices = sorted(vertex for vertex in component if vertex in unary)
        root = unary_vertices[0] if unary_vertices else min(component)

        parent = {root: None}
        parent_pair = {}
        order = [root]
        colour = {root: 0}
        conflict_pair = None
        queue = deque((root,))
        while queue:
            vertex = queue.popleft()
            for other, pair, _column in adjacency[vertex]:
                if other not in parent:
                    parent[other] = vertex
                    parent_pair[other] = pair
                    colour[other] = 1 - colour[vertex]
                    order.append(other)
                    queue.append(other)
                elif parent.get(vertex) != other and colour[other] == colour[vertex]:
                    conflict_pair = pair
        tree_pairs = set(parent_pair.values())
        non_tree_pairs = set(edge_columns) & {
            pair for vertex in component
            for _other, pair, _column in adjacency[vertex]
        }
        non_tree_pairs -= tree_pairs

        # Affine values a + b*t for the selected tree edges.  All unused
        # non-tree edges are zero; t is one odd-cycle chord when required.
        chosen_chord = None
        if not unary_vertices and conflict_pair is not None:
            require(conflict_pair in non_tree_pairs,
                    "odd conflict was unexpectedly a tree edge")
            chosen_chord = conflict_pair
        fixed = {vertex: (Fraction(0), Fraction(0)) for vertex in component}
        if chosen_chord is not None:
            for vertex in chosen_chord:
                fixed[vertex] = (Fraction(0), Fraction(1))

        tree_value = {}
        children = defaultdict(list)
        for vertex, upper in parent.items():
            if upper is not None:
                children[upper].append(vertex)
        for vertex in reversed(order[1:]):
            constant = Fraction(right_hand_side.get(vertex, 0)) - fixed[vertex][0]
            slope = -fixed[vertex][1]
            for child in children[vertex]:
                a, b = tree_value[child]
                constant -= a
                slope -= b
            tree_value[vertex] = (constant, slope)

        root_left = fixed[root]
        left_constant, left_slope = root_left
        for child in children[root]:
            a, b = tree_value[child]
            left_constant += a
            left_slope += b
        root_rhs = Fraction(right_hand_side.get(root, 0))
        parameter = Fraction(0)
        kind = "rooted-by-unary"
        if unary_vertices:
            unary_value = root_rhs - left_constant
            require(left_slope == 0, "rooted component retained a chord parameter")
            if unary_value:
                solution[unary[root]] += unary_value
        elif chosen_chord is not None:
            kind = "unrooted-nonbipartite"
            require(left_slope != 0,
                    "odd-cycle root equation did not see its chord")
            parameter = (root_rhs - left_constant) / left_slope
            if parameter:
                solution[edge_columns[chosen_chord]] += parameter
        else:
            kind = "unrooted-bipartite"
            discrepancy = root_rhs - left_constant
            if discrepancy:
                signed_sum = sum(
                    (1 if colour[vertex] == colour[root] else -1)
                    * Fraction(right_hand_side.get(vertex, 0))
                    for vertex in component
                )
                require(signed_sum == discrepancy,
                        "bipartite obstruction normalization changed")
                exact_obstructions.append({
                    "component_size": len(component),
                    "signed_target_pairing": str(signed_sum),
                    "positive_rows": sum(colour[v] == colour[root]
                                         for v in component),
                    "negative_rows": sum(colour[v] != colour[root]
                                         for v in component),
                })
                continue
        for vertex, pair in parent_pair.items():
            a, b = tree_value[vertex]
            value = a + b * parameter
            if value:
                solution[edge_columns[pair]] += value
        component_records.append({
            "size": len(component),
            "edges": sum(len(adjacency[v]) for v in component) // 2,
            "unary_vertices": len(unary_vertices),
            "type": kind,
        })
    return solution, component_records, exact_obstructions


def audit():
    data = PROBE.degree5_orbit_closure()
    rows5 = data["rows5"]
    columns5 = data["columns5"]
    singleton = {}
    unary = {}
    edge_columns = {}
    triples = 0
    for column in columns5:
        outputs = tuple(PROBE.canonical_row(row)
                        for row in BASE.column_rows(column)
                        if BASE.row_degree(row, PROBE.ANCHORS) == 5)
        require(len(outputs) in (1, 3),
                "degree-five leading count left the literal 1/3 split")
        require(len(outputs) == len(set(outputs)),
                "degree-five column has an unrecorded row-orbit multiplicity")
        if len(outputs) == 1:
            singleton.setdefault(outputs[0], column)
        else:
            triples += 1
    non_rows = tuple(sorted(set(rows5) - set(singleton)))
    non_set = set(non_rows)
    for column in columns5:
        outputs = tuple(PROBE.canonical_row(row)
                        for row in BASE.column_rows(column)
                        if BASE.row_degree(row, PROBE.ANCHORS) == 5)
        if len(outputs) != 3:
            continue
        projected = tuple(sorted(row for row in outputs if row in non_set))
        require(len(projected) <= 2,
                "triple quotient acquired a weight-three column")
        if len(projected) == 1:
            unary.setdefault(projected[0], column)
        elif len(projected) == 2:
            edge_columns.setdefault(projected, column)

    # Compress and symmetrize the already-replayed literal K^5 certificate.
    lower_certificate = parse_lower_certificate(data["lower_columns"])
    lower_replay = expand_average(lower_certificate, (0, 1, 2, 3, 4))
    target5_lower = target_actual(5)
    require(lower_replay == target5_lower,
            "symmetrized upstream K^5 certificate failed labelled replay")
    current5 = expand_average(lower_certificate, (5,))
    exact_target5 = Counter({row: value for row, value in target_actual(6).items()
                             if BASE.row_degree(row, PROBE.ANCHORS) == 5})
    residual5 = Counter(exact_target5)
    residual5.subtract(current5)
    residual5 = Counter({row: value for row, value in residual5.items() if value})
    check_invariance(residual5)
    require(all(PROBE.canonical_row(row) in set(rows5) for row in residual5),
            "lower tail escaped the closed degree-five component")
    residual_scaled = Counter({
        row: residual5[row] * row_orbit_size(row) for row in rows5
        if residual5[row]
    })
    quotient_rhs = Counter({row: residual_scaled[row] for row in non_rows
                            if residual_scaled[row]})

    triple_solution, component_records, obstructions = solve_graph_quotient(
        non_rows, unary, edge_columns, quotient_rhs
    )
    # A failure here is only an obstruction to this chosen lower lift.  It is
    # not a K^6 nonmembership claim because lower syzygies may alter the tail.
    if obstructions:
        core = {
            "status": "EXACT OBSTRUCTION TO FROZEN K5 LIFT ONLY",
            "zero_based_chart": 30,
            "legacy_one_based_chart": 27,
            "stabilizer_order": len(PROBE.STABILIZER),
            "degree5_row_column_orbits": [len(rows5), len(columns5)],
            "literal_singleton_row_orbits": len(singleton),
            "coupled_quotient_rows": len(non_rows),
            "projected_unary_rows": len(unary),
            "projected_distinct_edges": len(edge_columns),
            "component_records": component_records,
            "frozen_lower_lift_obstructions": obstructions,
            "K6_nonmembership_proved": False,
            "reason": "lower K5 syzygy tails were not yet included",
        }
        encoded = json.dumps(core, sort_keys=True, separators=(",", ":"))
        core["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
        return core

    triple_certificate = tuple((value, column) for column, value in
                               sorted(triple_solution.items(),
                                      key=lambda item: repr(item[0])) if value)
    triple_replay5 = expand_average(triple_certificate, (5,))
    remaining5 = Counter(residual5)
    remaining5.subtract(triple_replay5)
    remaining5 = Counter({row: value for row, value in remaining5.items() if value})
    require(not any(remaining5[row] for row in remaining5
                    if PROBE.canonical_row(row) in non_set),
            "complete quotient echelon left a coupled labelled row")

    singleton_certificate = []
    for representative in sorted(singleton):
        coefficient = remaining5[representative] * row_orbit_size(representative)
        if coefficient:
            singleton_certificate.append((coefficient, singleton[representative]))
    singleton_certificate = tuple(singleton_certificate)
    certificate = lower_certificate + triple_certificate + singleton_certificate
    replay = expand_average(certificate, (0, 1, 2, 3, 4, 5))
    expected = target_actual(6)
    require(replay == expected,
            "full K^6 orbit certificate failed labelled exact Q replay")

    # Must-fire controls.  Removing any nonzero term, omitting group-average
    # normalization, and truncating the final closure layer must all be seen.
    mutation_term = next(item for item in certificate if item[0])
    mutated = list(certificate)
    mutated.remove(mutation_term)
    require(expand_average(tuple(mutated), (0, 1, 2, 3, 4, 5)) != expected,
            "certificate term-deletion mutation did not fire")
    unnormalized = Counter()
    for coefficient, column in certificate:
        for action in range(len(PROBE.STABILIZER)):
            for row in BASE.column_rows(PROBE.transform_column(column, action)):
                if BASE.row_degree(row, PROBE.ANCHORS) < 6:
                    unnormalized[row] += coefficient
    require(unnormalized != expected,
            "orbit-multiplicity normalization mutation did not fire")
    require(len(data["layers"]) >= 2 and data["layers"][-1][0] == 0
            and data["layers"][-1][1] > 0,
            "early-stop control lost its terminal column-only closure layer")

    denominator_lcm = 1
    from math import gcd
    for coefficient, _column in certificate:
        denominator_lcm = (denominator_lcm * coefficient.denominator
                           // gcd(denominator_lcm, coefficient.denominator))
    coefficient_histogram = Counter(str(value) for value, _ in certificate)
    ledger = []
    for coefficient, column in certificate:
        ledger.append({
            "coefficient_on_six_transform_average": str(coefficient),
            "word": "".join(map(str, column[0])),
            "multiplier": [BASE.cell_name(BASE.CELLS[cell])
                           for cell in column[1]],
            "column_orbit_size": len(PROBE.column_orbit(column)),
            "minimum_K_degree": PROBE.column_minimum_degree(column),
        })
    core = {
        "status": "UNAUDITED EXACT FILTERED K6 LIFT; NO CHART CLOSURE CLAIM",
        "zero_based_chart": 30,
        "legacy_one_based_chart": 27,
        "stabilizer_order": len(PROBE.STABILIZER),
        "degree5_row_column_orbits": [len(rows5), len(columns5)],
        "degree5_literal_leading_split": {
            "singleton_columns": sum(1 for column in columns5
                                     if sum(BASE.row_degree(row, PROBE.ANCHORS) == 5
                                            for row in BASE.column_rows(column)) == 1),
            "triple_columns": triples,
            "row_orbit_collisions": 0,
        },
        "complete_common_echelon": {
            "literal_singleton_row_orbits": len(singleton),
            "coupled_quotient_rows": len(non_rows),
            "projected_unary_rows": len(unary),
            "projected_distinct_edges": len(edge_columns),
            "components": component_records,
            "exact_obstructions": [],
        },
        "certificate": {
            "lower_orbit_average_terms": len(lower_certificate),
            "coupled_triple_orbit_average_terms": len(triple_certificate),
            "singleton_orbit_average_terms": len(singleton_certificate),
            "total_orbit_average_terms": len(certificate),
            "denominator_lcm": denominator_lcm,
            "coefficient_histogram": dict(sorted(coefficient_histogram.items())),
            "exact_labelled_Q_replay": True,
            "term_deletion_mutation_fired": True,
            "orbit_multiplicity_mutation_fired": True,
            "early_stop_terminal_layer_fired": True,
            "terms": ledger,
        },
        "conclusion": "H0*H1*H2 belongs to I_mix + K_anchor^6 over Q",
        "full_localized_chart_controlled": False,
        "remaining_anchor_degrees": [6, 7, 8, 9, 10, 11, 12],
    }
    encoded = json.dumps(core, sort_keys=True, separators=(",", ":"))
    core["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    return core


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    result = audit()
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("legacy27 K6 exact audit:", result["status"])
    print("result sha256:", result["result_sha256"])
    if "certificate" in result:
        print("certificate terms:",
              result["certificate"]["total_orbit_average_terms"])


if __name__ == "__main__":
    main()
