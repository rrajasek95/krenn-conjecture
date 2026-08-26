#!/usr/bin/env python3
"""Exact PM4/PM6 audit of the translated five-column gain bridge.

The third frozen separator is the only one involving a quadratic-minimum
word.  This checker identifies its literal four-site and six-site hafnian
fibres, tests source-label compatibility, and Schur-contracts one canonical
quadratic translate through the independently acyclic y^8/y^9 layers.  It
never loads or scans the 63.6-million-row global y^10 core.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import importlib.util
import json
import sys
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PACKET = ROOT / "computations/unaudited-codex-n8-degree8-antichain-cells-2026-08-23"
PACKET_SCRIPT = PACKET / "audit_degree8_antichain_cells.py"
PACKET_RESULT = PACKET / "results_degree8_antichain_cells.json"
OUT = HERE / "results_pm4_pm6_translated_bridge.json"
EXPECTED_PACKET_LOGICAL = "4b33611aa61c89ea34de63a4a07b002d0dfde8c7960151a88d888efb305edea2"
Q = Fraction


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def fraction_record(value):
    value = Q(value)
    return [value.numerator, value.denominator]


def add(work, row, value):
    result = work.get(row, Q(0)) + value
    if result:
        work[row] = result
    else:
        work.pop(row, None)


def histogram(values):
    counter = collections.Counter(values)
    return {str(key): value for key, value in sorted(counter.items(), key=lambda x: str(x[0]))}


def run(mutate=False):
    frozen = json.loads(PACKET_RESULT.read_text(encoding="utf-8"))
    require(frozen["logical_sha256"] == EXPECTED_PACKET_LOGICAL,
            "frozen gain-cell package changed")
    P = load("pm_bridge_packet", PACKET_SCRIPT)
    A = load("pm_bridge_prolong", P.PROLONG)
    M = A.load_checker()
    cache = {}

    @lru_cache(None)
    def minimum_layer(code):
        polynomial = M.normalized_generator(code)
        degree = min(map(len, polynomial))
        return degree, tuple(sorted(
            (row, coefficient) for row, coefficient in polynomial.items()
            if len(row) == degree
        ))

    separator_rounds = frozen["hard11_exchange_closure"]["rounds"][:4]
    word_types = {}
    round_type_census = []
    for record in separator_rounds:
        census = collections.Counter()
        for item in record["separator"]:
            degree, layer = minimum_layer(item["word_code"])
            key = degree, len(layer)
            census[key] += 1
            word_types[item["word"]] = {
                "minimum_y_degree": degree,
                "minimum_support": len(layer),
            }
        round_type_census.append({
            f"degree{degree}_support{support}": count
            for (degree, support), count in sorted(census.items())
        })
    require(round_type_census == [
        {"degree1_support1": 4},
        {"degree1_support1": 4},
        {"degree2_support3": 1, "degree3_support15": 4},
        {"degree1_support1": 22},
    ], "gain-cell PM layer census changed")

    support = tuple(M.D5.COORDINATES[value] for value in M.D5.SUPPORT_IDS)

    def fixed_edges(code):
        word = M.D5.decode_word(code)
        return tuple(sorted(
            (left, right, colour)
            for left, right, colour, right_colour in support
            if colour == right_colour
            and word[left] == colour and word[right] == colour
        ))

    def unmatched(code):
        covered = {vertex for left, right, _colour in fixed_edges(code)
                   for vertex in (left, right)}
        return tuple(sorted(set(range(8)) - covered))

    def equality_partition(code, vertices):
        word = M.D5.decode_word(code)
        return tuple(sorted(
            tuple(vertex for vertex in vertices if word[vertex] == colour)
            for colour in range(3)
            if any(word[vertex] == colour for vertex in vertices)
        ))

    bridge = separator_rounds[2]["separator"]
    pm4_item = next(item for item in bridge
                    if word_types[item["word"]]["minimum_y_degree"] == 2)
    pm6_items = [item for item in bridge
                 if word_types[item["word"]]["minimum_y_degree"] == 3]
    require(pm4_item["word"] == "11001012"
            and len(pm6_items) == 4
            and {item["word"] for item in pm6_items} == {"12011110"},
            "PM4/PM6 bridge labels changed")

    pm4_column = (pm4_item["word_code"], bytes.fromhex(pm4_item["multiplier"]))
    pm6_columns = [
        (item["word_code"], bytes.fromhex(item["multiplier"]))
        for item in pm6_items
    ]
    pm4_actual = M.normalized_column_orbit(pm4_column)
    pm6_actual_by_column = [M.normalized_column_orbit(column)
                            for column in pm6_columns]
    require(len(pm4_actual) == 4
            and all(len(orbit) == 4 for orbit in pm6_actual_by_column),
            "bridge actual-orbit sizes changed")

    common_pm4_edge = set(fixed_edges(pm4_actual[0][0]))
    for code, _multiplier in pm4_actual[1:]:
        common_pm4_edge &= set(fixed_edges(code))
    require(common_pm4_edge == {(2, 5, 0)},
            "PM4 orbit lost its common chart edge")

    fibre_records = []
    for code4, multiplier4 in pm4_actual:
        edges4 = set(fixed_edges(code4))
        require(len(edges4) == 2 and (2, 5, 0) in edges4,
                "PM4 word is not a two-fixed-edge chart coefficient")
        exchange_edge = next(iter(edges4 - {(2, 5, 0)}))
        u4 = unmatched(code4)
        matches = []
        for orbit in pm6_actual_by_column:
            selected = [(code, multiplier) for code, multiplier in orbit
                        if set(fixed_edges(code)) == {exchange_edge}]
            require(len(selected) == 1,
                    "PM6 orbit lacks the uniquely nested six-site fibre")
            matches.append(selected[0])
        codes6 = {code for code, _multiplier in matches}
        require(len(codes6) == 1,
                "four PM6 columns do not use one nested source word")
        code6 = next(iter(codes6))
        u6 = unmatched(code6)
        require(set(u6) == set(u4) | {2, 5},
                "PM6 unmatched set is not PM4 plus the common-edge endpoints")

        partition4 = equality_partition(code4, u4)
        partition6_on4 = equality_partition(code6, u4)
        require(partition4 != partition6_on4,
                "hostile source-label mismatch disappeared")

        degree4, layer4_record = minimum_layer(code4)
        degree6, layer6_record = minimum_layer(code6)
        require((degree4, len(layer4_record), degree6, len(layer6_record))
                == (2, 3, 3, 15), "literal PM support sizes changed")
        layer4 = {row: value for row, value in layer4_record}
        layer6 = {row: value for row, value in layer6_record}
        word6 = M.D5.decode_word(code6)
        bridge_variable = M.D5.COORDINATE_ID[(2, 5, word6[2], word6[5])]
        require(M.D5.IS_OFF_SUPPORT[bridge_variable],
                "nested PM6 bridge variable became a chart cell")
        quotients = set()
        for row in layer6:
            if bridge_variable not in row:
                continue
            position = row.index(bridge_variable)
            quotients.add(row[:position] + row[position + 1:])
        require(len(quotients) == 3,
                "PM6 edge slice stopped being a three-term PM4 coefficient")
        overlap = len(set(layer4) & quotients)
        require(overlap == 0,
                "PM4 and nested PM6 source matrices unexpectedly aligned")
        fibre_records.append({
            "pm4_word": A.word_label(M, code4),
            "pm4_multiplier": multiplier4.hex(),
            "pm4_fixed_edges": [list(edge) for edge in sorted(edges4)],
            "pm4_unmatched_vertices": list(u4),
            "pm4_colour_partition": [list(block) for block in partition4],
            "pm6_word": A.word_label(M, code6),
            "pm6_unmatched_vertices": list(u6),
            "pm6_restriction_colour_partition": [list(block) for block in partition6_on4],
            "pm6_column_multipliers": [multiplier.hex() for _code, multiplier in matches],
            "nested_edge_variable": list(M.D5.COORDINATES[bridge_variable]),
            "pm4_terms": [row.hex() for row in sorted(layer4)],
            "pm6_edge_slice_quotients": [row.hex() for row in sorted(quotients)],
            "literal_term_overlap": overlap,
            "global_colour_permutation_can_align": False,
        })

    # A canonical quadratic translation on the disjoint physical edges 01,23.
    translation = bytes((1, 117))
    require(tuple(M.D5.COORDINATES[value] for value in translation)
            == ((0, 1, 0, 1), (2, 3, 0, 0)),
            "canonical quadratic translation changed")
    translated_columns = collections.defaultdict(Q)
    for item in bridge:
        multiplier = bytes(sorted(bytes.fromhex(item["multiplier"]) + translation))
        column = M.canonical_normalized_column((item["word_code"], multiplier))
        translated_columns[column] += Q(*item["coefficient"])
    translated_columns = {column: value for column, value in translated_columns.items()
                          if value}
    require(len(translated_columns) == 5,
            "quadratic translation collided bridge columns")
    work = {}
    for column, value in translated_columns.items():
        for row, coefficient in A.column_entries(M, column, cache).items():
            add(work, row, value * coefficient)
    initial_histogram = collections.Counter(map(len, work))
    require(initial_histogram == {8: 3, 9: 84, 10: 438},
            "translated bridge degree profile changed")

    unique_codes = collections.defaultdict(list)
    for code in range(3 ** 8):
        if len(set(M.D5.decode_word(code))) == 1:
            continue
        degree, layer = minimum_layer(code)
        if degree == 1 and len(layer) == 1 and layer[0][1] == 1:
            unique_codes[layer[0][0][0]].append(code)
    require(len(unique_codes) == 240,
            "unique-linear pivots stopped covering every y variable")

    pivot_cache = {}

    def pivot(row):
        if row in pivot_cache:
            return pivot_cache[row]
        candidates = set()
        for position, variable in enumerate(row):
            multiplier = row[:position] + row[position + 1:]
            for code in unique_codes.get(variable, ()):
                candidates.add(M.canonical_normalized_column((code, multiplier)))
        for column in sorted(candidates):
            entries = A.column_entries(M, column, cache)
            minimum = min(map(len, entries))
            minimum_entries = {term: value for term, value in entries.items()
                               if len(term) == minimum}
            if minimum == len(row) and set(minimum_entries) == {row}:
                pivot_cache[row] = column, entries, minimum_entries[row]
                return pivot_cache[row]
        raise RuntimeError(f"no invariant unique-linear pivot for {row.hex()}")

    pivot_records = []
    while True:
        lower = [row for row in work if len(row) < 10]
        if not lower:
            break
        row = min(lower, key=lambda value: (len(value), value))
        value = work[row]
        column, entries, coefficient = pivot(row)
        factor = value / coefficient
        for output, entry in entries.items():
            add(work, output, -factor * entry)
        pivot_records.append({
            "row": row.hex(),
            "row_degree": len(row),
            "row_coefficient": fraction_record(value),
            "word": A.word_label(M, column[0]),
            "word_code": column[0],
            "multiplier": column[1].hex(),
            "pivot_coefficient": coefficient,
            "subtraction_factor": fraction_record(factor),
        })
        require(len(pivot_records) <= 1000 and len(work) <= 100000,
                "bounded translated bridge contraction exceeded guard")
    terminal_histogram = collections.Counter(map(len, work))
    require(len(pivot_records) == 101
            and terminal_histogram == {10: 1064, 11: 3088, 12: 6664},
            "translated bridge Schur remainder changed")
    degree10 = {row: value for row, value in work.items() if len(row) == 10}
    require(collections.Counter(degree10.values()) == {Q(1): 556, Q(-1): 508},
            "degree-ten coefficient profile changed")

    core_incidence = collections.Counter()
    zero_incidence = []
    for row in degree10:
        count = 0
        for column in M.bounded_incident_columns({row: Q(1)}, 12):
            degree, layer = minimum_layer(column[0])
            if (degree, len(layer)) != (2, 3):
                continue
            entries = A.column_entries(M, column, cache)
            minimum = min(map(len, entries))
            minimum_rows = {term for term in entries if len(term) == minimum}
            if minimum == 10 and row in minimum_rows:
                count += 1
        core_incidence[count] += 1
        if not count:
            zero_incidence.append(row)
    require(not zero_incidence and min(core_incidence) == 6
            and max(core_incidence) == 20,
            "translated remainder escaped the PM4 core incidence")

    if mutate:
        require(any(record["literal_term_overlap"] for record in fibre_records),
                "hostile source-fibre alignment mutation survived")

    degree10_record = [
        [row.hex(), *fraction_record(value)]
        for row, value in sorted(degree10.items())
    ]
    result = {
        "verdict": "PM4_PM6_UNMATCHED_SETS_NEST;SOURCE_LABELS_DO_NOT;TRANSLATED_REMAINDER_STAYS_IN_PM4_CORE",
        "scope": (
            "one exact canonical quadratic translate of the frozen five-column "
            "gain bridge, with deterministic contraction through y8/y9; no scan "
            "of the producer-reported 63,603,821-row R6 transfer tail"
        ),
        "minimum_layer_lemma": (
            "for a word w, its compatible chart edges E(w) form a matching; "
            "the normalized minimum layer is the literal perfect-matching "
            "coefficient on the unmatched vertices"
        ),
        "four_gain_cells": {
            "round_type_census": round_type_census,
            "word_types": word_types,
            "unique_PM4_PM6_bridge_round": 2,
        },
        "PM4_PM6_fibre_audit": {
            "common_PM4_chart_edge": [2, 5, 0],
            "actual_orbit_records": fibre_records,
            "unmatched_vertex_sets_nest": True,
            "same_source_labelled_six_vertex_fibre": False,
            "reason": (
                "on every actual orbit representative the PM6 coefficient "
                "restricts to a different equality partition on U4; its "
                "edge-25 PM4 slice has zero literal term overlap with the PM4 word"
            ),
        },
        "quadratic_translate": {
            "variables": [list(M.D5.COORDINATES[value]) for value in translation],
            "implicit_homogeneous_factor": "translation * t^2",
            "translated_columns": len(translated_columns),
            "initial_degree_histogram": dict(sorted(initial_histogram.items())),
            "unique_linear_pivots": len(pivot_records),
            "pivot_records": pivot_records,
            "terminal_degree_histogram": dict(sorted(terminal_histogram.items())),
            "degree10_terms": len(degree10),
            "degree10_coefficient_histogram": histogram(degree10.values()),
            "degree10_PM4_incidence_histogram": dict(sorted(core_incidence.items())),
            "degree10_rows_without_PM4_incidence": len(zero_incidence),
            "degree10_sha256": hashlib.sha256(json.dumps(
                degree10_record, separators=(",", ":")
            ).encode()).hexdigest(),
            "degree10_rows": degree10_record,
        },
        "conclusion": (
            "The proposed N4-to-N6 common-fibre theorem fails at literal "
            "endpoint labels even though the unmatched vertex sets nest. "
            "After exact lower-layer contraction, the chosen translate exposes "
            "1,064 nonzero y10 rows, all inside the coupled PM4 incidence core; "
            "it supplies neither a leaf nor a core closure."
        ),
        "global_transfer_scope_guard": (
            "the producer-reported 63.6M y10 export currently propagates only "
            "the truncated degree-six boundary R6 and has not yet been audited "
            "to include pre-existing Fh/certificate residuals in degrees7..10; "
            "it is not used or called the actual direct-Fh core here"
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = hashlib.sha256(logical.encode()).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()
    result = run(args.mutate)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        OUT.write_text(rendered, encoding="utf-8")
    if args.check_results:
        require(OUT.read_text(encoding="utf-8") == rendered,
                "frozen PM4/PM6 bridge result changed")
    print(json.dumps({
        "verdict": result["verdict"],
        "same_source_fibre": result["PM4_PM6_fibre_audit"]["same_source_labelled_six_vertex_fibre"],
        "degree10_terms": result["quadratic_translate"]["degree10_terms"],
        "logical_sha256": result["logical_sha256"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
