#!/usr/bin/env python3
"""Exact labelled root star on the first filtered Macaulay page in chart 26.

The chart is localized only at its three pure anchor monomials.  Exhaustive
labelled enumeration shows that precisely two mixed generator terms use only
chart-support cells.  Hence every anchor-Laurent translate incident to the
pure root is a unit translate of one of two columns.
"""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE_PATH = HERE / "verify_n8_full_source_cycle_product_membership.py"
SPEC = importlib.util.spec_from_file_location("n8_chart26_labelled_source", SOURCE_PATH)
SOURCE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SOURCE)
CHART_PATH = HERE / "verify_n8_target_triple_localization_orbits.py"
CHART_SPEC = importlib.util.spec_from_file_location("n8_chart26_orbit_guard", CHART_PATH)
CHARTS = importlib.util.module_from_spec(CHART_SPEC)
CHART_SPEC.loader.exec_module(CHARTS)
QQ = Fraction
EXPECTED_LEDGER_SHA256 = (
    "479d214a27f27710ae0a6ff93a1a2c39d99e3afa2376d26d588b26ea9e6c83dc"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def quotient(dividend, divisor):
    answer = list(dividend)
    for value in divisor:
        answer.remove(value)
    return tuple(answer)


def diagonal_count(row):
    return sum(left_colour == right_colour
               for _left, _right, left_colour, right_colour in row)


def component_sizes(row):
    adjacency = [set() for _vertex in SOURCE.VERTICES]
    for left, right, _left_colour, _right_colour in row:
        adjacency[left].add(right)
        adjacency[right].add(left)
    unseen = set(SOURCE.VERTICES)
    sizes = []
    while unseen:
        root = min(unseen)
        component = {root}
        queue = [root]
        while queue:
            vertex = queue.pop()
            for other in adjacency[vertex]:
                if other not in component:
                    component.add(other)
                    queue.append(other)
        unseen -= component
        sizes.append(len(component))
    return tuple(sorted(sizes, reverse=True))


def encode_row(row):
    return [[left, right, left_colour, right_colour]
            for left, right, left_colour, right_colour in row]


def rank_over_q(columns):
    basis = {}
    for source in columns:
        vector = dict(source)
        while vector:
            pivot = min(vector)
            if pivot not in basis:
                value = vector[pivot]
                basis[pivot] = {
                    row: coefficient / value
                    for row, coefficient in vector.items()
                }
                break
            value = vector[pivot]
            for row, coefficient in basis[pivot].items():
                output = vector.get(row, QQ(0)) - value * coefficient
                if output:
                    vector[row] = output
                else:
                    vector.pop(row, None)
    return len(basis)


def audit():
    root = SOURCE.SUPPORT_PRODUCT
    support = SOURCE.SUPPORT_SET
    anchors = tuple(tuple(
        variable for variable in root if variable[2] == colour
    ) for colour in SOURCE.COLOURS)
    require(all(len(anchor) == 4 for anchor in anchors),
            "chart anchor ceased to be a perfect matching monomial")
    require(tuple(sorted(sum(anchors, ()))) == root,
            "three anchor monomials no longer multiply to the chart root")

    # Verify independently that this literal expanded-prism support is chart26.
    mate = [-1] * 24
    for left, right, colour in SOURCE.COLOURED_SUPPORT:
        first, second = 3 * left + colour, 3 * right + colour
        mate[first] = second
        mate[second] = first
    roots = tuple(sorted(CHARTS.SOURCE.target_orbit_rows()))
    require(roots.index(CHARTS.SOURCE.canonical_key(tuple(mate))) + 1 == 26,
            "literal support is no longer localization chart 26")

    # Exhaust all labelled hafnian terms.  A Laurent translate can contain
    # root times anchor powers only if its selected generator term itself uses
    # support cells; off-support denominators are forbidden.
    support_terms = []
    mixed_support_terms = []
    for word in __import__("itertools").product(SOURCE.COLOURS, repeat=8):
        pure = len(set(word)) == 1
        for term in SOURCE.word_terms(word):
            if set(term) <= support:
                support_terms.append((word, term))
                if not pure:
                    mixed_support_terms.append((word, term))
    require(len(support_terms) == 5 and len(mixed_support_terms) == 2,
            "chart-support perfect-matching census changed")

    columns = tuple(sorted(SOURCE.incident_columns(root), key=repr))
    require(len(columns) == 2,
            "chart26 labelled root incident-column count changed")
    require({(word, selected) for word, selected in mixed_support_terms}
            == {(word, quotient(root, multiplier))
                for word, multiplier in columns},
            "incident columns do not equal the two mixed support terms")

    top_supports = []
    full_histograms = []
    column_records = []
    for word, multiplier in columns:
        require(set(multiplier) <= support and len(multiplier) == 8,
                "root multiplier left the chart support")
        require(component_sizes(multiplier) == (5, 3),
                "chart26 complement ceased to have odd (5,3) type")
        outputs = SOURCE.column_rows((word, multiplier))
        require(len(outputs) == 105 and outputs.count(root) == 1,
                "labelled fibre lost its unique root occurrence")
        histogram = Counter(map(diagonal_count, outputs))
        require(histogram == Counter({12: 3, 10: 30, 9: 48, 8: 24}),
                "chart26 labelled fibre diagonal histogram changed")
        top = frozenset(row for row in outputs if diagonal_count(row) == 12)
        require(len(top) == 3 and root in top,
                "diagonal-12 initial support changed")
        top_supports.append(top)
        full_histograms.append(dict(sorted(histogram.items(), reverse=True)))
        selected = quotient(root, multiplier)
        column_records.append({
            "word": list(word),
            "selected_support_term": encode_row(selected),
            "support_multiplier": encode_row(multiplier),
            "complement_components": list(component_sizes(multiplier)),
            "anchor_denominator_exponents": [0, 0, 0],
        })

    require(top_supports[0] & top_supports[1] == {root},
            "two labelled initial columns overlap away from the root")
    rows = tuple(sorted(top_supports[0] | top_supports[1]))
    row_index = {row: index for index, row in enumerate(rows)}
    matrix_columns = tuple({row_index[row]: QQ(1) for row in support}
                           for support in top_supports)
    rank = rank_over_q(matrix_columns)
    require(len(rows) == 5 and rank == 2,
            "labelled first-page matrix rank changed")

    # An explicit left-cokernel functional with value one on the root.
    unique_first = min(top_supports[0] - {root})
    unique_second = min(top_supports[1] - {root})
    witness = {root: QQ(1), unique_first: QQ(-1), unique_second: QQ(-1)}
    require(all(sum(witness.get(rows[row], 0) * coefficient
                    for row, coefficient in column.items()) == 0
                for column in matrix_columns),
            "root-survival cokernel witness stopped annihilating the block")
    require(witness[root] == 1,
            "root-survival witness lost its target pairing")

    matrix_record = tuple(tuple(sorted(column.items()))
                          for column in matrix_columns)
    witness_record = tuple(sorted(
        (row_index[row], value.numerator, value.denominator)
        for row, value in witness.items()
    ))
    ledger = {
        "chart": 26,
        "labelled_support_cells": len(root),
        "pure_anchor_monomials": [encode_row(anchor) for anchor in anchors],
        "all_support_contained_hafnian_terms": len(support_terms),
        "pure_support_contained_terms": len(support_terms) - len(mixed_support_terms),
        "mixed_support_contained_terms": len(mixed_support_terms),
        "labelled_root_incident_columns": len(columns),
        "column_records": column_records,
        "full_fibre_diagonal_histograms": full_histograms,
        "first_page_diagonal_level": 12,
        "first_strict_lower_diagonal_level": 10,
        "first_page_rows": len(rows),
        "first_page_columns": len(matrix_columns),
        "first_page_rank_over_Q": rank,
        "first_page_source_kernel_dimension": len(matrix_columns) - rank,
        "first_page_target_cokernel_dimension": len(rows) - rank,
        "two_column_initial_intersection_rows": len(
            top_supports[0] & top_supports[1]
        ),
        "matrix_sha256": sha256(repr(matrix_record).encode()).hexdigest(),
        "root_cokernel_witness_sha256": sha256(
            repr(witness_record).encode()
        ).hexdigest(),
        "root_class_survives_two_column_star": True,
        "root_class_survives_closed_first_page": "unresolved",
        "anchor_local_completeness": (
            "any column incident to root times powers of the three anchors "
            "must select a support-contained hafnian term; exhaustive labelled "
            "enumeration finds only these two mixed terms, and anchor-power "
            "translations are Laurent-unit copies of this block"
        ),
        "scope_guard": (
            "exact labelled two-column root star on the first associated "
            "diagonal page in chart26; no orbit mixing and no off-support "
            "denominator; columns incident to the four nonroot top rows must "
            "be closed before this becomes a full first-page cokernel"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "chart26 labelled first-page ledger changed")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    audit()
