#!/usr/bin/env python3
"""Peel the exact closed target-rooted K0--K9 component modulo two primes."""

from __future__ import annotations

import hashlib
import json
from collections import deque
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET = HERE / "k9_k12_tail_rows.tsv"
COLUMNS = HERE / "k9_incidence_closure_layer4_columns.tsv"
EDGES = HERE / "k5_k9_column_output_closure_layer4_edges.tsv"
CLOSURE = HERE / "results_joint_incidence_full_layer5.json"
OUT = HERE / "results_k0_k9_closed_component_modular_peel.json"
PINS = {
    TARGET: "4e214b40aede42b09c4c3dfc05c2969541f1a9dd6271f7eb53b36303478ba3ae",
    COLUMNS: "22e789dad1d71dbc7d6b40dab839b39042f3819bbfb782fb8b88d7cdae6d8ae5",
    EDGES: "97e6b061456e03a4c3db6ff68175fb8bfa6f0af904a72577cbfeefc68df0a344",
    CLOSURE: "a99af72f3ac5f3c08aea933ce85dab5271c6761d1ae0ff1cec6297d5297f48c4",
}
EXPECTED_ROWS = {0: 1, 2: 3, 3: 6, 4: 60, 5: 249, 6: 2291, 7: 17068, 8: 132967, 9: 859611}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def load():
    for path, digest in PINS.items():
        require(sha256(path) == digest, f"pin changed: {path}")
    closure = json.loads(CLOSURE.read_text())
    require(closure["sample_unique_new_columns"] == 0, "component is not closed")
    require(closure["existing_columns"] == 837883, "closure column census changed")
    require({int(k): v for k, v in closure["joint_rows_by_degree"].items()} == EXPECTED_ROWS, "closure row census changed")

    target = {}
    with TARGET.open() as handle:
        require(handle.readline().rstrip("\n") == "degree\trow\tcoefficient", "target header changed")
        for line in handle:
            degree, row, coefficient = line.rstrip("\n").split("\t")
            if degree == "9":
                target[(9, bytes.fromhex(row))] = int(coefficient)
    require(len(target) == 49988, "K9 target census changed")

    with COLUMNS.open() as handle:
        require(handle.readline().rstrip("\n") == "column_index\tminimum_degree\tword\tmultiplier", "column header changed")
        column_count = 0
        minimum_hist = {}
        for line in handle:
            index, minimum, word, multiplier = line.rstrip("\n").split("\t")
            require(int(index) == column_count and len(word) == 8 and len(multiplier) == 16, "bad column ledger")
            minimum = int(minimum)
            require(0 <= minimum <= 9, "bad column minimum")
            minimum_hist[minimum] = minimum_hist.get(minimum, 0) + 1
            column_count += 1
    require(column_count == 837883, "column census changed")

    row_index = {}
    row_degrees = []
    row_adj = []
    column_adj = [[] for _ in range(column_count)]
    edge_count = 0
    with EDGES.open() as handle:
        require(handle.readline().rstrip("\n") == "column_index\tdegree\trow\tmultiplicity", "edge header changed")
        previous_column = -1
        for line in handle:
            column, degree, row, value = line.rstrip("\n").split("\t")
            column, degree, value = int(column), int(degree), int(value)
            require(previous_column <= column < column_count and 0 <= degree <= 9 and value > 0, "bad incidence record")
            previous_column = column
            key = (degree, bytes.fromhex(row))
            if key not in row_index:
                row_index[key] = len(row_index)
                row_adj.append([])
                row_degrees.append(degree)
            row_number = row_index[key]
            row_adj[row_number].append((column, value))
            column_adj[column].append((row_number, value))
            edge_count += 1
    require(edge_count == 8342855, "edge census changed")
    require(all(column_adj), "zero-output column in closed component")

    target_by_row = [0] * len(row_index)
    for key, coefficient in target.items():
        require(key in row_index, "target escaped closed component")
        target_by_row[row_index[key]] = coefficient
    degree_counts = {}
    for degree, _ in row_index:
        degree_counts[degree] = degree_counts.get(degree, 0) + 1
    require(degree_counts == EXPECTED_ROWS, "loaded row degree census changed")
    return target_by_row, row_adj, column_adj, degree_counts, minimum_hist, row_degrees


def component_census(target, row_adj, column_adj, row_degrees):
    seen_rows = bytearray(len(row_adj))
    seen_columns = bytearray(len(column_adj))
    components = []
    for seed, coefficient in enumerate(target):
        if coefficient == 0 or seen_rows[seed]:
            continue
        queue = deque([seed])
        seen_rows[seed] = 1
        row_count = column_count = edge_count = target_support = 0
        degree_hist = {}
        while queue:
            node = queue.popleft()
            if node >= 0:
                row_count += 1
                degree = row_degrees[node]
                degree_hist[degree] = degree_hist.get(degree, 0) + 1
                edge_count += len(row_adj[node])
                if target[node]:
                    target_support += 1
                for column, _ in row_adj[node]:
                    if not seen_columns[column]:
                        seen_columns[column] = 1
                        queue.append(-1 - column)
            else:
                column = -1 - node
                column_count += 1
                for row, _ in column_adj[column]:
                    if not seen_rows[row]:
                        seen_rows[row] = 1
                        queue.append(row)
        components.append({
            "rows": row_count,
            "columns": column_count,
            "weighted_edges": edge_count,
            "target_support": target_support,
            "rows_by_degree": degree_hist,
        })
    require(sum(seen_rows) == len(row_adj) and sum(seen_columns) == len(column_adj), "closed matrix has a component without target support")
    components.sort(key=lambda item: (item["columns"], item["rows"], item["weighted_edges"]), reverse=True)
    return components


def column_singleton_peel(target, row_adj, column_adj):
    """Quotient by columns with one currently unpivoted row."""
    support = [len(entries) for entries in column_adj]
    pivoted_row = bytearray(len(row_adj))
    queue = deque(column for column, value in enumerate(support) if value == 1)
    pivot_rows = 0
    pivot_columns = 0
    target_pivot_rows = 0
    while queue:
        column = queue.popleft()
        if support[column] != 1:
            continue
        live = [row for row, _ in column_adj[column] if not pivoted_row[row]]
        require(len(live) == 1, "column support bookkeeping mismatch")
        row = live[0]
        pivoted_row[row] = 1
        pivot_rows += 1
        pivot_columns += 1
        if target[row]:
            target_pivot_rows += 1
        for affected, _ in row_adj[row]:
            require(support[affected] > 0, "pivot row touches empty active column")
            support[affected] -= 1
            if support[affected] == 1:
                queue.append(affected)
    active_columns = bytearray(value > 0 for value in support)
    core_rows = bytearray(len(row_adj))
    core_edges = 0
    for column, active in enumerate(active_columns):
        if not active:
            continue
        for row, _ in column_adj[column]:
            if not pivoted_row[row]:
                core_rows[row] = 1
                core_edges += 1
    require(sum(core_rows) + pivot_rows == len(row_adj), "peel left isolated nonpivot rows")
    return {
        "pivot_rows": pivot_rows,
        "pivot_columns": pivot_columns,
        "target_pivot_rows": target_pivot_rows,
        "core_rows": sum(core_rows),
        "core_columns": sum(active_columns),
        "core_weighted_edges": core_edges,
        "core_target_support": sum(bool(target[row]) and bool(core_rows[row]) for row in range(len(row_adj))),
        "initial_singleton_columns": sum(len(entries) == 1 for entries in column_adj),
    }


def alternating_leaf_peel(prime: int, target, row_adj, column_adj):
    """Exact solvability-preserving row/column leaf elimination."""
    rhs = [value % prime for value in target]
    row_degree = [len(entries) for entries in row_adj]
    column_degree = [len(entries) for entries in column_adj]
    active_rows = bytearray(b"\x01") * len(row_adj)
    active_columns = bytearray(b"\x01") * len(column_adj)
    row_queue = deque()
    column_queue = deque(column for column, degree in enumerate(column_degree) if degree == 1)
    row_queue_seeded = False
    row_leaf_pivots = 0
    column_leaf_pivots = 0
    zero_columns_removed = 0
    contradictions = []

    def remove_pivot(row: int, column: int, value: int | None) -> None:
        nonlocal row_leaf_pivots, column_leaf_pivots, zero_columns_removed
        if value is None:
            column_leaf_pivots += 1
        else:
            row_leaf_pivots += 1
            for affected, entry in column_adj[column]:
                if affected != row and active_rows[affected]:
                    rhs[affected] = (rhs[affected] - entry * value) % prime
        active_rows[row] = 0
        active_columns[column] = 0
        for affected, _ in column_adj[column]:
            if affected != row and active_rows[affected]:
                row_degree[affected] -= 1
                if row_degree[affected] <= 1:
                    row_queue.append(affected)
        for affected, _ in row_adj[row]:
            if affected != column and active_columns[affected]:
                column_degree[affected] -= 1
                if column_degree[affected] == 0:
                    active_columns[affected] = 0
                    zero_columns_removed += 1
                elif column_degree[affected] == 1:
                    column_queue.append(affected)
        row_degree[row] = 0
        column_degree[column] = 0

    while row_queue or column_queue or not row_queue_seeded:
        while column_queue:
            column = column_queue.popleft()
            if not active_columns[column] or column_degree[column] != 1:
                continue
            live = [row for row, _ in column_adj[column] if active_rows[row]]
            require(len(live) == 1, "column leaf bookkeeping mismatch")
            remove_pivot(live[0], column, None)
        if not row_queue_seeded:
            row_queue.extend(row for row, degree in enumerate(row_degree) if active_rows[row] and degree <= 1)
            row_queue_seeded = True
        while row_queue:
            row = row_queue.popleft()
            if not active_rows[row]:
                continue
            if row_degree[row] == 0:
                if rhs[row] and len(contradictions) < 32:
                    contradictions.append((row, rhs[row]))
                active_rows[row] = 0
                continue
            if row_degree[row] != 1:
                continue
            live = [(column, entry) for column, entry in row_adj[row] if active_columns[column]]
            require(len(live) == 1, "row leaf bookkeeping mismatch")
            column, entry = live[0]
            value = rhs[row] * pow(entry, -1, prime) % prime
            remove_pivot(row, column, value)

    inconsistent = len(contradictions)
    core_rows = sum(active_rows)
    core_columns = sum(active_columns)
    core_edges = sum(
        1 for row, entries in enumerate(row_adj) if active_rows[row]
        for column, _ in entries if active_columns[column]
    )
    require(core_edges == sum(row_degree[row] for row in range(len(row_adj)) if active_rows[row]), "core row degree mismatch")
    require(core_edges == sum(column_degree[column] for column in range(len(column_adj)) if active_columns[column]), "core column degree mismatch")
    return {
        "prime": prime,
        "row_leaf_pivots": row_leaf_pivots,
        "column_leaf_pivots": column_leaf_pivots,
        "zero_columns_removed": zero_columns_removed,
        "isolated_nonzero_rhs_samples": contradictions,
        "core_rows": core_rows,
        "core_columns": core_columns,
        "core_weighted_edges": core_edges,
        "status": "PROVED_NO_SOLUTION_DURING_LEAF_ELIMINATION" if inconsistent else (
            "PASS_SOLVED_BY_ALTERNATING_LEAVES" if core_columns == 0 else "ALTERNATING_LEAF_CORE_REMAINS"
        ),
    }


def peel(prime: int, target, row_adj, column_adj):
    rhs = [value % prime for value in target]
    degree = [len(entries) for entries in row_adj]
    active = bytearray(b"\x01") * len(column_adj)
    solution = [0] * len(column_adj)
    queue = deque(index for index, value in enumerate(degree) if value <= 1)
    assigned = 0
    while queue:
        row = queue.popleft()
        if degree[row] != 1:
            continue
        live = [(column, value) for column, value in row_adj[row] if active[column]]
        require(len(live) == 1, "active degree bookkeeping mismatch")
        column, coefficient = live[0]
        value = rhs[row] * pow(coefficient, -1, prime) % prime
        solution[column] = value
        active[column] = 0
        assigned += 1
        for affected, entry in column_adj[column]:
            if degree[affected] == 0:
                continue
            rhs[affected] = (rhs[affected] - entry * value) % prime
            degree[affected] -= 1
            if degree[affected] <= 1:
                queue.append(affected)

    contradictions = [(index, rhs[index]) for index, value in enumerate(degree) if value == 0 and rhs[index]][:32]
    inconsistent = sum(value == 0 and bool(rhs[index]) for index, value in enumerate(degree))
    core_columns = sum(active)
    core_rows = sum(value > 0 for value in degree)
    if inconsistent:
        status = "PROVED_NO_SOLUTION_ON_CLOSED_COMPONENT_MOD_PRIME"
    elif core_columns == 0:
        status = "PASS_CLOSED_COMPONENT_SOLVED_MOD_PRIME"
    else:
        status = "CLOSED_COMPONENT_CORE_REQUIRES_SPARSE_LINEAR_ALGEBRA"

    solution_digest = hashlib.sha256()
    nonzero_solution = 0
    for column, value in enumerate(solution):
        if value:
            nonzero_solution += 1
            solution_digest.update(f"{column}\t{value}\n".encode())
    return {
        "prime": prime,
        "assigned_columns": assigned,
        "core_columns": core_columns,
        "core_rows": core_rows,
        "zero_rows_nonzero_rhs": inconsistent,
        "contradiction_samples": contradictions,
        "partial_solution_nonzero_columns": nonzero_solution,
        "partial_solution_logical_sha256": solution_digest.hexdigest(),
        "status": status,
    }


def main() -> None:
    target, row_adj, column_adj, degree_counts, minimum_hist, row_degrees = load()
    components = component_census(target, row_adj, column_adj, row_degrees)
    structural_peel = column_singleton_peel(target, row_adj, column_adj)
    alternating_results = [alternating_leaf_peel(prime, target, row_adj, column_adj) for prime in (1009, 1013)]
    results = [peel(prime, target, row_adj, column_adj) for prime in (1009, 1013)]
    payload = {
        "status": "PASS_EXACT_CLOSED_COMPONENT_MODULAR_PEEL_AUDIT",
        "target_K9_rows": 49988,
        "closed_component_rows_by_degree": degree_counts,
        "columns_by_minimum_degree": minimum_hist,
        "columns": len(column_adj),
        "weighted_edges": sum(map(len, row_adj)),
        "connected_components": len(components),
        "largest_components": components[:32],
        "column_singleton_quotient": structural_peel,
        "alternating_leaf_results": alternating_results,
        "prime_results": results,
        "interpretation": (
            "The target-rooted K0--K9 row/column component is incidence-closed. "
            "A modular contradiction is therefore definitive over that prime; a residual core is complete but requires sparse elimination."
        ),
        "pins": {path.name: digest for path, digest in PINS.items()},
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["logical_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
