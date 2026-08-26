#!/usr/bin/env python3
"""Independent raw source-labelled K-adic audit for dangerous charts 25--28.

This file deliberately does not import the producer implementation.  Rows are
rebuilt from the 105 perfect matchings of eight labelled vertices.  A source
column is a mixed word times an eight-cell monomial; its 105 output rows retain
the source word and multiplier exactly.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from collections import deque
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import argparse
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
N = 8
COLORS = range(3)
EDGES = tuple(combinations(range(N), 2))
CELLS = tuple((u, v, a, b) for u, v in EDGES for a in COLORS for b in COLORS)
CELL_ID = {cell: index for index, cell in enumerate(CELLS)}
CELL_NAME_ID = {
    f"x{u}{v}_{a}{b}": index
    for index, (u, v, a, b) in enumerate(CELLS)
}
UPSTREAM = (
    HERE.parent / "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
    / "results.json"
)
EXPECTED_UPSTREAM_SHA256 = (
    "2b57a9919ee3e04186d5ede01280b43c6e7a9b9ba3ea35b9d55b82adeda4e3a8"
)
EXPECTED_D3_CERTIFICATE_SHA256 = {
    25: "49ca8ede7525d0def313f3e05421895c96fdca0ce9791144bef48d697976867b",
    26: "e3afabc74637f1eb402a03939663beae5e37f0a905afb600ea629ccf998d7321",
    27: "79361a351291b6ea44cefcbfbae7e2c6240230c2c9c4d13881c62ebf77aa0c53",
    28: "b5d635e28ed4f70df82c400b72e7f9111e3379080a0bbae0eae6aefb9a739d44",
}
EXPECTED_D4_CERTIFICATE_SHA256 = {
    25: "0509ec05898faab1d68d5068bf449010a9f57a9caffab8920c04d3765f0c3de6",
    26: "c1d65eacde76602b8cc06a5dd40633c68ff58b1f06923102d0d226ad9ebb687b",
    27: "8bb3bf535a3b15f9b25acf618269b4f2aeabc1648bcdaeda3291e8ce180901d0",
    28: "e29b5af0c83e7ccf5480c9abc24c0944b9fad4e13b81e0e42f8ae1677852a17e",
}
EXPECTED_D4_LEDGER_SHA256 = (
    "e457af40ab98c3bc0274f75c793c7a480e8e270993d48caf3d168dea9e03926a"
)
CHARTS = {
    25: (
        ((0, 1), (2, 3), (4, 5), (6, 7)),
        ((0, 2), (1, 3), (4, 6), (5, 7)),
        ((0, 4), (1, 5), (2, 6), (3, 7)),
    ),
    26: (
        ((0, 1), (2, 3), (4, 5), (6, 7)),
        ((0, 2), (1, 3), (4, 6), (5, 7)),
        ((0, 4), (1, 5), (2, 7), (3, 6)),
    ),
    27: (
        ((0, 1), (2, 3), (4, 5), (6, 7)),
        ((0, 2), (1, 3), (4, 6), (5, 7)),
        ((0, 4), (1, 6), (2, 5), (3, 7)),
    ),
    28: (
        ((0, 1), (2, 3), (4, 5), (6, 7)),
        ((0, 2), (1, 3), (4, 6), (5, 7)),
        ((0, 4), (1, 6), (2, 7), (3, 5)),
    ),
}


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
    for position, mate in enumerate(vertices[1:], 1):
        remainder = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(remainder):
            answer.append(((first, mate),) + tail)
    return tuple(answer)


PM8 = perfect_matchings(tuple(range(N)))
require(len(PM8) == 105, "perfect matching census changed")


def anchor_ids(chart):
    return frozenset(
        CELL_ID[(u, v, colour, colour)]
        for colour, matching in enumerate(CHARTS[chart])
        for u, v in matching
    )


def row_degree(row, anchors):
    return sum(cell not in anchors for cell in row)


@lru_cache(maxsize=None)
def word_terms(word):
    return tuple(bytes(sorted(
        CELL_ID[(u, v, word[u], word[v])] for u, v in matching
    )) for matching in PM8)


@lru_cache(maxsize=None)
def column_rows(column):
    word, multiplier = column
    return tuple(bytes(sorted(multiplier + term)) for term in word_terms(word))


@lru_cache(maxsize=None)
def word_degree_histogram(word, anchor_tuple):
    anchors = frozenset(anchor_tuple)
    return tuple(sorted(Counter(row_degree(row, anchors)
                                for row in word_terms(word)).items()))


def column_minimum_degree(column, anchors):
    word, multiplier = column
    multiplier_degree = row_degree(multiplier, anchors)
    minimum_word_degree = word_degree_histogram(word, tuple(sorted(anchors)))[0][0]
    return multiplier_degree + minimum_word_degree


@lru_cache(maxsize=None)
def incident_columns(row):
    """Every actual labelled mixed source column containing ``row``."""
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
        chosen = frozenset(selected)
        multiplier = bytes(row[index] for index in range(12)
                           if index not in chosen)
        answer.add((tuple(word), multiplier))
    return tuple(sorted(answer, key=repr))


def target_by_degree(chart, maximum=4):
    """Raw H_0 H_1 H_2 target, grouped by K degree."""
    anchors = anchor_ids(chart)
    pure = []
    for colour in COLORS:
        groups = defaultdict(list)
        for row in word_terms((colour,) * N):
            degree = row_degree(row, anchors)
            if degree <= maximum:
                groups[degree].append(row)
        pure.append(groups)
    targets = {degree: Counter() for degree in range(maximum + 1)}
    for degrees in product(range(maximum + 1), repeat=3):
        total = sum(degrees)
        if total > maximum:
            continue
        for terms in product(*(pure[colour].get(degrees[colour], ())
                               for colour in COLORS)):
            targets[total][bytes(sorted(b"".join(terms)))] += 1
    return targets


def seed_columns(chart):
    """All mixed anchor factorizations, rebuilt from the coloured skeleton."""
    matchings = CHARTS[chart]
    anchors = anchor_ids(chart)
    edge_colour = {
        edge: colour for colour, matching in enumerate(matchings)
        for edge in matching
    }
    anchor_row = bytes(sorted(anchors))
    seeds = set()
    for matching in PM8:
        if not all(edge in edge_colour for edge in matching):
            continue
        word = [None] * N
        selected = []
        for u, v in matching:
            colour = edge_colour[u, v]
            word[u] = word[v] = colour
            selected.append(CELL_ID[(u, v, colour, colour)])
        if len(set(word)) == 1:
            continue
        multiplier = list(anchor_row)
        for cell in selected:
            multiplier.remove(cell)
        column = (tuple(word), bytes(sorted(multiplier)))
        require(column_minimum_degree(column, anchors) == 0,
                "anchor seed lost its degree-zero term")
        seeds.add(column)
    return tuple(sorted(seeds, key=repr))


def close_leading(start_rows, anchors, degree):
    rows = set(start_rows)
    frontier = deque(sorted(start_rows))
    columns = set()
    while frontier:
        row = frontier.popleft()
        for column in incident_columns(row):
            if column in columns or column_minimum_degree(column, anchors) != degree:
                continue
            columns.add(column)
            for output in column_rows(column):
                if row_degree(output, anchors) != degree or output in rows:
                    continue
                rows.add(output)
                frontier.append(output)
    return tuple(sorted(rows)), tuple(sorted(columns, key=repr))


def lower_component(chart, targets=None):
    """Complete actual-row source component through K-degree three."""
    anchors = anchor_ids(chart)
    targets = targets or target_by_degree(chart)
    seeds = seed_columns(chart)
    start2 = set(targets[2])
    for column in seeds:
        start2.update(row for row in column_rows(column)
                      if row_degree(row, anchors) == 2)
    rows2, columns2 = close_leading(start2, anchors, 2)
    lower2 = seeds + columns2
    start3 = set(targets[3])
    for column in lower2:
        start3.update(row for row in column_rows(column)
                      if row_degree(row, anchors) == 3)
    rows3, columns3 = close_leading(start3, anchors, 3)
    rows = (bytes(sorted(anchors)),) + rows2 + rows3
    columns = lower2 + columns3
    return rows, columns, {
        "seed_columns": len(seeds),
        "degree2_rows": len(rows2),
        "degree2_columns": len(columns2),
        "degree3_rows": len(rows3),
        "degree3_columns": len(columns3),
    }


def truncated_column(column, anchors, maximum=4):
    return Counter(
        row for row in column_rows(column)
        if row_degree(row, anchors) <= maximum
    )


def upstream_payload():
    raw = UPSTREAM.read_bytes()
    require(sha256(raw).hexdigest() == EXPECTED_UPSTREAM_SHA256,
            "upstream dangerous-chart result file changed")
    return json.loads(raw)


def frozen_d3_certificate(chart):
    payload = upstream_payload()["charts"][str(chart)][
        "filtered_degree_three_exact"
    ]["exact_certificate"]
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode("ascii")).hexdigest()
    require(digest == EXPECTED_D3_CERTIFICATE_SHA256[chart],
            f"chart {chart} frozen d3 certificate changed")
    certificate = []
    for item in payload:
        column = (
            tuple(map(int, item["word"])),
            bytes(sorted(CELL_NAME_ID[name] for name in item["multiplier"])),
        )
        coefficient = int(item["coefficient"])
        require(str(coefficient) == item["coefficient"],
                "nonintegral d3 certificate coefficient")
        certificate.append((coefficient, column))
    return tuple(certificate), digest


def exact_counter(counter):
    return Counter({row: value for row, value in counter.items() if value})


def replay_d3(chart):
    anchors = anchor_ids(chart)
    targets = target_by_degree(chart)
    certificate, digest = frozen_d3_certificate(chart)
    replay = Counter()
    for coefficient, column in certificate:
        for row in column_rows(column):
            degree = row_degree(row, anchors)
            if degree in (0, 2, 3):
                replay[row] += coefficient
    expected = Counter()
    for degree in (0, 2, 3):
        expected.update(targets[degree])
    replay = exact_counter(replay)
    require(replay == expected,
            f"chart {chart} frozen d3 certificate failed raw replay")
    mutation = Counter(replay)
    coefficient, column = certificate[0]
    for row in column_rows(column):
        if row_degree(row, anchors) in (0, 2, 3):
            mutation[row] -= 2 * coefficient
    require(exact_counter(mutation) != expected,
            "degree-three sign mutation did not fire")
    return certificate, digest, targets


def singleton_degree4_pivot(row, anchors):
    """Find a min-degree-four source column with this sole d=4 output."""
    require(row_degree(row, anchors) == 4, "singleton pivot row is not d4")
    anchor_tuple = tuple(sorted(anchors))
    for column in incident_columns(row):
        word, multiplier = column
        multiplier_degree = row_degree(multiplier, anchors)
        histogram = word_degree_histogram(word, anchor_tuple)
        minimum_word_degree, leading_count = histogram[0]
        if multiplier_degree + minimum_word_degree != 4:
            continue
        if leading_count != 1:
            continue
        leading = tuple(output for output in column_rows(column)
                        if row_degree(output, anchors) == 4)
        require(leading == (row,),
                "histogram singleton and literal leading row disagree")
        return column
    return None


def encode_column(column):
    word, multiplier = column
    return {
        "word": "".join(map(str, word)),
        "multiplier": [
            f"x{u}{v}_{a}{b}" for u, v, a, b in (CELLS[cell]
                                                   for cell in multiplier)
        ],
    }


def add_fraction(mapping, key, value):
    updated = mapping.get(key, Fraction(0)) + Fraction(value)
    if updated:
        mapping[key] = updated
    else:
        mapping.pop(key, None)


def add_scaled(target, source, scalar):
    scalar = Fraction(scalar)
    for key, value in source.items():
        add_fraction(target, key, scalar * value)


def exact_core_solution(generators, target, row_count):
    """Select a mod-p full-rank minor, then solve it exactly over Q."""
    prime = 1009
    modular_basis = {}
    selected = []
    for generator_number, source in enumerate(generators):
        vector = {index: value % prime for index, value in source.items()
                  if value % prime}
        while vector:
            pivot = min(vector)
            coefficient = vector[pivot]
            if pivot not in modular_basis:
                inverse = pow(coefficient, -1, prime)
                modular_basis[pivot] = {
                    index: value * inverse % prime
                    for index, value in vector.items()
                }
                selected.append(generator_number)
                break
            for index, value in modular_basis[pivot].items():
                updated = (vector.get(index, 0) - coefficient * value) % prime
                if updated:
                    vector[index] = updated
                else:
                    vector.pop(index, None)
        if len(selected) == row_count:
            break
    require(len(selected) == row_count,
            "B plus literal degree-three kernel differences lost full core rank")

    basis = {}
    basis_combinations = {}
    for local_number, generator_number in enumerate(selected):
        vector = {
            index: Fraction(value)
            for index, value in generators[generator_number].items() if value
        }
        combination = {local_number: Fraction(1)}
        while vector:
            pivot = min(vector)
            coefficient = vector[pivot]
            if pivot not in basis:
                vector = {
                    index: value / coefficient
                    for index, value in vector.items()
                }
                combination = {
                    index: value / coefficient
                    for index, value in combination.items()
                }
                basis[pivot] = vector
                basis_combinations[pivot] = combination
                break
            add_scaled(vector, basis[pivot], -coefficient)
            add_scaled(combination, basis_combinations[pivot], -coefficient)
        else:
            raise RuntimeError("modularly independent core minor vanished over Q")

    residual = {
        index: Fraction(value) for index, value in target.items() if value
    }
    solution_on_selected = {}
    while residual:
        pivot = min(residual)
        coefficient = residual[pivot]
        require(pivot in basis, "exact core target escaped selected minor")
        add_scaled(residual, basis[pivot], -coefficient)
        add_scaled(solution_on_selected,
                   basis_combinations[pivot], coefficient)
    solution = {
        selected[local_number]: coefficient
        for local_number, coefficient in solution_on_selected.items()
    }
    replay = {}
    for generator_number, coefficient in solution.items():
        add_scaled(replay, generators[generator_number], coefficient)
    require(replay == {index: Fraction(value)
                       for index, value in target.items() if value},
            "exact core solution replay failed")
    return solution, tuple(selected)


def degree4_lift(chart):
    anchors = anchor_ids(chart)
    certificate3, digest3, targets = replay_d3(chart)
    lower_rows, lower_columns, lower_ledger = lower_component(chart, targets)
    require(len(lower_rows) == lower_ledger["degree2_rows"]
            + lower_ledger["degree3_rows"] + 1,
            "lower row ledger is inconsistent")

    image4 = Counter()
    for coefficient, column in certificate3:
        for row in column_rows(column):
            if row_degree(row, anchors) == 4:
                image4[row] += coefficient
    residual4 = Counter(targets[4])
    residual4.subtract(image4)
    residual4 = exact_counter(residual4)
    residual_histogram = Counter(residual4.values())
    direct_pivots = {}
    def direct_pivot(row):
        if row not in direct_pivots:
            direct_pivots[row] = singleton_degree4_pivot(row, anchors)
        return direct_pivots[row]

    # Quotient the top layer by every literal singleton min-d4 column.  Seed
    # the complementary core with both the target and all tails of every old
    # source column: this is what retains all lower-kernel freedom.
    core_rows = {
        row for row in targets[4] if direct_pivot(row) is None
    }
    old_tail_rows = set()
    for column in lower_columns:
        for row in column_rows(column):
            if row_degree(row, anchors) != 4:
                continue
            old_tail_rows.add(row)
            if direct_pivot(row) is None:
                core_rows.add(row)
    core_frontier = deque(sorted(core_rows))
    degree4_columns = set()
    while core_frontier:
        row = core_frontier.popleft()
        for column in incident_columns(row):
            if (column in degree4_columns
                    or column_minimum_degree(column, anchors) != 4):
                continue
            degree4_columns.add(column)
            for output in column_rows(column):
                if (row_degree(output, anchors) == 4
                        and direct_pivot(output) is None
                        and output not in core_rows):
                    core_rows.add(output)
                    core_frontier.append(output)
    ordered_core = tuple(sorted(core_rows))
    core_index = {row: index for index, row in enumerate(ordered_core)}

    def core_vector(column):
        return Counter(
            core_index[row] for row in column_rows(column)
            if row in core_index
        )

    # Each min-d3 column has one literal leading row.  Differences inside a
    # fixed-leading-row fibre are genuine source-labelled lower-kernel
    # directions.  Together with B (the min-d4 leading block) they suffice
    # on all four charts; this is checked by a full core-rank certificate.
    generators = []
    descriptions = []
    for column in sorted(degree4_columns, key=repr):
        vector = core_vector(column)
        if vector:
            generators.append(vector)
            descriptions.append(("B", column))
    degree3_fibres = defaultdict(list)
    for column in lower_columns:
        if column_minimum_degree(column, anchors) != 3:
            continue
        leading = tuple(row for row in column_rows(column)
                        if row_degree(row, anchors) == 3)
        require(len(leading) == 1,
                "minimum-degree-three column lost its singleton leading row")
        degree3_fibres[leading[0]].append(column)
    kernel_generator_count = 0
    for leading_row in sorted(degree3_fibres):
        columns = sorted(degree3_fibres[leading_row], key=repr)
        base = columns[0]
        base_vector = core_vector(base)
        for column in columns[1:]:
            vector = core_vector(column)
            vector.subtract(base_vector)
            vector = exact_counter(vector)
            if not vector:
                continue
            generators.append(vector)
            descriptions.append(("K3", column, base))
            kernel_generator_count += 1

    core_target = Counter(
        {core_index[row]: coefficient for row, coefficient in residual4.items()
         if row in core_index}
    )
    solution, selected_minor = exact_core_solution(
        generators, core_target, len(ordered_core)
    )
    source_adjustment = {}
    used_generator_types = Counter()
    for generator_number, coefficient in solution.items():
        description = descriptions[generator_number]
        used_generator_types[description[0]] += 1
        if description[0] == "B":
            add_fraction(source_adjustment, description[1], coefficient)
        else:
            add_fraction(source_adjustment, description[1], coefficient)
            add_fraction(source_adjustment, description[2], -coefficient)

    # The K3 part is a literal kernel, not a quotient inference.
    lower_adjustment_replay = Counter()
    for column, coefficient in source_adjustment.items():
        if column_minimum_degree(column, anchors) != 3:
            continue
        for row in column_rows(column):
            if row_degree(row, anchors) <= 3:
                lower_adjustment_replay[row] += coefficient
    require(not exact_counter(lower_adjustment_replay),
            "degree-three differences failed to cancel in the lower block")

    adjusted_image4 = Counter(image4)
    for column, coefficient in source_adjustment.items():
        for row in column_rows(column):
            if row_degree(row, anchors) == 4:
                adjusted_image4[row] += coefficient
    remaining4 = Counter(targets[4])
    remaining4.subtract(adjusted_image4)
    remaining4 = exact_counter(remaining4)
    require(all(direct_pivot(row) is not None for row in remaining4),
            "core solve left a non-singleton degree-four row")
    direct_repairs = {}
    for row, coefficient in remaining4.items():
        add_fraction(direct_repairs, direct_pivot(row), coefficient)

    certificate4_map = dict(source_adjustment)
    for column, coefficient in direct_repairs.items():
        add_fraction(certificate4_map, column, coefficient)
    certificate4 = tuple(sorted(
        ((coefficient, column)
         for column, coefficient in certificate4_map.items()),
        key=lambda item: repr(item[1]),
    ))

    full_replay = Counter()
    for coefficient, column in certificate3 + certificate4:
        for row in column_rows(column):
            if row_degree(row, anchors) <= 4:
                full_replay[row] += coefficient
    full_replay = exact_counter(full_replay)
    full_target = Counter()
    for degree in range(5):
        full_target.update(targets[degree])
    exact_lift = full_replay == full_target
    require(exact_lift, "complete degree-four lift failed full raw replay")
    mutated = Counter(full_replay)
    coefficient, column = certificate4[0]
    for row in column_rows(column):
        if row_degree(row, anchors) <= 4:
            mutated[row] -= 2 * coefficient
    require(exact_counter(mutated) != full_target,
            "degree-four sign mutation did not fire")

    certificate4_payload = [
        {"coefficient": str(coefficient), **encode_column(column)}
        for coefficient, column in certificate4
    ]
    certificate4_digest = sha256(json.dumps(
        certificate4_payload, sort_keys=True, separators=(",", ":")
    ).encode("ascii")).hexdigest()
    require(certificate4_digest == EXPECTED_D4_CERTIFICATE_SHA256[chart],
            f"chart {chart} degree-four certificate changed")
    return {
        "chart": chart,
        "numbering": "zero-based pure-matching orbit index",
        "anchors": [
            f"x{u}{v}_{a}{b}" for u, v, a, b in
            (CELLS[cell] for cell in sorted(anchors))
        ],
        "frozen_d3_certificate_terms": len(certificate3),
        "frozen_d3_certificate_sha256": digest3,
        "raw_d3_replay": True,
        "d3_sign_mutation_fired": True,
        "lower_component": lower_ledger,
        "lower_rows": len(lower_rows),
        "lower_columns": len(lower_columns),
        "degree4_target_rows": len(targets[4]),
        "degree4_d3_tail_rows": len(exact_counter(image4)),
        "degree4_residual_rows": len(residual4),
        "degree4_residual_coefficient_histogram": dict(sorted(
            residual_histogram.items()
        )),
        "degree4_old_tail_rows": len(old_tail_rows),
        "degree4_direct_pivot_cache_rows": len(direct_pivots),
        "degree4_core_rows": len(ordered_core),
        "degree4_core_columns_B": len(degree4_columns),
        "degree3_kernel_generators_available": kernel_generator_count,
        "core_generators": len(generators),
        "core_selected_minor": len(selected_minor),
        "core_solution_generator_terms": len(solution),
        "core_solution_generator_type_histogram": dict(sorted(
            used_generator_types.items()
        )),
        "source_adjustment_terms": len(source_adjustment),
        "source_adjustment_minimum_degree_histogram": dict(sorted(Counter(
            column_minimum_degree(column, anchors)
            for column in source_adjustment
        ).items())),
        "remaining_direct_rows": len(remaining4),
        "direct_repair_terms": len(direct_repairs),
        "degree4_certificate_terms": len(certificate4),
        "degree4_certificate_denominator_lcm": math.lcm(*(
            coefficient.denominator for coefficient, _column in certificate4
        )),
        "degree4_certificate_coefficient_histogram": dict(sorted(Counter(
            str(coefficient) for coefficient, _column in certificate4
        ).items())),
        "degree4_certificate_sha256": certificate4_digest,
        "exact_membership_I_mix_plus_K5": exact_lift,
        "degree4_sign_mutation_fired": True,
        "lower_kernel_freedoms": (
            "literal differences of min-d3 columns with the same sole d3 "
            "leading row are included before the full core-rank solve"
        ),
        "localization_status": (
            "finite I_mix+K^5 membership is preserved by anchor localization; "
            "this does not establish membership in the full localized ideal, "
            "saturation, or radical membership"
        ),
        "certificate4": certificate4_payload,
    }


def lift_mode(charts):
    results = {}
    for chart in charts:
        print("chart", chart, "raw d3 replay and d4 lift", flush=True)
        results[str(chart)] = degree4_lift(chart)
        item = results[str(chart)]
        print("chart", chart, "residual", item["degree4_residual_rows"],
              "core", item["degree4_core_rows"],
              "kernel/B adjustment", item["source_adjustment_terms"],
              "direct repairs", item["direct_repair_terms"],
              "exact", item["exact_membership_I_mix_plus_K5"], flush=True)
    digest_payload = {
        chart: {key: value for key, value in item.items()
                if key != "certificate4"}
        for chart, item in results.items()
    }
    digest = sha256(json.dumps(
        digest_payload, sort_keys=True, separators=(",", ":")
    ).encode("ascii")).hexdigest()
    require(digest == EXPECTED_D4_LEDGER_SHA256,
            "dangerous-chart degree-four ledger changed")
    payload = {
        "status": "UNAUDITED exact finite K-adic computation",
        "legacy_numbering_guard": (
            "legacy one-based chart25 is zero-based orbit24 (W40), not one "
            "of the present zero-based charts25--28"
        ),
        "charts": results,
        "ledger_sha256": digest,
    }
    output = HERE / "results_d4.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("ledger sha256", digest)


def target_stats(chart):
    anchors = anchor_ids(chart)
    targets = target_by_degree(chart)
    leading_histogram = Counter()
    incident_histogram = Counter()
    candidates = []
    for row, coefficient in targets[4].items():
        columns = tuple(
            column for column in incident_columns(row)
            if column_minimum_degree(column, anchors) <= 4
        )
        low_sizes = tuple(sorted(
            sum(truncated_column(column, anchors).values()) for column in columns
        ))
        leading_histogram[len(columns)] += 1
        incident_histogram.update(low_sizes)
        candidates.append({
            "row": row.hex(),
            "target_coefficient": coefficient,
            "incident_columns": len(columns),
            "truncated_output_sizes": list(low_sizes),
        })
    candidates.sort(key=lambda item: (
        item["incident_columns"], item["truncated_output_sizes"], item["row"]
    ))
    return {
        "chart": chart,
        "anchors": [CELLS[cell] for cell in sorted(anchors)],
        "target_support": {str(d): len(targets[d]) for d in range(5)},
        "target_coefficient_histograms": {
            str(d): dict(sorted(Counter(targets[d].values()).items()))
            for d in range(5)
        },
        "degree4_incident_column_histogram": dict(sorted(leading_histogram.items())),
        "degree4_truncated_output_size_histogram": dict(sorted(incident_histogram.items())),
        "lowest_incident_candidates": candidates[:100],
    }


def stats_mode(charts):
    result = {str(chart): target_stats(chart) for chart in charts}
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode("ascii")).hexdigest()
    payload = {"charts": result, "sha256": digest}
    output = HERE / "target_stats.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    for chart in charts:
        item = result[str(chart)]
        print("chart", chart, "target", item["target_support"],
              "d4 incidence", item["degree4_incident_column_histogram"])
        print(" lowest", [(x["incident_columns"], x["truncated_output_sizes"])
                           for x in item["lowest_incident_candidates"][:3]])
    print("sha256", digest)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("stats", "lift"))
    parser.add_argument("charts", nargs="*", type=int, default=sorted(CHARTS))
    args = parser.parse_args()
    require(all(chart in CHARTS for chart in args.charts), "unknown chart")
    if args.mode == "stats":
        stats_mode(args.charts)
    elif args.mode == "lift":
        lift_mode(args.charts)


if __name__ == "__main__":
    main()
