#!/usr/bin/env python3
"""Exact two-shell incidence geometry of the minimal N8 degree-seven packet."""

from __future__ import annotations

import argparse
import collections
import hashlib
import importlib.util
import itertools
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROVIDER = (ROOT / "computations" /
            "unaudited-codex-n8-normalized-dfs-degree7-2026-08-23")
WORDS = PROVIDER / "degree7_word_packet.txt"
SEED = PROVIDER / "degree7_tail_seed.txt"
CHECKER = ROOT / "computations" / "verify_n8_normalized_critical_contraction.py"
OUT = HERE / "results_degree7_two_shell_geometry.json"
WORD_SHA = "cc4fd5cf7119646f3722f5dbb32599741cf260116a3a367336fe1054a8b44ae1"
SEED_SHA = "36523c54c1a6dd466f6fe2fe936c3bed1d815d18042fb4c93edc98f92d2c7171"
C5_LABELS = ("00000012", "11000010", "11010012", "11012111", "12012000")


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def sha256_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_checker():
    spec = importlib.util.spec_from_file_location("normalized", CHECKER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def word_label(C, code):
    return "".join(map(str, C.D5.decode_word(code)))


def read_words(C):
    require(sha256_file(WORDS) == WORD_SHA, "word packet hash changed")
    allowed = set()
    with WORDS.open(encoding="ascii") as stream:
        require(stream.readline().split() ==
                ["KRENN_N8_WORD_PACKET_V1", "78", "22"],
                "word packet header changed")
        for line in stream:
            tag, code_text, label = line.split()
            code = int(code_text)
            require(tag == "WORD" and word_label(C, code) == label,
                    "word packet row changed")
            allowed.add(code)
    require(len(allowed) == 78, "word packet census changed")
    canonical_words = {
        min(C.D5.WORD_TRANSFORMS[index][code]
            for index in range(len(C.D5.GROUP)))
        for code in allowed
    }
    require(len(canonical_words) == 22, "word orbit census changed")
    c5_codes = {
        min(C.D5.WORD_TRANSFORMS[index][C.D5.word_code(tuple(map(int, label)))]
            for index in range(len(C.D5.GROUP)))
        for label in C5_LABELS
    }
    require(c5_codes <= canonical_words and len(c5_codes) == 5,
            "contraction word-orbit packet changed")
    return allowed, canonical_words, c5_codes


def read_seed():
    require(sha256_file(SEED) == SEED_SHA, "tail seed hash changed")
    rows = {}
    with SEED.open(encoding="ascii") as stream:
        require(stream.readline().split() ==
                ["KRENN_N8_NORMALIZED_TAIL_V1", "7", "564", "2"],
                "tail seed header changed")
        for line in stream:
            tag, encoded, coefficient = line.split()
            row = bytes.fromhex(encoded)
            require(tag == "ROW" and row not in rows,
                    "tail seed row changed")
            rows[row] = int(coefficient)
    require(len(rows) == 564, "tail seed census changed")
    return rows


def packet_algebra(C, allowed):
    polynomials = {code: C.normalized_generator(code) for code in allowed}
    term_index = collections.defaultdict(set)
    for code, polynomial in polynomials.items():
        for term in polynomial:
            term_index[term].add(code)
    return polynomials, term_index


def incident_columns(C, rows, term_index):
    answer = set()
    for row in rows:
        for term in C.multiset_divisors(row):
            if len(row) - len(term) > 3:
                continue
            for code in term_index.get(term, ()):
                answer.add(C.canonical_column((code, C.quotient(row, term))))
    return answer


def column_images(C, columns, polynomials):
    return {
        column: {
            row: coefficient for row, coefficient in
            C.invariant_column_image(column, polynomials).items()
            if coefficient
        }
        for column in columns
    }


def histogram(values):
    return {str(key): value for key, value in
            sorted(collections.Counter(values).items())}


def transition_record(C, columns, images, previous_rows, c5_codes):
    intersection_histogram = collections.Counter()
    support_histogram = collections.Counter()
    coefficient_histogram = collections.Counter()
    singleton_words = collections.Counter()
    diamond_words = collections.Counter()
    diamond_degree_pairs = collections.Counter()
    diamond_gcd_degree = collections.Counter()
    diamond_coefficient_pairs = collections.Counter()
    family = collections.Counter()
    pair_columns = collections.defaultdict(list)
    for column in columns:
        image = images[column]
        support_histogram[len(image)] += 1
        coefficient_histogram.update(image.values())
        intersection = tuple(sorted(set(image) & previous_rows))
        intersection_histogram[len(intersection)] += 1
        canonical_code = min(C.D5.WORD_TRANSFORMS[index][column[0]]
                             for index in range(len(C.D5.GROUP)))
        label = word_label(C, canonical_code)
        family["contraction_C5" if canonical_code in c5_codes
               else "closure22"] += 1
        if len(intersection) == 1:
            singleton_words[label] += 1
        if len(intersection) == 2:
            diamond_words[label] += 1
            left, right = intersection
            diamond_degree_pairs[tuple(sorted((len(left), len(right))))] += 1
            common = sum((collections.Counter(left) &
                          collections.Counter(right)).values())
            diamond_gcd_degree[common] += 1
            diamond_coefficient_pairs[
                tuple(sorted((image[left], image[right])))
            ] += 1
            pair_columns[intersection].append(column)
    return {
        "columns": len(columns),
        "full_support_size_histogram": dict(sorted(support_histogram.items())),
        "entry_coefficient_histogram": dict(sorted(coefficient_histogram.items())),
        "previous_shell_intersection_histogram": dict(
            sorted(intersection_histogram.items())
        ),
        "relative_singleton_columns": intersection_histogram[1],
        "relative_singletons_by_word_orbit": dict(sorted(singleton_words.items())),
        "relative_diamond_columns": intersection_histogram[2],
        "relative_diamonds_by_word_orbit": dict(sorted(diamond_words.items())),
        "relative_diamond_degree_pairs": {
            f"{left},{right}": count for (left, right), count in
            sorted(diamond_degree_pairs.items())
        },
        "relative_diamond_gcd_degree": dict(sorted(diamond_gcd_degree.items())),
        "relative_diamond_coefficient_pairs": {
            str(key): value for key, value in
            sorted(diamond_coefficient_pairs.items())
        },
        "parallel_two_row_diamonds": sum(
            len(items) * (len(items) - 1) // 2
            for items in pair_columns.values() if len(items) > 1
        ),
        "column_family_histogram": dict(sorted(family.items())),
    }


def projected_singleton_peel(roots, columns, images):
    ordered_rows = tuple(sorted(roots))
    row_index = {row: index for index, row in enumerate(ordered_rows)}
    ordered_columns = tuple(sorted(columns))
    column_rows = []
    row_columns = [[] for _ in ordered_rows]
    for column_index, column in enumerate(ordered_columns):
        entries = [row_index[row] for row in images[column] if row in row_index]
        column_rows.append(entries)
        for row in entries:
            row_columns[row].append(column_index)
    degrees = list(map(len, column_rows))
    initial_singletons = sum(degree == 1 for degree in degrees)
    active = [True] * len(ordered_rows)
    queue = collections.deque(index for index, degree in enumerate(degrees)
                              if degree == 1)
    pivots = []
    while queue:
        column = queue.popleft()
        if degrees[column] != 1:
            continue
        row = next(item for item in column_rows[column] if active[item])
        active[row] = False
        pivots.append((row, column))
        for touched in row_columns[row]:
            degrees[touched] -= 1
            if degrees[touched] == 1:
                queue.append(touched)
    core_rows = {index for index, value in enumerate(active) if value}
    core_columns = {
        index for index, degree in enumerate(degrees) if degree > 0
    }
    core_support_histogram = collections.Counter(degrees[index]
                                                 for index in core_columns)

    # A four-cycle is two surviving rows shared by two surviving columns.
    by_pair = collections.defaultdict(list)
    for column in core_columns:
        entries = sorted(row for row in column_rows[column] if row in core_rows)
        for left, right in itertools.combinations(entries, 2):
            by_pair[left, right].append(column)
    cycles = []
    for (left, right), items in by_pair.items():
        for first, second in itertools.combinations(items, 2):
            cycles.append((ordered_rows[left], ordered_rows[right],
                           ordered_columns[first], ordered_columns[second],
                           degrees[first], degrees[second]))
    require(cycles, "peeled core lost its four-cycle")
    cycle = min(cycles)
    left, right, first, second, first_degree, second_degree = cycle
    return {
        "initial_relative_singletons": initial_singletons,
        "peeled_root_rows": len(pivots),
        "core_root_rows": len(core_rows),
        "core_columns": len(core_columns),
        "core_column_degree_histogram": dict(sorted(core_support_histogram.items())),
        "incidence_four_cycles": len(cycles),
        "row_pairs_supporting_a_four_cycle": sum(
            len(items) >= 2 for items in by_pair.values()
        ),
        "lex_first_four_cycle": {
            "rows": [left.hex(), right.hex()],
            "row_degrees": [len(left), len(right)],
            "columns": [
                {
                    "word": word_label_from_column(first),
                    "word_code": first[0],
                    "multiplier": first[1].hex(),
                    "coefficient_pair": [images[first][left], images[first][right]],
                    "full_support": len(images[first]),
                    "peeled_core_support": first_degree,
                },
                {
                    "word": word_label_from_column(second),
                    "word_code": second[0],
                    "multiplier": second[1].hex(),
                    "coefficient_pair": [images[second][left], images[second][right]],
                    "full_support": len(images[second]),
                    "peeled_core_support": second_degree,
                },
            ],
        },
    }


def word_label_from_column(column):
    code = column[0]
    word = [0] * 8
    for index in range(7, -1, -1):
        word[index] = code % 3
        code //= 3
    return "".join(map(str, word))


def order_coverage(rows, columns, images):
    incident = collections.defaultdict(list)
    for column in columns:
        for row in images[column]:
            if row in rows:
                incident[row].append(column)

    def component(row, feature, orientation):
        value = len(row) if feature == "normalized_degree" else tuple(row)
        if orientation == 1:
            return value
        if isinstance(value, int):
            return -value
        return tuple(-item for item in value)

    records = []
    for order in itertools.permutations(("normalized_degree", "raw_id_lex")):
        for orientations in itertools.product((-1, 1), repeat=2):
            direction = dict(zip(order, orientations))

            def key(row):
                return tuple(component(row, feature, direction[feature])
                             for feature in order)

            covered = 0
            for row in rows:
                if any(all(other == row or key(other) < key(row)
                           for other in images[column])
                       for column in incident[row]):
                    covered += 1
            name = ">".join(("+" if direction[feature] == 1 else "-") +
                            feature for feature in order)
            records.append((covered, name))
    records.sort(reverse=True)
    return {
        "tested_orders": len(records),
        "rows": len(rows),
        "best": [{"covered_rows": count, "order": name}
                 for count, name in records[:4]],
        "orders_covering_every_row": [name for count, name in records
                                      if count == len(rows)],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()

    C = load_checker()
    allowed, canonical_words, c5_codes = read_words(C)
    seed = read_seed()
    polynomials, term_index = packet_algebra(C, allowed)

    # Independently replay the six-column contraction against the frozen seed.
    contraction = collections.defaultdict(C.QQ)
    for scalar, code, multiplier in C.CONTRACTION:
        for row, coefficient in C.invariant_column_image(
                (code, multiplier), polynomials).items():
            contraction[row] += scalar * coefficient
    require(contraction.pop(b"") == 1, "contraction constant changed")
    contraction = {row: value for row, value in contraction.items() if value}
    require({row: int(2 * value) for row, value in contraction.items()} == seed,
            "frozen seed is not the cleared six-column tail")
    roots = set(seed)

    first_columns = incident_columns(C, roots, term_index)
    first_images = column_images(C, first_columns, polynomials)
    first_rows = set().union(*(set(image) for image in first_images.values()))
    require(len(first_columns) == 294 and len(first_rows) == 25153,
            "first shell census changed")

    second_columns = incident_columns(C, first_rows, term_index)
    second_images = column_images(C, second_columns, polynomials)
    second_rows = set().union(*(set(image) for image in second_images.values()))
    new_second_columns = second_columns - first_columns
    require(len(second_columns) == 1187 and len(new_second_columns) == 893
            and len(second_rows) == 107344 and len(second_rows - first_rows) == 82191,
            "second shell census changed")

    first_transition = transition_record(
        C, first_columns, first_images, roots, c5_codes
    )
    second_transition = transition_record(
        C, new_second_columns, second_images, first_rows, c5_codes
    )
    peel = projected_singleton_peel(roots, first_columns, first_images)
    require((peel["initial_relative_singletons"], peel["peeled_root_rows"],
             peel["core_root_rows"], peel["core_columns"])
            == (151, 174, 390, 77), "root projected core changed")

    root_order = order_coverage(roots, first_columns, first_images)
    first_row_order = order_coverage(first_rows, second_columns, second_images)
    require(not root_order["orders_covering_every_row"] and
            not first_row_order["orders_covering_every_row"],
            "a fixed degree/lex monovariant unexpectedly appeared")

    if args.mutate:
        require(peel["core_root_rows"] == 389,
                "hostile projected-core mutation survived")

    result = {
        "verdict": "TWO_SHELL_PACKET_HAS_RELATIVE_SINGLETONS_BUT_A_390_ROW_77_COLUMN_CRITICAL_CORE_WITH_FOUR_CYCLES",
        "scope": (
            "minimal 78-word homogeneous degree-seven packet; exact first "
            "two incidence shells only; no span or full DFS decision"
        ),
        "inputs": {
            "word_packet_sha256": WORD_SHA,
            "tail_seed_sha256": SEED_SHA,
            "literal_words": len(allowed),
            "word_orbits": len(canonical_words),
            "tail_roots": len(roots),
        },
        "first_shell": {
            "columns": len(first_columns),
            "cumulative_rows": len(first_rows),
            "new_rows": len(first_rows - roots),
            "row_degree_histogram": histogram(map(len, first_rows)),
            "transition": first_transition,
        },
        "second_shell": {
            "new_columns": len(new_second_columns),
            "cumulative_columns": len(second_columns),
            "new_rows": len(second_rows - first_rows),
            "cumulative_rows": len(second_rows),
            "row_degree_histogram": histogram(map(len, second_rows)),
            "transition_for_new_columns": second_transition,
        },
        "root_projection_singleton_peel": peel,
        "decreasing_statistic_screen": {
            "features": ["normalized degree (equivalently inverse t-degree)",
                         "canonical raw-ID lex word"],
            "root_rows": root_order,
            "first_shell_rows": first_row_order,
            "conclusion": (
                "no fixed priority/orientation of degree and raw-ID lex makes "
                "every relevant row the unique maximum of an incident column"
            ),
        },
        "interpretation": (
            "singleton peeling explains only 174 of 564 roots. The surviving "
            "first-shell projection already contains literal incidence "
            "four-cycles, so a human contraction needs a state-dependent "
            "pivot/collapse height or additional word orbits; neither degree "
            "nor raw-ID lex is a global monovariant"
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = hashlib.sha256(logical.encode()).hexdigest()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        OUT.write_text(rendered, encoding="utf-8")
    if args.check_results:
        require(OUT.read_text(encoding="utf-8") == rendered,
                "frozen result differs")
    print(json.dumps({
        "first_columns_rows": [len(first_columns), len(first_rows)],
        "second_new_columns_rows": [len(new_second_columns),
                                     len(second_rows - first_rows)],
        "first_relative_singletons_diamonds": [
            first_transition["relative_singleton_columns"],
            first_transition["relative_diamond_columns"],
        ],
        "second_relative_singletons_diamonds": [
            second_transition["relative_singleton_columns"],
            second_transition["relative_diamond_columns"],
        ],
        "root_core": [peel["core_root_rows"], peel["core_columns"]],
        "logical_sha256": result["logical_sha256"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
