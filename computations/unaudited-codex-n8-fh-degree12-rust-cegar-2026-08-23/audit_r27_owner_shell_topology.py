#!/usr/bin/env python3
"""Exact topology/rank audit of the frozen r27 selected-owner shell."""

from collections import Counter, deque
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
from time import monotonic


HERE = Path(__file__).resolve().parent
DRIVER_PATH = HERE / "run_fh_degree12_incremental.py"
SHELL = HERE / "r27_selected_top_owner_core.txt"
CORE = HERE / "r27_selected_owner_2core.txt"
RESULT = HERE / "results_r27_owner_shell_topology.json"
EXPECTED_LOGICAL_SHA256 = "e92e1fd60a4ee4f61ec0cb89b85bdce354b59ff010d66f21605983270459c9af"
WALL_CAP_SECONDS = 300
PRIMES = (1009, 1013)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, f"cannot load {path}")
    spec.loader.exec_module(module)
    return module


def parse_column(text):
    code, multiplier = text.split(":")
    return int(code), bytes.fromhex(multiplier)


def column_text(column):
    return f"{column[0]}:{column[1].hex()}"


def exchange_type(first, second):
    if first == second:
        return "same-physical-matching/decoration"
    common = set(first) & set(second)
    remaining = (set(first) | set(second)) - common
    adjacency = {}
    for left, right in remaining:
        adjacency.setdefault(left, set()).add(right)
        adjacency.setdefault(right, set()).add(left)
    seen = set()
    components = []
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
            "perfect-matching exchange stopped being even-cycle")
    return "+".join(f"C{size}" for size in sorted(components))


def providers(module, row, column):
    answer = []
    for actual_code, actual_multiplier in module.normalized_column_orbit(column):
        term = module.quotient(row, actual_multiplier)
        if term is None or len(term) != 4:
            continue
        coefficient = module.normalized_generator(actual_code).get(term, 0)
        if not coefficient:
            continue
        edges = tuple(sorted((module.D5.COORDINATES[value][0],
                              module.D5.COORDINATES[value][1])
                             for value in term))
        require(len({vertex for edge in edges for vertex in edge}) == 8,
                "top provider is not a physical perfect matching")
        answer.append((actual_code, actual_multiplier, term, coefficient, edges))
    return answer


def component_census(row_adjacency, column_adjacency):
    seen_rows = set()
    seen_columns = set()
    records = []
    for seed in range(len(row_adjacency)):
        if seed in seen_rows:
            continue
        rows = {seed}
        columns = set()
        queue = deque(((0, seed),))
        seen_rows.add(seed)
        edges = 0
        while queue:
            side, index = queue.popleft()
            if side == 0:
                edges += len(row_adjacency[index])
                for other in row_adjacency[index]:
                    if other not in seen_columns:
                        seen_columns.add(other)
                        columns.add(other)
                        queue.append((1, other))
            else:
                for other in column_adjacency[index]:
                    if other not in seen_rows:
                        seen_rows.add(other)
                        rows.add(other)
                        queue.append((0, other))
        records.append((len(rows), len(columns), edges))
    require(len(seen_columns) == len(column_adjacency),
            "shell contains a column with no row")
    return records


def two_core(row_adjacency, column_adjacency):
    row_degree = list(map(len, row_adjacency))
    column_degree = list(map(len, column_adjacency))
    active_rows = [True] * len(row_degree)
    active_columns = [True] * len(column_degree)
    row_queue = deque(i for i, degree in enumerate(row_degree) if degree < 2)
    column_queue = deque(i for i, degree in enumerate(column_degree) if degree < 2)
    while row_queue or column_queue:
        while row_queue:
            row = row_queue.popleft()
            if not active_rows[row] or row_degree[row] >= 2:
                continue
            active_rows[row] = False
            for column in row_adjacency[row]:
                if active_columns[column]:
                    column_degree[column] -= 1
                    if column_degree[column] < 2:
                        column_queue.append(column)
        while column_queue:
            column = column_queue.popleft()
            if not active_columns[column] or column_degree[column] >= 2:
                continue
            active_columns[column] = False
            for row in column_adjacency[column]:
                if active_rows[row]:
                    row_degree[row] -= 1
                    if row_degree[row] < 2:
                        row_queue.append(row)
    return active_rows, active_columns


def modular_rank(column_vectors, row_count, prime):
    pivots = {}
    for source in column_vectors:
        vector = {row: value % prime for row, value in source.items()
                  if value % prime}
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in pivots:
                inverse = pow(value, prime - 2, prime)
                pivots[pivot] = {row: coefficient * inverse % prime
                                 for row, coefficient in vector.items()}
                break
            basis = pivots[pivot]
            for row, coefficient in basis.items():
                result = (vector.get(row, 0) - value * coefficient) % prime
                if result:
                    vector[row] = result
                else:
                    vector.pop(row, None)
    require(len(pivots) <= row_count, "rank exceeds row count")
    return len(pivots)


def exact_rank_via_degree_two(column_vectors, row_count):
    """Collapse x_u+x_v=0 edges, then rank the tiny residual over Q."""
    adjacency = [[] for _ in range(row_count)]
    for vector in column_vectors:
        if len(vector) == 2:
            (first, first_value), (second, second_value) = sorted(vector.items())
            require(first_value == second_value == 1,
                    "degree-two core column changed coefficient")
            adjacency[first].append(second)
            adjacency[second].append(first)
    colour = {}
    parameter = {}
    free_parameters = 0
    odd_components = 0
    degree_two_components = 0
    for seed in range(row_count):
        if seed in colour:
            continue
        degree_two_components += 1
        colour[seed] = 1
        queue = deque((seed,))
        vertices = []
        odd = False
        while queue:
            vertex = queue.popleft()
            vertices.append(vertex)
            for other in adjacency[vertex]:
                if other not in colour:
                    colour[other] = -colour[vertex]
                    queue.append(other)
                elif colour[other] != -colour[vertex]:
                    odd = True
        if odd:
            odd_components += 1
        else:
            for vertex in vertices:
                parameter[vertex] = free_parameters
            free_parameters += 1

    equations = []
    for vector in column_vectors:
        if len(vector) <= 2:
            continue
        equation = {}
        for row, value in vector.items():
            if row not in parameter:
                continue
            index = parameter[row]
            coefficient = equation.get(index, 0) + value * colour[row]
            if coefficient:
                equation[index] = coefficient
            else:
                equation.pop(index, None)
        if equation:
            equations.append(equation)
    pivots = {}
    for source in equations:
        vector = {index: Fraction(value) for index, value in source.items()}
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in pivots:
                pivots[pivot] = {index: coefficient / value
                                 for index, coefficient in vector.items()}
                break
            basis = pivots[pivot]
            for index, coefficient in basis.items():
                result = vector.get(index, Fraction(0)) - value * coefficient
                if result:
                    vector[index] = result
                else:
                    vector.pop(index, None)
    collapsed_rank = len(pivots)
    left_nullity = free_parameters - collapsed_rank
    return {
        "degree_two_components": degree_two_components,
        "odd_degree_two_components_forcing_zero": odd_components,
        "free_sign_parameters_before_hyperedges": free_parameters,
        "nonzero_collapsed_hyperedge_equations": len(equations),
        "exact_collapsed_rank_over_Q": collapsed_rank,
        "exact_left_nullity": left_nullity,
        "exact_rank_over_Q": row_count - left_nullity,
    }


def counter_record(counter):
    return [[str(key), value] for key, value in sorted(
        counter.items(), key=lambda item: str(item[0]))]


def audit():
    started = monotonic()
    driver = load(DRIVER_PATH, "r27_shell_driver")
    source_api, module = driver.ROOT_STAR.load_source()
    checkpoint = json.loads(driver.CHECKPOINT.read_text())
    r27_columns = {driver.parse_column(record)
                   for record in checkpoint["pending_columns"]}
    require(len(r27_columns) == 7_316, "r27 column packet changed")

    row_hexes = []
    expected_columns = []
    owner_lists = []
    column_ids = {}
    columns = []
    row_adjacency = []
    column_adjacency = []
    for line in SHELL.read_text().splitlines():
        fields = line.split()
        row_hexes.append(fields[0])
        expected_columns.append(parse_column(fields[1]))
        owners = [parse_column(field) for field in fields[2:]]
        owner_lists.append(owners)
        adjacency = []
        for owner in owners:
            column = column_ids.get(owner)
            if column is None:
                column = len(columns)
                column_ids[owner] = column
                columns.append(owner)
                column_adjacency.append([])
            adjacency.append(column)
            column_adjacency[column].append(len(row_adjacency))
        row_adjacency.append(adjacency)
    require(len(row_adjacency) == 7_316 and len(columns) == 58_497
            and sum(map(len, row_adjacency)) == 67_635,
            "selected owner shell changed")

    row_degree_histogram = Counter(map(len, row_adjacency))
    column_degree_histogram = Counter(map(len, column_adjacency))
    components = component_census(row_adjacency, column_adjacency)
    component_shapes = Counter(components)
    active_rows, active_columns = two_core(row_adjacency, column_adjacency)
    core_rows = [index for index, value in enumerate(active_rows) if value]
    core_columns = [index for index, value in enumerate(active_columns) if value]
    core_row_map = {row: index for index, row in enumerate(core_rows)}
    core_column_set = set(core_columns)
    core_edges = sum(1 for row in core_rows for column in row_adjacency[row]
                     if column in core_column_set)
    require((len(core_rows), len(core_columns), core_edges)
            == (3_942, 7_180, 15_400), "owner-shell 2-core changed")

    coefficient_histogram = Counter()
    exchange_histogram = Counter()
    exchange_set_histogram = Counter()
    edge_coefficients = {}
    with CORE.open("w", encoding="ascii") as core_output:
        for row_index, (row_hex, expected, owners) in enumerate(
                zip(row_hexes, expected_columns, owner_lists)):
            row = bytes.fromhex(row_hex)
            expected_providers = providers(module, row, expected)
            require(len(expected_providers) == 1
                    and expected_providers[0][3] == 1,
                    "r27 selected private provider changed")
            expected_edges = expected_providers[0][4]
            for owner in owners:
                owner_providers = providers(module, row, owner)
                require(owner_providers, "owner-shell edge lost source provider")
                coefficient = sum(record[3] for record in owner_providers)
                coefficient_histogram[coefficient] += 1
                labels = tuple(sorted(set(exchange_type(expected_edges, record[4])
                                          for record in owner_providers)))
                if owner != expected:
                    exchange_set_histogram[labels] += 1
                    for record in owner_providers:
                        exchange_histogram[exchange_type(expected_edges,
                                                         record[4])] += 1
                column_index = column_ids[owner]
                edge_coefficients[row_index, column_index] = coefficient
                if active_rows[row_index] and active_columns[column_index]:
                    core_output.write(
                        f"{row_index} {column_index} {coefficient} "
                        f"{','.join(labels)} {row_hex} {column_text(owner)}\n"
                    )
            if (row_index + 1) % 1024 == 0:
                print("PROVIDERS", row_index + 1, "/", len(row_adjacency),
                      flush=True)
            require(monotonic() - started < WALL_CAP_SECONDS,
                    "owner-shell provider audit exceeded 300 seconds")

    core_vectors = []
    for column in core_columns:
        vector = {}
        for row in column_adjacency[column]:
            if active_rows[row]:
                vector[core_row_map[row]] = edge_coefficients[row, column]
        core_vectors.append(vector)
    core_ranks = {str(prime): modular_rank(core_vectors, len(core_rows), prime)
                  for prime in PRIMES}
    exact_core = exact_rank_via_degree_two(core_vectors, len(core_rows))
    require(all(rank == exact_core["exact_rank_over_Q"]
                for rank in core_ranks.values()),
            "modular core ranks differ from exact collapsed rank")

    # Exact one-shell escape census: inspect outputs of the 51,181 external
    # owner columns, but do not promote any escaping row or next column.
    round_rows = set(driver.load_rows_from(driver.ROUND_ROWS))
    external_columns = [column for column in columns if column not in r27_columns]
    require(len(external_columns) == 51_181, "external owner census changed")
    escape_histogram = Counter()
    escaping_columns = 0
    total_escape_incidences = 0
    escape_examples = []
    for index, column in enumerate(external_columns, 1):
        entries = source_api.invariant_entries(module, column)
        escaping = [row for row in entries if row not in round_rows]
        escape_histogram[len(escaping)] += 1
        if escaping:
            escaping_columns += 1
            total_escape_incidences += len(escaping)
            if len(escape_examples) < 64:
                escape_examples.append(
                    [column[0], column[1].hex(), escaping[0].hex(), len(escaping)])
        if index % 4096 == 0:
            print("ESCAPE", index, "/", len(external_columns), flush=True)
        require(monotonic() - started < WALL_CAP_SECONDS,
                "owner-shell escape audit exceeded 300 seconds")

    result = {
        "format": "n8-fh-d12-r27-owner-shell-topology-v1",
        "status": "PASS_FINITE_COLLISION_CORE_WITH_EXTERNAL_ESCAPE",
        "scope": (
            "exact combinatorics and source coefficients on the frozen "
            "7,316-row selected-owner shell only; external outputs are counted "
            "but not promoted; no next-shell closure or target solve"
        ),
        "shell": {
            "rows": len(row_adjacency), "columns": len(columns),
            "incidence_edges": sum(map(len, row_adjacency)),
            "r27_columns": len(r27_columns),
            "external_columns": len(external_columns),
            "row_degree_histogram": counter_record(row_degree_histogram),
            "column_degree_histogram": counter_record(column_degree_histogram),
            "connected_components": len(components),
            "component_shapes": counter_record(component_shapes),
            "cyclomatic_number": (sum(map(len, row_adjacency))
                                    - len(row_adjacency) - len(columns)
                                    + len(components)),
        },
        "two_core": {
            "rows": len(core_rows), "columns": len(core_columns),
            "edges": core_edges,
            "modular_ranks": core_ranks,
            "exact_rank_decomposition": exact_core,
            "exact_full_row_rank_over_Q": (
                exact_core["exact_rank_over_Q"] == len(core_rows)),
            "file": CORE.name,
            "sha256": sha256(CORE.read_bytes()).hexdigest(),
        },
        "source_labels": {
            "coefficient_histogram": counter_record(coefficient_histogram),
            "exchange_provider_histogram": counter_record(exchange_histogram),
            "exchange_label_set_histogram": counter_record(exchange_set_histogram),
        },
        "external_escape": {
            "columns_with_rows_beyond_r27_interface": escaping_columns,
            "columns_without_rows_beyond_r27_interface": (
                len(external_columns) - escaping_columns),
            "escape_count_per_column": counter_record(escape_histogram),
            "total_escape_incidences": total_escape_incidences,
            "first_examples": escape_examples,
        },
        "theorem": (
            "The selected collision shell is not a finite closed cellular "
            "boundary: after leaf peeling it retains the exported 3,942-by-"
            "7,180 cyclic 2-core.  Degree-two sign propagation followed by "
            "exact rational reduction of the collapsed hyperedges gives rank "
            "3,178 and a 764-dimensional left obstruction.  Every external "
            "owner escapes to rows outside the frozen r27 interface, so the "
            "one-shell cellular boundary does not close."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    if EXPECTED_LOGICAL_SHA256 is not None:
        require(result["logical_sha256"] == EXPECTED_LOGICAL_SHA256,
                "owner-shell topology result changed")
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("OWNER_SHELL", result["shell"])
    print("CORE", result["two_core"])
    print("ESCAPE", escaping_columns, "/", len(external_columns))
    print("logical", result["logical_sha256"])
    return result


if __name__ == "__main__":
    audit()
