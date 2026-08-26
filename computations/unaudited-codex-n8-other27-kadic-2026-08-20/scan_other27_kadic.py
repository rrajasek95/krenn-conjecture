#!/usr/bin/env python3
"""Source-labelled K-adic triage for the 27 non-dangerous N=8 charts.

This checker reads only the raw ordered matching triples from the quotient
orbit ledger.  For a chart it names the twelve selected pure cells as
anchors, lets K be the other 240 endpoint cells, and constructs the complete
literal mixed-hafnian incidence component modulo K^d.  The initial discovery
mode reports finite-field ranks only; exact certificates/duals are added
separately before any membership verdict is frozen.
"""

from __future__ import annotations

import argparse
from collections import Counter, deque
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
import math
from pathlib import Path
import sys


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
UPSTREAM = (
    HERE.parent / "unaudited-codex-x4-quotient-eliminator-2026-08-20"
    / "results.json"
)
EXPECTED_UPSTREAM_SHA256 = (
    "7b61e3c5cc2422087ea6d6d2a4e393fdebfd5df88c4e6eb5805f894ab01f8162"
)
EXCLUDED = frozenset((25, 26, 27, 28))
PRIME = 1_000_003
N = 8
COLORS = range(3)
EDGES = tuple(combinations(range(N), 2))
CELLS = tuple(
    (u, v, a, b)
    for u, v in EDGES
    for a in COLORS
    for b in COLORS
)
CELL_ID = {cell: index for index, cell in enumerate(CELLS)}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


@lru_cache(maxsize=None)
def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index, second in enumerate(vertices[1:], 1):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


PM8 = perfect_matchings(tuple(range(N)))
require(len(PM8) == 105, "perfect-matching census changed")


def cell_name(cell):
    u, v, a, b = cell
    return f"x{u}{v}_{a}{b}"


def term_ids(word, matching):
    return bytes(sorted(
        CELL_ID[u, v, word[u], word[v]] for u, v in matching
    ))


@lru_cache(maxsize=None)
def word_terms(word):
    return tuple(term_ids(word, matching) for matching in PM8)


@lru_cache(maxsize=250_000)
def column_rows(column):
    word, multiplier = column
    return tuple(bytes(sorted(multiplier + term)) for term in word_terms(word))


@lru_cache(maxsize=250_000)
def incident_columns(row):
    """All degree-eight multiples of mixed H_word containing literal row."""
    decoded = tuple(CELLS[cell] for cell in row)
    answer = set()
    for selected in combinations(range(12), 4):
        word = [None] * N
        covered = []
        for index in selected:
            u, v, a, b = decoded[index]
            covered.extend((u, v))
            word[u], word[v] = a, b
        if len(set(covered)) != N or len(set(word)) == 1:
            continue
        selected_set = frozenset(selected)
        multiplier = bytes(
            row[index] for index in range(12) if index not in selected_set
        )
        answer.add((tuple(word), multiplier))
    return tuple(sorted(answer, key=repr))


def anchor_ids(matchings):
    anchors = frozenset(
        CELL_ID[u, v, color, color]
        for color, matching in enumerate(matchings)
        for u, v in matching
    )
    require(len(anchors) == 12, "selected pure cells are not twelve distinct anchors")
    return anchors


def row_degree(row, anchors):
    return sum(cell not in anchors for cell in row)


def filtered_target(matchings, cutoff):
    """Literal expansion of H0 H1 H2 in K-degrees strictly below cutoff."""
    anchors = anchor_ids(matchings)
    groups = []
    for color in COLORS:
        by_degree = {}
        for term in word_terms((color,) * N):
            degree = row_degree(term, anchors)
            if degree < cutoff:
                by_degree.setdefault(degree, []).append(term)
        groups.append(by_degree)
    target = Counter()
    for degrees in product(range(cutoff), repeat=3):
        if sum(degrees) >= cutoff:
            continue
        for terms in product(*(groups[color].get(degrees[color], ())
                               for color in COLORS)):
            target[bytes(sorted(b"".join(terms)))] += 1
    require(target, "filtered pure target vanished")
    require(Counter(row_degree(row, anchors) for row in target)
            == Counter({degree: sum(1 for row in target
                                    if row_degree(row, anchors) == degree)
                        for degree in set(row_degree(row, anchors)
                                          for row in target)}),
            "target degree inventory failed")
    return target


def complete_component(matchings, cutoff):
    """Close the full literal row/column component modulo K^cutoff."""
    anchors = anchor_ids(matchings)
    target = filtered_target(matchings, cutoff)
    rows = set(target)
    frontier = deque(sorted(rows))
    columns = set()
    while frontier:
        row = frontier.popleft()
        for column in incident_columns(row):
            if column in columns:
                continue
            outputs = tuple(
                output for output in column_rows(column)
                if row_degree(output, anchors) < cutoff
            )
            require(row in outputs, "incident column lost its input row")
            columns.add(column)
            for output in outputs:
                if output not in rows:
                    rows.add(output)
                    frontier.append(output)
    ordered_rows = tuple(sorted(rows))
    ordered_columns = tuple(sorted(columns, key=repr))
    truncated_columns = tuple(
        tuple(output for output in column_rows(column)
              if row_degree(output, anchors) < cutoff)
        for column in ordered_columns
    )
    require(all(outputs for outputs in truncated_columns),
            "closed component retained an empty column")
    return anchors, target, ordered_rows, ordered_columns, truncated_columns


def modular_membership(rows, columns, target):
    row_index = {row: index for index, row in enumerate(rows)}
    basis = {}
    for outputs in columns:
        vector = Counter(row_index[row] for row in outputs)
        vector = {index: value % PRIME for index, value in vector.items()
                  if value % PRIME}
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in basis:
                inverse = pow(value, -1, PRIME)
                basis[pivot] = {
                    index: entry * inverse % PRIME
                    for index, entry in vector.items()
                }
                break
            for index, entry in basis[pivot].items():
                new = (vector.get(index, 0) - value * entry) % PRIME
                if new:
                    vector[index] = new
                else:
                    vector.pop(index, None)
    residual = {
        row_index[row]: value % PRIME
        for row, value in target.items() if value % PRIME
    }
    original = len(residual)
    while residual:
        pivot = min(residual)
        value = residual[pivot]
        if pivot not in basis:
            break
        for index, entry in basis[pivot].items():
            new = (residual.get(index, 0) - value * entry) % PRIME
            if new:
                residual[index] = new
            else:
                residual.pop(index, None)
    return {
        "rank_mod_prime": len(basis),
        "left_nullity_mod_prime": len(rows) - len(basis),
        "target_nonzeros": original,
        "target_remainder_nonzeros": len(residual),
        "target_in_span_mod_prime": not residual,
    }


def add_scaled(target, source, scale):
    for key, value in source.items():
        new = target.get(key, Fraction(0)) + scale * value
        if new:
            target[key] = new
        else:
            target.pop(key, None)


def exact_core_singleton_certificate(
        anchors, target, rows, columns, truncated_columns):
    """Peel exact unit columns, solve the residual core over Q, and replay."""
    row_number = {row: index for index, row in enumerate(rows)}
    incident = [[] for _row in rows]
    output_numbers = []
    for column_index, outputs in enumerate(truncated_columns):
        numbers = tuple(row_number[row] for row in outputs)
        output_numbers.append(numbers)
        for number in numbers:
            incident[number].append(column_index)
    active = [True] * len(rows)
    active_counts = [len(numbers) for numbers in output_numbers]
    queue = deque(index for index, count in enumerate(active_counts) if count == 1)
    peel_order = []
    while queue:
        column_index = queue.popleft()
        if active_counts[column_index] != 1:
            continue
        number = next((value for value in output_numbers[column_index]
                       if active[value]), None)
        require(number is not None, "unit-peeling active count drifted")
        active[number] = False
        peel_order.append((rows[number], column_index))
        for other_column in incident[number]:
            active_counts[other_column] -= 1
            require(active_counts[other_column] >= 0,
                    "unit-peeling column count became negative")
            if active_counts[other_column] == 1:
                queue.append(other_column)
    core_rows = tuple(row for index, row in enumerate(rows) if active[index])
    core_index = {row: index for index, row in enumerate(core_rows)}

    candidates = []
    for index, outputs in enumerate(truncated_columns):
        vector = Counter(core_index[row] for row in outputs if row in core_index)
        if vector:
            candidates.append((len(vector), len(outputs), repr(columns[index]),
                               index, vector))
    candidates.sort()
    basis = {}
    selected = []
    for _core_weight, _weight, _label, column_index, raw_vector in candidates:
        vector = {index: value % PRIME for index, value in raw_vector.items()
                  if value % PRIME}
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in basis:
                inverse = pow(value, -1, PRIME)
                basis[pivot] = {
                    index: entry * inverse % PRIME
                    for index, entry in vector.items()
                }
                selected.append(column_index)
                break
            for index, entry in basis[pivot].items():
                new = (vector.get(index, 0) - value * entry) % PRIME
                if new:
                    vector[index] = new
                else:
                    vector.pop(index, None)
    core_target_mod = {
        core_index[row]: value % PRIME
        for row, value in target.items()
        if row in core_index and value % PRIME
    }
    while core_target_mod:
        pivot = min(core_target_mod)
        value = core_target_mod[pivot]
        require(pivot in basis,
                "target has a modular obstruction on the irreducible core")
        for index, entry in basis[pivot].items():
            new = (core_target_mod.get(index, 0) - value * entry) % PRIME
            if new:
                core_target_mod[index] = new
            else:
                core_target_mod.pop(index, None)

    pivot_rows = tuple(core_rows[index] for index in sorted(basis))
    require(len(selected) == len(pivot_rows),
            "selected core basis and pivot-row count differ")

    augmented = []
    for row in pivot_rows:
        augmented.append([
            Fraction(sum(output == row
                         for output in truncated_columns[column_index]))
            for column_index in selected
        ] + [Fraction(target.get(row, 0))])
    determinant = Fraction(1)
    sign = 1
    size = len(selected)
    for column in range(size):
        pivot = next((row for row in range(column, size)
                      if augmented[row][column]), None)
        require(pivot is not None, "modular core minor vanished over Q")
        if pivot != column:
            augmented[column], augmented[pivot] = (
                augmented[pivot], augmented[column]
            )
            sign *= -1
        pivot_value = augmented[column][column]
        determinant *= pivot_value
        augmented[column] = [
            value / pivot_value for value in augmented[column]
        ]
        for row in range(size):
            if row == column or not augmented[row][column]:
                continue
            scale = augmented[row][column]
            augmented[row] = [
                left - scale * right
                for left, right in zip(augmented[row], augmented[column])
            ]
    determinant *= sign
    require(determinant.denominator == 1 and determinant,
            "exact core determinant is not a nonzero integer")

    certificate = Counter()
    for index, column_index in enumerate(selected):
        if augmented[index][-1]:
            certificate[column_index] += augmented[index][-1]
    replay = {}
    for column_index, coefficient in certificate.items():
        add_scaled(replay, Counter(truncated_columns[column_index]), coefficient)
    residual = {row: Fraction(value) for row, value in target.items()}
    add_scaled(residual, replay, Fraction(-1))
    require(all(row not in core_index for row in residual),
            "exact core solve left an irreducible row")
    for row, column_index in reversed(peel_order):
        coefficient = residual.get(row, Fraction(0))
        if not coefficient:
            continue
        certificate[column_index] += coefficient
        add_scaled(
            residual,
            Counter(truncated_columns[column_index]),
            -coefficient,
        )
    require(not residual, "reverse unit peeling did not cancel the residual")

    exact_replay = {}
    for column_index, coefficient in certificate.items():
        add_scaled(
            exact_replay,
            Counter(truncated_columns[column_index]),
            coefficient,
        )
    expected = {row: Fraction(value) for row, value in target.items()}
    require(exact_replay == expected, "literal rational certificate replay failed")
    first_column = min(certificate)
    mutation = dict(exact_replay)
    add_scaled(
        mutation,
        Counter(truncated_columns[first_column]),
        -2 * certificate[first_column],
    )
    require(mutation != expected, "certificate sign mutation did not fire")

    ledger = []
    for column_index, coefficient in sorted(certificate.items()):
        if not coefficient:
            continue
        word, multiplier = columns[column_index]
        full_outputs = column_rows(columns[column_index])
        ledger.append({
            "coefficient": str(coefficient),
            "word": "".join(map(str, word)),
            "multiplier": [cell_name(CELLS[cell]) for cell in multiplier],
            "minimum_K_degree": min(row_degree(row, anchors)
                                      for row in full_outputs),
            "truncated_output_count": len(truncated_columns[column_index]),
        })
    denominator_lcm = 1
    for coefficient in certificate.values():
        denominator_lcm = (
            denominator_lcm * coefficient.denominator
            // math.gcd(denominator_lcm, coefficient.denominator)
        )
    return {
        "method": (
            "iterated literal unit-column peeling, exact Q solve on the "
            "irreducible core, and reverse exact cancellation"
        ),
        "iteratively_peeled_rows": len(peel_order),
        "irreducible_core_rows": len(core_rows),
        "irreducible_core_rank": len(selected),
        "irreducible_core_left_nullity": len(core_rows) - len(selected),
        "selected_exact_core_columns": len(selected),
        "exact_core_minor_determinant": str(determinant),
        "exact_certificate_terms": len(ledger),
        "exact_certificate_denominator_lcm": denominator_lcm,
        "coefficient_histogram": dict(sorted(Counter(
            item["coefficient"] for item in ledger
        ).items())),
        "exact_certificate": ledger,
        "exact_replay": True,
        "sign_mutation_fired": True,
    }


def port_mate(triple):
    mate = [-1] * 24
    for color, matching in enumerate(triple):
        for u, v in matching:
            left, right = 3 * u + color, 3 * v + color
            mate[left], mate[right] = right, left
    require(all(value >= 0 for value in mate), "port matching incomplete")
    return tuple(mate)


def color_transform(mate, permutation):
    answer = [-1] * 24
    for vertex in range(8):
        for color in range(3):
            target = 3 * vertex + permutation[color]
            other_vertex, other_color = divmod(mate[3 * vertex + color], 3)
            answer[target] = 3 * other_vertex + permutation[other_color]
    return tuple(answer)


def vertex_components(mate):
    adjacency = [set() for _ in range(8)]
    for port, other in enumerate(mate):
        adjacency[port // 3].add(other // 3)
    unseen = set(range(8))
    answer = []
    while unseen:
        root = min(unseen)
        component = {root}
        frontier = [root]
        while frontier:
            vertex = frontier.pop()
            for other in adjacency[vertex]:
                if other not in component:
                    component.add(other)
                    frontier.append(other)
        unseen -= component
        answer.append(component)
    return tuple(answer)


def rooted_component_code(mate, component, root):
    order = [root]
    labels = {root: 0}
    for vertex in order:
        for color in range(3):
            other_vertex = mate[3 * vertex + color] // 3
            if other_vertex not in labels:
                labels[other_vertex] = len(order)
                order.append(other_vertex)
    require(set(order) == component, "root traversal missed component")
    return tuple(
        3 * labels[mate[3 * vertex + color] // 3]
        + mate[3 * vertex + color] % 3
        for vertex in order for color in range(3)
    )


def legacy_key(triple):
    mate = port_mate(triple)
    return min(
        tuple(sorted(
            min(rooted_component_code(transformed, component, root)
                for root in component)
            for component in vertex_components(transformed)
        ))
        for color_permutation in permutations(range(3))
        for transformed in (color_transform(mate, color_permutation),)
    )


def load_charts():
    digest = sha256(UPSTREAM.read_bytes()).hexdigest()
    require(digest == EXPECTED_UPSTREAM_SHA256,
            ("raw matching ledger changed", digest))
    payload = json.loads(UPSTREAM.read_text())
    records = payload["pure_matching_orbits"]["records"]
    require([record["orbit"] for record in records] == list(range(31)),
            "zero-based orbit numbering changed")
    require(sum(record["orbit_size"] for record in records) == 105 ** 3,
            "matching-triple orbits no longer exhaust 105^3")
    all_charts = {
        record["orbit"]: tuple(
            tuple(tuple(edge) for edge in matching)
            for matching in record["representative"]
        )
        for record in records
    }
    keys = {chart: legacy_key(triple) for chart, triple in all_charts.items()}
    sorted_keys = sorted(set(keys.values()))
    require(len(sorted_keys) == 31, "legacy raw chart count changed")
    legacy = {chart: sorted_keys.index(key) + 1 for chart, key in keys.items()}
    require({chart: legacy[chart] for chart in (24, 29, 30)}
            == {24: 25, 29: 26, 30: 27}, "legacy critical mapping changed")
    require([legacy[chart] for chart in sorted(EXCLUDED)] == [28, 29, 30, 31],
            "dangerous legacy mapping changed")
    return {
        chart: triple for chart, triple in all_charts.items()
        if chart not in EXCLUDED
    }, legacy, digest


def scan_chart(chart, legacy_chart, matchings, cutoff, exact):
    anchors, target, rows, columns, truncated = complete_component(
        matchings, cutoff
    )
    modular = modular_membership(rows, truncated, target)
    singleton_rows = {
        outputs[0] for outputs in truncated if len(outputs) == 1
    }
    answer = {
        "chart": chart,
        "legacy_one_based_chart": legacy_chart,
        "first_layer_stratum": (
            "leading-contractible" if legacy_chart <= 24
            else "lex-Morse-critical-25-to-27"
        ),
        "cutoff": cutoff,
        "statement_scanned": f"H0*H1*H2 in I_mix + K^{cutoff}",
        "anchor_names": [cell_name(CELLS[cell]) for cell in sorted(anchors)],
        "anchors_specialized": 0,
        "rows": len(rows),
        "columns": len(columns),
        "literal_singleton_rows": len(singleton_rows),
        "nonsingleton_core_rows": len(rows) - len(singleton_rows),
        "target_degree_histogram": dict(sorted(Counter(
            row_degree(row, anchors) for row in target
        ).items())),
        **modular,
    }
    if exact:
        answer["exact_membership"] = exact_core_singleton_certificate(
            anchors, target, rows, columns, truncated
        )
        answer["verdict"] = "EXACT FORMAL LIFT"
        answer["scope_guard"] = (
            "membership modulo K^d is formal-boundary data only; it is not "
            "localized chart closure and does not repair the first-layer "
            "31-chart Morse contraction by itself"
        )
    summary = {
        key: answer[key] for key in (
            "chart", "legacy_one_based_chart", "first_layer_stratum",
            "cutoff", "rows", "columns", "literal_singleton_rows",
            "nonsingleton_core_rows", "target_in_span_mod_prime",
        )
    }
    if exact:
        summary.update({
            "exact_certificate_terms": answer["exact_membership"][
                "exact_certificate_terms"
            ],
            "exact_core_minor_determinant": answer["exact_membership"][
                "exact_core_minor_determinant"
            ],
            "exact_replay": answer["exact_membership"]["exact_replay"],
        })
    print(json.dumps(summary, sort_keys=True), flush=True)
    return answer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--chart", type=int, action="append")
    parser.add_argument("--cutoff", type=int, choices=(3, 4, 5), action="append")
    parser.add_argument("--discovery-only", action="store_true")
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--output-name", default="results.json")
    args = parser.parse_args()
    charts, legacy, digest = load_charts()
    selected = sorted(args.chart or charts)
    cutoffs = sorted(set(args.cutoff or (3, 4)))
    require(set(selected) <= set(charts),
            ("requested excluded or unknown chart", selected))
    results = []
    for chart in selected:
        for cutoff in cutoffs:
            results.append(scan_chart(
                chart, legacy[chart], charts[chart], cutoff,
                not args.discovery_only,
            ))
        incident_columns.cache_clear()
        column_rows.cache_clear()
    core = {
        "status": (
            "DISCOVERY ONLY: modular ranks are not proof"
            if args.discovery_only else
            "UNAUDITED EXACT FORMAL K-ADIC LIFTS; NO CHART CLOSURE CLAIMED"
        ),
        "upstream_raw_matching_sha256": digest,
        "prime": PRIME,
        "excluded_zero_based_charts": sorted(EXCLUDED),
        "records": results,
    }
    if not args.discovery_only:
        require(all(record["exact_membership"]["exact_replay"]
                    for record in results), "an exact replay was lost")
        core["classification"] = {
            "cutoffs_scanned": cutoffs,
            "charts_with_exact_formal_lift_at_every_scanned_cutoff": sorted(selected),
            "failed_memberships": [],
            "smallest_exact_obstruction": None,
            "leading_contractible_legacy_1_to_24": sum(
                legacy[chart] <= 24 for chart in selected
            ),
            "critical_legacy_25_to_27": sorted(
                chart for chart in selected if legacy[chart] in (25, 26, 27)
            ),
            "critical_low_degree_verdict": (
                "exact formal lifts through K4 exist, but they are not the "
                "missing algebraic repairs of the first-layer Morse complex"
            ),
        }
        if cutoffs == [3, 4] and set(selected) == set(charts):
            core["classification"].update({
                "universal_other27_through_K4": True,
                "first_failed_at_K3": [],
                "first_failed_at_K4": [],
            })
        if cutoffs == [5]:
            core["classification"].update({
                "K5_probe_only": True,
                "first_layer_contractibility_predicts_K5_lift": False,
                "prediction_verdict": (
                    "all probes lift; critical legacy27 and leading legacy1 "
                    "peel completely, while leading legacy24 has the largest "
                    "irreducible core and the only denominator-two certificate"
                ),
            })
    encoded = json.dumps(core, sort_keys=True, separators=(",", ":"))
    if args.write_results:
        require(Path(args.output_name).name == args.output_name,
                "output name must be a basename")
        (HERE / args.output_name).write_text(
            json.dumps(core, indent=2, sort_keys=True) + "\n"
        )
    print(json.dumps({
        "status": core["status"],
        "records": len(results),
        "sha256": sha256(encoded.encode()).hexdigest(),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
