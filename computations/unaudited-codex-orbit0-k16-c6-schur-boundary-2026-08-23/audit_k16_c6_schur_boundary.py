#!/usr/bin/env python3
"""Finite source-faithful Schur interface on the 28 K16 c6 blockers.

The first stage reconstructs the blockers and their complete incident mixed
degree-24 source-column H-orbits.  Later stages attach only the deterministic
higher-cycle Morse pivots; no unrestricted closure is permitted.
"""

from collections import Counter
from fractions import Fraction
from math import gcd
from hashlib import sha256
import argparse
import importlib.util
import json
from pathlib import Path
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
HQ_PATH = (ROOT / "computations/unaudited-codex-orbit0-k16-h-quotient-closure-2026-08-23"
           / "run_k16_h_quotient_closure.py")
RESULT = HERE / "results_k16_c6_schur_boundary.json"
INTERFACE = HERE / "boundary_incident_interface.json"
SCHUR = HERE / "boundary_schur_interface.json"
VERDICT = HERE / "results_k16_c6_schur_verdict.json"
PARENT_CENSUS = HERE / "boundary_parent_column_census.json"
ROW_CAP = 250_000
COLUMN_CAP = 250_000


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, path)
    spec.loader.exec_module(module)
    return module


HQ = load("k16_c6_hq", HQ_PATH)
WD = HQ.WD
D24 = HQ.D24
F = HQ.F
H = HQ.H


def graph_data(row):
    """Return the port-cycle partition and a cycle id for every port."""
    parent = list(range(24))
    size = [1] * 24
    edges = [0] * 24
    degree = [0] * 24

    def root(x):
        while parent[x] != x:
            x = parent[x]
        return x

    for cell in row:
        u, v, a, b = D24.BASE.CELLS[cell]
        x, y = 3 * u + a, 3 * v + b
        degree[x] += 1
        degree[y] += 1
        x, y = root(x), root(y)
        if x == y:
            edges[x] += 1
        else:
            if size[x] < size[y]:
                x, y = y, x
            parent[y] = x
            size[x] += size[y]
            edges[x] += edges[y] + 1
    require(set(degree) == {2}, (row.hex(), Counter(degree)))
    roots = sorted((x for x in range(24) if root(x) == x), key=lambda x: size[x])
    require(all(edges[x] == size[x] for x in roots), row.hex())
    root_id = {}
    for index, component in enumerate(roots):
        for port in range(24):
            if root(port) == component:
                root_id[port] = index
    return tuple(size[x] for x in roots), root_id


def eligible_pivot(row):
    """Lex first mixed physical PM using four distinct port cycles, or None."""
    partition, root_id = graph_data(row)
    if len(partition) < 4:
        return None
    by_edge = {}
    for cell in row:
        u, v, a, b = D24.BASE.CELLS[cell]
        by_edge.setdefault((u, v), set()).add((cell, root_id[3 * u + a], a, b))

    def visit(unused, cycles, colours, cells):
        if not unused:
            if len(set(colours)) > 1:
                return tuple(colours), bytes(sorted(cells))
            return None
        u = min(unused)
        for v in sorted(unused - {u}):
            edge = (u, v) if u < v else (v, u)
            for cell, cycle, a, b in sorted(by_edge.get(edge, ())):
                if cycle in cycles:
                    continue
                new_colours = list(colours)
                if u < v:
                    new_colours[u], new_colours[v] = a, b
                else:
                    new_colours[u], new_colours[v] = b, a
                answer = visit(unused - {u, v}, cycles | {cycle}, new_colours,
                               cells + [cell])
                if answer is not None:
                    return answer
        return None

    return visit(set(range(8)), set(), [0] * 8, [])


def collect_blockers():
    blockers = []
    seen_partition = 0
    for index, (row, numerator, denominator) in enumerate(WD.literal_records(WD.INPUT), 1):
        partition, _ = graph_data(row)
        if partition != (2, 2, 2, 2, 4, 12):
            continue
        seen_partition += 1
        if eligible_pivot(row) is None:
            blockers.append((row, numerator, denominator))
    require(seen_partition == 12_294, seen_partition)
    require(len(blockers) == 28, len(blockers))
    return blockers


def col_key(column):
    word, multiplier = column
    return "".join(map(str, word)) + ":" + multiplier.hex()


def expand_incident_stage():
    """Expand the frozen 1,114 columns through K<=16, without any closure."""
    started = time.monotonic()
    seed = json.loads(RESULT.read_text())
    require(seed["status"] == "BOUNDARY_AND_INCIDENT_COLUMNS_EXACT", seed["status"])
    columns = []
    rows = set()
    high_k16 = set()
    k_hist = Counter()
    cycle_hist = Counter()
    for index, key in enumerate(seed["incident_H_columns"], 1):
        column = HQ.parse_column_key(key)
        representative, orbit_size, entries, _ = HQ.column_vector(column)
        require(HQ.column_key(representative) == key, key)
        encoded = []
        for row, value in sorted(entries.items()):
            degree = D24.row_k_degree(row)
            partition, _ = graph_data(row)
            rows.add(row)
            k_hist[degree] += 1
            cycle_hist[(degree, len(partition))] += 1
            if degree == 16 and len(partition) >= 7:
                high_k16.add(row)
            encoded.append([row.hex(), value])
        columns.append({"key": key, "orbit_size": orbit_size, "entries": encoded})
        require(len(rows) <= ROW_CAP, len(rows))
        if index % 100 == 0:
            print(f"EXPAND columns={index} rows={len(rows)} high_k16={len(high_k16)} "
                  f"elapsed={time.monotonic()-started:.1f}", flush=True)
    payload = {
        "schema": "orbit0-k16-c6-incident-interface-v1",
        "status": "EXACT_ONE_PAGE_UNREDUCED",
        "seed_logical_sha256": seed["logical_sha256"],
        "column_orbits": len(columns),
        "row_orbits": len(rows),
        "high_cycle_K16_row_orbits": len(high_k16),
        "row_K_degree_occurrences": dict(sorted(k_hist.items())),
        "row_K_cycle_occurrences": {f"{k},{c}": v for (k, c), v in sorted(cycle_hist.items())},
        "columns": columns,
        "caps": {"row_orbits": ROW_CAP, "column_orbits": COLUMN_CAP},
        "elapsed_seconds": time.monotonic() - started,
    }
    logical = dict(payload)
    logical.pop("elapsed_seconds")
    payload["logical_sha256"] = sha256(json.dumps(logical, sort_keys=True,
                                                   separators=(",", ":")).encode()).hexdigest()
    INTERFACE.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: payload[key] for key in
                      ("status", "column_orbits", "row_orbits",
                       "high_cycle_K16_row_orbits", "logical_sha256",
                       "elapsed_seconds")}, sort_keys=True))


def add_scaled(left, right, scale):
    for key, value in right.items():
        updated = left.get(key, 0) + scale * value
        if updated:
            left[key] = updated
        else:
            left.pop(key, None)


def pivot_column(row):
    witness = eligible_pivot(row)
    require(witness is not None, (row.hex(), "missing proven high-cycle pivot"))
    word, cells = witness
    multiplier = list(row)
    for cell in cells:
        multiplier.remove(cell)
    return HQ.canonical_column((tuple(word), bytes(sorted(multiplier))))


def schur_stage():
    """Reduce the one-page columns only through deterministic c>=7 K16 pivots."""
    started = time.monotonic()
    page = json.loads(INTERFACE.read_text())
    require(page["status"] == "EXACT_ONE_PAGE_UNREDUCED", page["status"])
    partition_cache = {}

    def cycle_count(row):
        value = partition_cache.get(row)
        if value is None:
            value = len(graph_data(row)[0])
            partition_cache[row] = value
        return value

    def reducible(row):
        return D24.row_k_degree(row) == 16 and cycle_count(row) >= 7

    normal_forms = {}
    pivot_records = {}
    active = set()

    def normal_form(row):
        found = normal_forms.get(row)
        if found is not None:
            return found
        require(reducible(row), row.hex())
        require(row not in active, (row.hex(), "cycle descent recursed"))
        active.add(row)
        column = pivot_column(row)
        representative, orbit_size, entries, _ = HQ.column_vector(column)
        require(representative == column, HQ.column_key(column))
        pivot_value = entries.get(row)
        require(pivot_value == orbit_size, (row.hex(), pivot_value, orbit_size))
        source_cycles = cycle_count(row)
        answer = Counter()
        tail_hist = Counter()
        for target, value in entries.items():
            if target == row:
                continue
            require(value % pivot_value == 0,
                    (row.hex(), target.hex(), value, pivot_value))
            multiplicity = value // pivot_value
            target_cycles = cycle_count(target)
            tail_hist[(D24.row_k_degree(target), target_cycles)] += multiplicity
            if reducible(target):
                require(target_cycles < source_cycles,
                        (row.hex(), target.hex(), source_cycles, target_cycles))
                add_scaled(answer, normal_form(target), -multiplicity)
            else:
                answer[target] -= multiplicity
        answer = Counter({key: value for key, value in answer.items() if value})
        active.remove(row)
        require(len(answer) <= ROW_CAP, (row.hex(), len(answer)))
        normal_forms[row] = answer
        pivot_records[row] = {
            "column": HQ.column_key(column),
            "source_orbit_size": orbit_size,
            "source_cycles": source_cycles,
            "raw_tail_entries": len(entries) - 1,
            "normal_form_entries": len(answer),
            "tail_K_cycle_histogram": {
                f"{k},{c}": value for (k, c), value in sorted(tail_hist.items())
            },
        }
        return answer

    reduced_columns = []
    row_union = set()
    total_incidence = 0
    for index, record in enumerate(page["columns"], 1):
        vector = Counter({bytes.fromhex(row): value for row, value in record["entries"]})
        answer = Counter()
        for row, value in vector.items():
            if reducible(row):
                add_scaled(answer, normal_form(row), value)
            else:
                answer[row] += value
        answer = Counter({key: value for key, value in answer.items() if value})
        row_union.update(answer)
        total_incidence += len(answer)
        require(len(row_union) <= ROW_CAP, len(row_union))
        reduced_columns.append({
            "key": record["key"],
            "entries": [[row.hex(), value] for row, value in sorted(answer.items())],
        })
        if index % 100 == 0:
            print(f"SCHUR columns={index} rows={len(row_union)} incidence={total_incidence} "
                  f"pivots={len(normal_forms)} elapsed={time.monotonic()-started:.1f}",
                  flush=True)

    # Relative target: exact frozen target on this induced row set, plus the
    # corrections from high rows actually present on this one page.  No claim
    # is made about higher-pivot ancestors outside this induced page.
    # The weighted DAFSA keeps the frozen collector's representative, which is
    # not necessarily the lex representative chosen by HQ.canonical_row.  Load
    # its 1.85M terminals once and query the complete H orbit exactly.
    frozen_target = {row: (numerator, denominator)
                     for row, numerator, denominator in WD.literal_records(WD.INPUT)}
    orbit_mass_cache = {}

    def orbit_mass(row):
        if row in orbit_mass_cache:
            return orbit_mass_cache[row]
        hits = {frozen_target[moved] for action in H
                if (moved := F.move_row(row, action)) in frozen_target}
        require(len(hits) <= 1, (row.hex(), hits))
        answer = next(iter(hits)) if hits else None
        orbit_mass_cache[row] = answer
        return answer

    seed = json.loads(RESULT.read_text())
    boundary_rows = {HQ.canonical_row(bytes.fromhex(record["row"]))
                     for record in seed["blockers"]}
    require(len(boundary_rows) == 28, len(boundary_rows))
    row_union.update(boundary_rows)
    target = Counter()
    queried = set(row_union)
    high_rows = {bytes.fromhex(row) for record in page["columns"]
                 for row, _ in record["entries"]
                 if reducible(bytes.fromhex(row))}
    queried.update(high_rows)
    target_hits = 0
    high_target_hits = 0
    for row in sorted(queried):
        if D24.row_k_degree(row) != 16:
            continue
        mass = orbit_mass(row)
        if mass is None:
            continue
        value = Fraction(*mass)
        target_hits += 1
        if reducible(row):
            high_target_hits += 1
            add_scaled(target, normal_form(row), value)
        elif row in row_union:
            target[row] += value
    target = Counter({key: value for key, value in target.items() if value})
    row_union.update(target)
    require(len(row_union) <= ROW_CAP, len(row_union))

    payload = {
        "schema": "orbit0-k16-c6-induced-schur-v1",
        "status": "EXACT_FINITE_ONE_PAGE_SCHUR_INTERFACE",
        "seed_logical_sha256": page["logical_sha256"],
        "column_orbits": len(reduced_columns),
        "row_orbits": len(row_union),
        "matrix_nonzeros": total_incidence,
        "higher_cycle_pivot_rows_memoized": len(normal_forms),
        "pivot_cycle_histogram": dict(sorted(Counter(
            record["source_cycles"] for record in pivot_records.values()).items())),
        "target_queries_nonzero": target_hits,
        "higher_cycle_target_queries_nonzero": high_target_hits,
        "relative_target_entries": [[row.hex(), [value.numerator, value.denominator]]
                                    for row, value in sorted(target.items())],
        "columns": reduced_columns,
        "pivots": {row.hex(): pivot_records[row] for row in sorted(pivot_records)},
        "scope_guard": (
            "Complete source columns incident to the 28 c6 blockers, reduced only "
            "through deterministic c>=7 K16 pivots. The target includes high rows "
            "present on this one page, but not unenumerated higher-pivot ancestors; "
            "any rank verdict is relative to this finite induced interface."
        ),
        "caps": {"row_orbits": ROW_CAP, "column_orbits": COLUMN_CAP},
        "elapsed_seconds": time.monotonic() - started,
    }
    logical = dict(payload)
    logical.pop("elapsed_seconds")
    payload["logical_sha256"] = sha256(json.dumps(logical, sort_keys=True,
                                                   separators=(",", ":")).encode()).hexdigest()
    SCHUR.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: payload[key] for key in
                      ("status", "column_orbits", "row_orbits", "matrix_nonzeros",
                       "higher_cycle_pivot_rows_memoized", "target_queries_nonzero",
                       "higher_cycle_target_queries_nonzero", "logical_sha256",
                       "elapsed_seconds")}, sort_keys=True))


def parent_census_stage():
    """Count the exact first backward source page without expanding outputs."""
    started = time.monotonic()
    page = json.loads(INTERFACE.read_text())
    parents = set()
    for record in page["columns"]:
        for row_hex, _ in record["entries"]:
            row = bytes.fromhex(row_hex)
            if D24.row_k_degree(row) == 16 and len(graph_data(row)[0]) >= 7:
                parents.add(row)
    require(len(parents) == 374, len(parents))
    per_parent = []
    global_columns = set()
    raw_total = 0
    canonical_total = 0
    for index, parent in enumerate(sorted(parents), 1):
        raw = D24.incident_degree24_columns(parent)
        canonical = {HQ.canonical_column(column) for column in raw}
        raw_total += len(raw)
        canonical_total += len(canonical)
        global_columns.update(canonical)
        per_parent.append({
            "parent": parent.hex(),
            "cycles": len(graph_data(parent)[0]),
            "literal_incident_columns": len(raw),
            "canonical_incident_columns": len(canonical),
        })
        if index % 50 == 0:
            print(f"PARENTS {index}/374 global_columns={len(global_columns)} "
                  f"elapsed={time.monotonic()-started:.1f}", flush=True)
    payload = {
        "schema": "orbit0-k16-c6-backward-parent-column-census-v1",
        "status": "EXACT_COUNTS_NO_OUTPUT_EXPANSION",
        "parents": len(parents),
        "literal_incident_occurrences": raw_total,
        "canonical_incident_occurrences": canonical_total,
        "global_canonical_column_orbits": len(global_columns),
        "reference_difference_generators_upper_bound": canonical_total - len(parents),
        "per_parent": per_parent,
        "global_columns": [HQ.column_key(column)
                           for column in sorted(global_columns, key=HQ.column_key)],
        "scope_guard": "Backward c>=7 parents from the 1,114-column page only; columns counted, outputs not expanded.",
        "elapsed_seconds": time.monotonic() - started,
    }
    logical = dict(payload)
    logical.pop("elapsed_seconds")
    payload["logical_sha256"] = sha256(json.dumps(logical, sort_keys=True,
                                                   separators=(",", ":")).encode()).hexdigest()
    PARENT_CENSUS.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: payload[key] for key in
                      ("status", "parents", "literal_incident_occurrences",
                       "canonical_incident_occurrences", "global_canonical_column_orbits",
                       "reference_difference_generators_upper_bound",
                       "logical_sha256", "elapsed_seconds")}, sort_keys=True))


def modular_rank(columns, prime, row_degree):
    basis = {}
    order = {}
    sequence = []
    max_nnz = 0
    for raw in columns:
        vector = {row: value % prime for row, value in raw.items() if value % prime}
        while True:
            old = [(order[row], row) for row in vector if row in basis]
            if not old:
                break
            _, pivot = min(old)
            scale = vector[pivot]
            for row, value in basis[pivot].items():
                updated = (vector.get(row, 0) - scale * value) % prime
                if updated:
                    vector[row] = updated
                else:
                    vector.pop(row, None)
        if not vector:
            continue
        pivot = min(vector, key=lambda row: (row_degree[row], row))
        inverse = pow(vector[pivot], prime - 2, prime)
        vector = {row: value * inverse % prime for row, value in vector.items()}
        basis[pivot] = vector
        order[pivot] = len(sequence)
        sequence.append(pivot)
        max_nnz = max(max_nnz, len(vector))
    return len(basis), max_nnz


def verdict_stage():
    started = time.monotonic()
    data = json.loads(SCHUR.read_text())
    require(data["status"] == "EXACT_FINITE_ONE_PAGE_SCHUR_INTERFACE", data["status"])
    columns = []
    row_degree = Counter()
    for record in data["columns"]:
        vector = {bytes.fromhex(row): value for row, value in record["entries"]}
        require(all(vector.values()), record["key"])
        columns.append(vector)
        row_degree.update(vector)
    target = {bytes.fromhex(row): Fraction(*value)
              for row, value in data["relative_target_entries"]}

    candidates = []
    candidate_count = 0
    for column_index, vector in enumerate(columns):
        private = sorted(row for row in vector if row_degree[row] == 1)
        for left_index, left in enumerate(private):
            for right in private[left_index + 1:]:
                a, b = vector[left], vector[right]
                divisor = gcd(abs(a), abs(b))
                lam_left, lam_right = b // divisor, -a // divisor
                if lam_left < 0:
                    lam_left, lam_right = -lam_left, -lam_right
                pairing = lam_left * target.get(left, 0) + lam_right * target.get(right, 0)
                if not pairing:
                    continue
                candidate_count += 1
                candidates.append((left, right, lam_left, lam_right, pairing,
                                   column_index))
    require(candidates, "no exact private-row separator found")
    left, right, lam_left, lam_right, pairing, owner = min(
        candidates, key=lambda item: (item[0], item[1], item[2], item[3]))
    dual = {left: lam_left, right: lam_right}
    annihilation = []
    for index, vector in enumerate(columns):
        value = sum(dual.get(row, 0) * coefficient
                    for row, coefficient in vector.items())
        if value:
            annihilation.append((index, value))
    require(not annihilation, annihilation[:3])
    direct_pairing = sum(value * target.get(row, 0) for row, value in dual.items())
    require(direct_pairing == pairing and pairing, (direct_pairing, pairing))

    ranks = {}
    for prime in (32003, 32009):
        rank, max_nnz = modular_rank(columns, prime, row_degree)
        ranks[str(prime)] = {"rank": rank, "max_echelon_column_nnz": max_nnz}

    def row_record(row, coefficient):
        partition, _ = graph_data(row)
        return {
            "row": row.hex(),
            "coefficient": coefficient,
            "K_degree": D24.row_k_degree(row),
            "cycle_partition": list(partition),
            "matrix_incidence_degree": row_degree[row],
            "relative_target_mass": [target.get(row, 0).numerator,
                                     target.get(row, 0).denominator],
        }

    payload = {
        "schema": "orbit0-k16-c6-induced-schur-verdict-v1",
        "status": "EXACT_RELATIVE_NONMEMBERSHIP_TWO_ROW_DUAL",
        "schur_logical_sha256": data["logical_sha256"],
        "matrix": {
            "row_orbits": data["row_orbits"],
            "column_orbits": data["column_orbits"],
            "nonzeros": data["matrix_nonzeros"],
            "rank_modular": ranks,
            "private_row_orbits": sum(value == 1 for value in row_degree.values()),
            "columns_without_private_row": sum(
                not any(row_degree[row] == 1 for row in column) for column in columns),
        },
        "two_row_target_coupled_private_separators": candidate_count,
        "lex_first_dual": {
            "rows": [row_record(left, lam_left), row_record(right, lam_right)],
            "owner_column": data["columns"][owner]["key"],
            "owner_entries": [
                [left.hex(), columns[owner][left]],
                [right.hex(), columns[owner][right]],
            ],
            "pairing_with_relative_target": [pairing.numerator, pairing.denominator],
            "annihilated_column_orbits": len(columns),
        },
        "projection_reconciliation": (
            "The 28-row boundary projection may have full rank, but this dual uses "
            "one K13 c7 exterior row and one K16 c5 row. Projecting away the K13 "
            "source tail destroys the obstruction."
        ),
        "scope_guard": data["scope_guard"],
        "elapsed_seconds": time.monotonic() - started,
    }
    logical = dict(payload)
    logical.pop("elapsed_seconds")
    payload["logical_sha256"] = sha256(json.dumps(logical, sort_keys=True,
                                                   separators=(",", ":")).encode()).hexdigest()
    VERDICT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": payload["status"],
        "ranks": ranks,
        "two_row_separators": candidate_count,
        "dual_pairing": payload["lex_first_dual"]["pairing_with_relative_target"],
        "logical_sha256": payload["logical_sha256"],
        "elapsed_seconds": payload["elapsed_seconds"],
    }, sort_keys=True))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutate", action="store_true")
    parser.add_argument("--expand", action="store_true")
    parser.add_argument("--schur", action="store_true")
    parser.add_argument("--verdict", action="store_true")
    parser.add_argument("--parent-census", action="store_true")
    args = parser.parse_args()
    if args.expand:
        expand_incident_stage()
        return
    if args.schur:
        schur_stage()
        return
    if args.verdict:
        verdict_stage()
        return
    if args.parent_census:
        parent_census_stage()
        return
    started = time.monotonic()
    blockers = collect_blockers()
    incident = set()
    raw_counts = []
    for row, _, _ in blockers:
        raw = D24.incident_degree24_columns(row)
        raw_counts.append(len(raw))
        incident.update(HQ.canonical_column(column) for column in raw)
    require(len(incident) <= COLUMN_CAP, len(incident))
    if args.mutate:
        incident.pop()
    payload = {
        "schema": "orbit0-k16-c6-schur-boundary-v1",
        "status": "BOUNDARY_AND_INCIDENT_COLUMNS_EXACT",
        "scope": "28 c6 blockers and all incident mixed D24 source-column H-orbits; no closure yet",
        "partition": [2, 2, 2, 2, 4, 12],
        "partition_orbits": 12294,
        "blocker_orbits": len(blockers),
        "blockers": [
            {"row": row.hex(), "target_mass": [numerator, denominator],
             "literal_incident_columns": raw}
            for (row, numerator, denominator), raw in zip(blockers, raw_counts, strict=True)
        ],
        "incident_H_column_orbits": len(incident),
        "incident_H_columns": [col_key(column) for column in sorted(incident, key=col_key)],
        "caps": {"row_orbits": ROW_CAP, "column_orbits": COLUMN_CAP},
        "elapsed_seconds": time.monotonic() - started,
    }
    logical = dict(payload)
    logical.pop("elapsed_seconds")
    payload["logical_sha256"] = sha256(json.dumps(logical, sort_keys=True,
                                                   separators=(",", ":")).encode()).hexdigest()
    RESULT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: payload[key] for key in
                      ("status", "blocker_orbits", "incident_H_column_orbits",
                       "logical_sha256", "elapsed_seconds")}, sort_keys=True))


if __name__ == "__main__":
    main()
