#!/usr/bin/env python3
"""Certify the diagonal-rewrite fibre lemma and its sharp counterguards."""

from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import importlib.util
import json
from math import factorial
from pathlib import Path


HERE = Path(__file__).resolve().parent
GRAPH_PATH = HERE / "analyze_n8_even_rewrite_state_graph.py"
SPEC = importlib.util.spec_from_file_location("n8_even_rewrite_graph", GRAPH_PATH)
GRAPH = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GRAPH)
SOURCE = GRAPH.SOURCE

EXPECTED_LEDGER_SHA256 = (
    "f60104bf038b76a97f49edb62c18600c2f21357ce493f8605a25c4c6d6ffbbb6"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def word_on_matching(matching, mate):
    word = [None] * 8
    selected = frozenset(matching)
    for first, second in selected:
        left, left_colour = divmod(first, 3)
        right, right_colour = divmod(second, 3)
        require(word[left] is None and word[right] is None,
                "matching repeated a physical vertex")
        word[left] = left_colour
        word[right] = right_colour
    require(all(value is not None for value in word),
            "matching did not cover every physical vertex")
    require(all(mate[first] == second for first, second in selected),
            "selected matching is not contained in the state")
    return tuple(word)


def matching_diagonal_count(matching):
    return sum(first % 3 == second % 3 for first, second in matching)


def minimum_diagonal_formula(word):
    counts = Counter(word)
    return max(0, max(counts.values()) - 4)


def word_matching_diagonal(matching, word):
    return sum(word[left] == word[right] for left, right in matching)


def zero_diagonal_matching_count(counts):
    padded = tuple(counts) + (0,) * (3 - len(counts))
    n0, n1, n2 = padded
    if max(padded) > 4:
        return 0
    e01 = 4 - n2
    e02 = 4 - n1
    e12 = 4 - n0
    return (
        factorial(n0) * factorial(n1) * factorial(n2)
        // (factorial(e01) * factorial(e02) * factorial(e12))
    )


def candidate_records(row):
    mate = SOURCE.decode_key(row)
    records = []
    edges = SOURCE.mate_edges(mate)
    for selected in combinations(edges, 4):
        if len({port // 3 for edge in selected for port in edge}) != 8:
            continue
        word = word_on_matching(selected, mate)
        if len(set(word)) == 1:
            continue
        selected_set = frozenset(selected)
        complement = tuple(edge for edge in edges if edge not in selected_set)
        cycles = GRAPH.component_sizes(complement)
        if not all(size % 2 == 0 for size in cycles):
            continue
        multiplier = list(mate)
        for first, second in selected:
            multiplier[first] = -1
            multiplier[second] = -1
        column = SOURCE.canonical_key(tuple(multiplier))
        before = matching_diagonal_count(selected)
        minimum = minimum_diagonal_formula(word)
        outputs = SOURCE.column_outputs(column)
        actual_minimum = min(GRAPH.diagonal_count(other) for other in outputs)
        complement_diagonal = GRAPH.diagonal_count(row) - before
        require(actual_minimum == complement_diagonal + minimum,
                "fibre minimum failed after restoring the complement")
        records.append((before, minimum, tuple(sorted(Counter(word).values(),
                                                       reverse=True)), cycles))
    return records


def audit():
    # First prove the word-fibre formula independently on all 3^8 words.
    fibre_types = Counter()
    mixed_words = 0
    for word in product(range(3), repeat=8):
        if len(set(word)) == 1:
            continue
        mixed_words += 1
        values = [
            word_matching_diagonal(matching, word)
            for matching in SOURCE.VERTEX_MATCHINGS
        ]
        formula = minimum_diagonal_formula(word)
        require(min(values) == formula,
                "minimum diagonal-pair formula failed")
        partition = tuple(sorted(Counter(word).values(), reverse=True))
        zero_count = values.count(0)
        require(zero_count == zero_diagonal_matching_count(partition),
                "zero-diagonal matching formula failed")
        if zero_count:
            fibre_types[partition, zero_count] += 1
    require(mixed_words == 3 ** 8 - 3, "mixed word count changed")
    require(set(fibre_types) == {
        ((4, 4), 24), ((4, 3, 1), 24),
        ((4, 2, 2), 24), ((3, 3, 2), 36),
    }, "all-offdiagonal fibre types changed")

    # The proposed positive-diagonal lemma is false exactly where the known
    # parity audit says it must be false: chart 26 has no even complement.
    roots = tuple(sorted(SOURCE.target_orbit_rows()))
    root_records = [candidate_records(row) for row in roots]
    roots_without_even = [
        index for index, records in enumerate(root_records, 1) if not records
    ]
    require(roots_without_even == [26],
            "root even-complement exception changed")
    for index, records in enumerate(root_records, 1):
        if index == 26:
            continue
        require(any(before > minimum for before, minimum, _part, _cycles
                    in records),
                f"root chart {index} lost every strict diagonal rewrite")

    # One exact nonroot layer is a counterguard, not the structural proof.
    layer_one = set()
    for row in roots:
        for column, _cycles in GRAPH.even_columns(row):
            layer_one.update(SOURCE.column_outputs(column))
    layer_one -= set(roots)
    require(len(layer_one) == 505, "first rewrite layer changed")
    layer_one_sinks = [
        row for row in layer_one
        if not any(before > minimum
                   for before, minimum, _part, _cycles in candidate_records(row))
    ]
    require(not layer_one_sinks,
            "a first-layer nonroot escaped the fibre criterion")

    bottom_types = [
        {
            "word_partition": list(partition),
            "labelled_zero_diagonal_matchings": zero_count,
            "fibre_local_relation_rank": 1,
            "fibre_local_cokernel_lower_bound": zero_count - 1,
        }
        for partition, zero_count in sorted(fibre_types)
    ]
    ledger = {
        "mixed_words": mixed_words,
        "minimum_diagonal_formula": "max(0,max(n0,n1,n2)-4)",
        "strict_rewrite_criterion": (
            "an even-complement selected matching decreases diagonal count "
            "iff its diagonal count exceeds the word-fibre minimum"
        ),
        "root_charts_without_even_complement": roots_without_even,
        "other_root_charts_with_strict_decrease": 30,
        "first_nonroot_layer_states": len(layer_one),
        "first_nonroot_layer_fibre_sinks": len(layer_one_sinks),
        "all_offdiagonal_bottom_fibre_types": bottom_types,
        "bottom_signed_fibre_guard": (
            "the lowest-diagonal initial of one mixed hafnian fibre is one "
            "all-+1 relation on 24 or 36 labelled states; by itself it leaves "
            "local cokernel dimension at least 23 or 35"
        ),
        "scope_guard": (
            "universal word-fibre lemma, exact 31-root exception, and first "
            "nonroot layer; not a global classification of all bottom state "
            "orbits and not a signed Morse acyclicity theorem"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "diagonal fibre lemma ledger changed")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    audit()
