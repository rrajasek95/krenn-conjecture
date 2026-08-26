#!/usr/bin/env python3
"""No-solve structural audit of the 7,316-column full-Fh D12 r27 packet."""

import argparse
from collections import Counter, deque
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
from time import monotonic


HERE = Path(__file__).resolve().parent
DRIVER_PATH = HERE / "run_fh_degree12_incremental.py"
RESULT = HERE / "results_r27_pending_structure.json"
WALL_CAP_SECONDS = 300
DURABLE_PREFIX = 5_376
EXPECTED_LOGICAL_SHA256 = "ff43d5930325a6bd1f2afe39f4ef14b6fc0fdd2023ae801178579058ab355f81"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, f"cannot load {path}")
    spec.loader.exec_module(module)
    return module


def counter_record(counter):
    return [[str(key), value] for key, value in sorted(
        counter.items(), key=lambda item: str(item[0]))]


def graph_shape(module, multiplier):
    edges = Counter()
    degrees = [0] * 8
    adjacency = [set() for _ in range(8)]
    for value in multiplier:
        left, right, _a, _b = module.D5.COORDINATES[value]
        edges[left, right] += 1
        degrees[left] += 1
        degrees[right] += 1
        adjacency[left].add(right)
        adjacency[right].add(left)
    seen = set()
    components = []
    for vertex in range(8):
        if vertex in seen or not adjacency[vertex]:
            continue
        stack = [vertex]
        seen.add(vertex)
        size = 0
        while stack:
            current = stack.pop()
            size += 1
            for other in adjacency[current]:
                if other not in seen:
                    seen.add(other)
                    stack.append(other)
        components.append(size)
    return (
        len(multiplier),
        tuple(sorted(degrees, reverse=True)),
        tuple(sorted(components, reverse=True)),
        tuple(sorted(edges.values(), reverse=True)),
    )


def word_record(module, code):
    word = module.D5.decode_word(code)
    profile = tuple(sorted(Counter(word).values(), reverse=True))
    support_edges = []
    used = set()
    for value in module.D5.SUPPORT_IDS:
        left, right, left_colour, right_colour = module.D5.COORDINATES[value]
        if word[left] == left_colour and word[right] == right_colour:
            require(left not in used and right not in used,
                    "support-compatible edges stopped being a matching")
            used.update((left, right))
            support_edges.append((left, right, left_colour))
    minimum = min(map(len, module.normalized_generator(code)))
    require(minimum == 4 - len(support_edges),
            "support matching/minimum-degree theorem changed")
    return word, profile, tuple(sorted(support_edges)), minimum


def exchange_type(first, second):
    if first == second:
        return "same-physical-matching/decoration"
    common = set(first) & set(second)
    remaining = (set(first) | set(second)) - common
    adjacency = {}
    for left, right in remaining:
        adjacency.setdefault(left, set()).add(right)
        adjacency.setdefault(right, set()).add(left)
    components = []
    seen = set()
    for vertex in adjacency:
        if vertex in seen:
            continue
        stack = [vertex]
        seen.add(vertex)
        size = 0
        while stack:
            current = stack.pop()
            size += 1
            for other in adjacency[current]:
                if other not in seen:
                    seen.add(other)
                    stack.append(other)
        components.append(size)
    require(all(size in (4, 6, 8) for size in components),
            "two perfect matchings lost even-cycle exchange form")
    return "+".join(f"C{size}" for size in sorted(components))


def audit(mutate=False):
    started = monotonic()
    driver = load(DRIVER_PATH, "r27_structure_driver")
    source_api, module = driver.ROOT_STAR.load_source()
    checkpoint = json.loads(driver.CHECKPOINT.read_text())
    pending = sorted(driver.parse_column(record)
                     for record in checkpoint["pending_columns"])
    require(len(pending) == 7_316 and checkpoint["completed_rounds"] == 27,
            "r27 pending checkpoint changed")
    old_rows = set(driver.load_rows())
    require(len(old_rows) == 1_473_022, "r26 row interface changed")

    row_ids = {}
    row_values = []
    row_counts = []
    row_xors = []
    column_rows = []
    vector_order = []
    word_profiles = Counter()
    fibres = Counter()
    multiplier_degrees = Counter()
    multiplier_shapes = Counter()
    stabilizer_sizes = Counter()
    column_records = []

    for column_id, column in enumerate(pending):
        code, multiplier = column
        entries = source_api.invariant_entries(module, column)
        require(entries, "pending column vanished")
        minimum_row = min(entries, key=lambda row: (-len(row), row))
        vector_order.append(((-len(minimum_row), minimum_row),
                             len(entries), column, column_id))
        word, profile, support_edges, minimum = word_record(module, code)
        fibre = f"PM{2 * minimum}"
        shape = graph_shape(module, multiplier)
        orbit_size = len(module.normalized_column_orbit(column))
        word_profiles[profile] += 1
        fibres[fibre] += 1
        multiplier_degrees[len(multiplier)] += 1
        multiplier_shapes[shape] += 1
        stabilizer_sizes[orbit_size] += 1
        row_list = []
        for row in entries:
            if row in old_rows:
                continue
            row_id = row_ids.get(row)
            if row_id is None:
                row_id = len(row_values)
                row_ids[row] = row_id
                row_values.append(row)
                row_counts.append(0)
                row_xors.append(0)
            row_counts[row_id] += 1
            row_xors[row_id] ^= column_id
            row_list.append(row_id)
        column_rows.append(row_list)
        column_records.append({
            "id": column_id, "code": code,
            "word": "".join(map(str, word)),
            "word_profile": list(profile),
            "support_matching": [list(edge) for edge in support_edges],
            "leading_fibre": fibre,
            "multiplier_hex": multiplier.hex(),
            "multiplier_shape": [shape[0], list(shape[1]), list(shape[2]),
                                   list(shape[3])],
            "stabilizer_orbit_size": orbit_size,
        })
        if (column_id + 1) % 1024 == 0:
            print("INCIDENCE", column_id + 1, "/", len(pending),
                  "new_rows", len(row_values), flush=True)
        require(monotonic() - started < WALL_CAP_SECONDS,
                "r27 structural census exceeded 300 seconds")

    require(len(row_values) == 1_997_290 - 1_473_022,
            "new-row census changed")
    vector_order.sort()
    durable_ids = {record[-1] for record in vector_order[:DURABLE_PREFIX]}
    for record in column_records:
        record["durable_prefix"] = record["id"] in durable_ids

    initial_counts = tuple(row_counts)
    initial_private_rows = sum(count == 1 for count in initial_counts)
    initial_private_columns = len({row_xors[index]
                                   for index, count in enumerate(initial_counts)
                                   if count == 1})
    private_degree = Counter()
    private_coefficient = Counter()
    private_provider_count = Counter()
    private_witnesses = []
    for column_id, column in enumerate(pending):
        entries = source_api.invariant_entries(module, column)
        candidates = [row for row in entries
                      if row in row_ids and initial_counts[row_ids[row]] == 1]
        require(candidates, "column lost its literal private row")
        private_row = min(candidates, key=lambda row: (-len(row), row))
        providers = []
        provider_sum = 0
        for actual_code, actual_multiplier in module.normalized_column_orbit(column):
            for term, coefficient in module.normalized_generator(actual_code).items():
                row = bytes(sorted(actual_multiplier + term))
                if row != private_row or row != module.canonical_normalized_row(row):
                    continue
                raw_terms = []
                for raw_term in module.D5.iter_word_terms(actual_code):
                    normalized = bytes(value for value in raw_term
                                       if value not in module.D5.SUPPORT_IDS)
                    if normalized == term:
                        raw_terms.append(raw_term.hex())
                require(len(raw_terms) == coefficient,
                        "normalized source matching multiplicity changed")
                providers.append({
                    "word_code": actual_code,
                    "word": "".join(map(str, module.D5.decode_word(actual_code))),
                    "multiplier_hex": actual_multiplier.hex(),
                    "normalized_matching_term_hex": term.hex(),
                    "coefficient": coefficient,
                    "literal_source_matching_terms_hex": raw_terms,
                })
                provider_sum += coefficient
        require(provider_sum == entries[private_row] and providers,
                "private-row source provenance did not replay")
        private_degree[len(private_row) - len(column[1])] += 1
        private_coefficient[entries[private_row]] += 1
        private_provider_count[len(providers)] += 1
        private_witnesses.append({
            "column_id": column_id,
            "word_code": column[0],
            "multiplier_hex": column[1].hex(),
            "private_row_hex": private_row.hex(),
            "private_coefficient": entries[private_row],
            "durable_prefix": column_id in durable_ids,
            "providers": providers,
        })
    queue = deque(index for index, count in enumerate(row_counts) if count == 1)
    active = [True] * len(pending)
    peel_order = []
    peel_wave = [None] * len(pending)
    wave = 0
    while queue:
        next_queue = deque()
        while queue:
            row_id = queue.popleft()
            if row_counts[row_id] != 1:
                continue
            owner = row_xors[row_id]
            if not active[owner]:
                continue
            active[owner] = False
            peel_wave[owner] = wave
            peel_order.append(owner)
            for incident_row in column_rows[owner]:
                if row_counts[incident_row] == 0:
                    continue
                row_counts[incident_row] -= 1
                row_xors[incident_row] ^= owner
                if row_counts[incident_row] == 1:
                    next_queue.append(incident_row)
        queue = next_queue
        wave += 1
    residual_ids = [index for index, value in enumerate(active) if value]

    # Top-y collision exchange types, restricted to the residual core when one
    # exists and otherwise to all degree-two ownership rows as a control.
    collision_rows = {row_values[index] for index, count in enumerate(row_counts)
                      if count >= 2}
    top_providers = {}
    if collision_rows:
        residual_set = set(residual_ids)
        for column_id in residual_ids:
            column = pending[column_id]
            for actual in module.normalized_column_orbit(column):
                code, multiplier = actual
                for term, coefficient in module.normalized_generator(code).items():
                    if len(term) != 4 or not coefficient:
                        continue
                    row = bytes(sorted(multiplier + term))
                    if row not in collision_rows or row != module.canonical_normalized_row(row):
                        continue
                    edges = tuple(sorted((module.D5.COORDINATES[value][0],
                                          module.D5.COORDINATES[value][1])
                                         for value in term))
                    require(len({vertex for edge in edges for vertex in edge}) == 8,
                            "top generator term is not a physical perfect matching")
                    top_providers.setdefault(row, set()).add((column_id, edges))
        exchange_histogram = Counter()
        for providers in top_providers.values():
            providers = sorted(providers)
            for first_index in range(len(providers)):
                for second_index in range(first_index + 1, len(providers)):
                    first_column, first_edges = providers[first_index]
                    second_column, second_edges = providers[second_index]
                    if first_column != second_column:
                        exchange_histogram[exchange_type(first_edges, second_edges)] += 1
    else:
        exchange_histogram = Counter()

    durable_profiles = Counter(tuple(column_records[index]["word_profile"])
                               for index in durable_ids)
    durable_fibres = Counter(column_records[index]["leading_fibre"]
                             for index in durable_ids)
    durable_orbits = Counter(column_records[index]["stabilizer_orbit_size"]
                             for index in durable_ids)
    peel_waves = Counter(value for value in peel_wave if value is not None)
    residual_profiles = Counter(tuple(column_records[index]["word_profile"])
                                for index in residual_ids)
    residual_fibres = Counter(column_records[index]["leading_fibre"]
                              for index in residual_ids)

    result = {
        "format": "n8-fh-d12-r27-pending-structure-v1",
        "status": "PASS",
        "scope": (
            "exact literal incidence of the 7,316 r27 canonical column orbits "
            "against rows new beyond accepted r26; no rank solve or target verdict"
        ),
        "counts": {
            "pending_columns": len(pending),
            "durable_vector_prefix": len(durable_ids),
            "old_rows": len(old_rows),
            "new_rows": len(row_values),
            "initial_private_rows": initial_private_rows,
            "initial_private_columns": initial_private_columns,
            "leaf_peeled_columns": len(peel_order),
            "residual_columns": len(residual_ids),
            "peel_waves": counter_record(peel_waves),
        },
        "all_columns": {
            "word_profiles": counter_record(word_profiles),
            "leading_matching_fibres": counter_record(fibres),
            "multiplier_degrees": counter_record(multiplier_degrees),
            "multiplier_shapes": counter_record(multiplier_shapes),
            "stabilizer_orbit_sizes": counter_record(stabilizer_sizes),
        },
        "durable_prefix": {
            "word_profiles": counter_record(durable_profiles),
            "leading_matching_fibres": counter_record(durable_fibres),
            "stabilizer_orbit_sizes": counter_record(durable_orbits),
        },
        "private_row_certificate": {
            "normalized_matching_term_degrees": counter_record(private_degree),
            "private_coefficients": counter_record(private_coefficient),
            "provider_counts": counter_record(private_provider_count),
            "witnesses": private_witnesses,
        },
        "residual_core": {
            "column_ids": residual_ids,
            "columns": [column_records[index] for index in residual_ids],
            "word_profiles": counter_record(residual_profiles),
            "leading_matching_fibres": counter_record(residual_fibres),
            "top_exchange_types": counter_record(exchange_histogram),
        },
        "theorem": (
            "Every r27 column has an exact new-row triangular pivot over Z."
            if not residual_ids else
            "The raw new-row leaf order stops on the exported collision core; "
            "modular independence is not explained by private rows alone."
        ),
    }
    first_private_coefficient = private_witnesses[0]["private_coefficient"]
    if mutate:
        result["private_row_certificate"]["witnesses"][0]["private_coefficient"] += 1
    require(result["private_row_certificate"]["witnesses"][0]
            ["private_coefficient"] == first_private_coefficient,
            "hostile private-coefficient mutation survived")
    logical_payload = dict(result)
    encoded = json.dumps(logical_payload, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    if EXPECTED_LOGICAL_SHA256 is not None:
        require(result["logical_sha256"] == EXPECTED_LOGICAL_SHA256,
                "r27 structural result changed")
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("R27_STRUCTURE", json.dumps(result["counts"], sort_keys=True))
    print("THEOREM", result["theorem"])
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutate", action="store_true")
    audit(parser.parse_args().mutate)
