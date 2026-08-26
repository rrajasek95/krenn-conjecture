#!/usr/bin/env python3
"""Orbit census and bounded generic-rank screen for 2/3 missing 611 pivots."""

from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
UPSTREAM = HERE / "results_tail_polar_source_lift.json"
OUT = HERE / "results_multi_cofactor_generic_rank_screen.json"
VERTICES = tuple(range(8))
EDGES = tuple(combinations(VERTICES, 2))
COLUMNS = tuple((site, tail) for tail in (6, 7) for site in range(6))
COLUMN_NAMES = tuple(f"{'y' if tail == 6 else 'z'}{site}"
                     for site, tail in COLUMNS)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def logical_hash(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def file_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def profile(word):
    return tuple(sorted(Counter(word).values(), reverse=True))


def hafnian(values, subset, modulus):
    @lru_cache(None)
    def rec(vertices):
        if not vertices:
            return 1
        first = vertices[0]
        answer = 0
        for index in range(1, len(vertices)):
            second = vertices[index]
            rest = vertices[1:index] + vertices[index+1:]
            answer += values[tuple(sorted((first, second)))] * rec(rest)
        return answer % modulus
    return rec(tuple(subset))


def matrix_rank(rows, modulus):
    if not rows:
        return 0
    matrix = [list(map(lambda value: value % modulus, row)) for row in rows]
    rank = 0
    for column in range(len(matrix[0])):
        pivot = next((row for row in range(rank, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], -1, modulus)
        matrix[rank] = [(entry*inverse) % modulus for entry in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [(left-scale*right) % modulus
                           for left, right in zip(matrix[row], matrix[rank])]
        rank += 1
    return rank


def solve_square(matrix, rhs, modulus):
    augmented = [list(row) + [value]
                 for row, value in zip(matrix, rhs)]
    size = len(matrix)
    for column in range(size):
        pivot = next((row for row in range(column, size)
                      if augmented[row][column] % modulus), None)
        if pivot is None:
            return None
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        inverse = pow(augmented[column][column] % modulus, -1, modulus)
        augmented[column] = [(entry*inverse) % modulus
                             for entry in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            scale = augmented[row][column] % modulus
            augmented[row] = [(left-scale*right) % modulus
                              for left, right in zip(augmented[row],
                                                     augmented[column])]
    return tuple(augmented[row][-1] % modulus for row in range(size))


def fixed_tail_actions():
    actions = []
    for block_permutation in permutations(range(3)):
        for flips in product((0, 1), repeat=4):
            mapping = {}
            for vertex in VERTICES:
                block, clone = divmod(vertex, 2)
                image_block = (block_permutation[block]
                               if block < 3 else 3)
                mapping[vertex] = 2*image_block + (clone ^ flips[block])
            actions.append(tuple(COLUMNS.index(tuple(sorted(
                (mapping[site], mapping[tail]))))
                for site, tail in COLUMNS))
    actions = tuple(sorted(set(actions)))
    require(len(actions) == 96, "fixed-tail group size changed")
    return actions


def subset_orbits(size, actions):
    unseen = set(combinations(range(12), size))
    records = []
    while unseen:
        representative = min(unseen)
        orbit = {tuple(sorted(action[index] for index in representative))
                 for action in actions}
        unseen -= orbit
        records.append({
            "representative_indices": list(representative),
            "representative_columns": [COLUMN_NAMES[index]
                                       for index in representative],
            "orbit_size": len(orbit),
        })
    return records


def intersecting_edge_sets(size):
    return tuple(candidate for candidate in combinations(EDGES, size)
                 if all(set(left) & set(right)
                        for left, right in combinations(candidate, 2)))


def constrained_graph(missing, modulus, seed):
    """Find a deterministic torus sample with exactly these h2 columns zero.

    Target edges are pairwise intersecting, so no Hafnian matching contains
    two of them.  The missing-cofactor equations are therefore a literal
    linear system in those targets after all other edges are specialized.
    """
    for attempt in range(1, 40):
        base = {edge: (1 + 41*(index+1) + 17*(seed+attempt)*(index+3)**2)
                % modulus for index, edge in enumerate(EDGES)}
        base = {edge: value or 1 for edge, value in base.items()}
        for targets in intersecting_edge_sets(len(missing)):
            values = dict(base)
            for edge in targets:
                values[edge] = 0
            constants = []
            coefficient_rows = []
            for column in missing:
                site, tail = COLUMNS[column]
                subset = tuple(vertex for vertex in VERTICES
                               if vertex not in (site, tail))
                constant = hafnian(values, subset, modulus)
                row = []
                for edge in targets:
                    trial = dict(values)
                    trial[edge] = 1
                    row.append((hafnian(trial, subset, modulus)-constant)
                               % modulus)
                constants.append(constant)
                coefficient_rows.append(row)
            if matrix_rank(coefficient_rows, modulus) != len(missing):
                continue
            solution = solve_square(coefficient_rows,
                                    [(-value) % modulus
                                     for value in constants], modulus)
            require(solution is not None, "ranked target system did not solve")
            if not all(solution):
                continue
            for edge, value in zip(targets, solution):
                values[edge] = value
            cofactors = []
            for site, tail in COLUMNS:
                subset = tuple(vertex for vertex in VERTICES
                               if vertex not in (site, tail))
                cofactors.append(hafnian(values, subset, modulus))
            if any(cofactors[index] for index in missing):
                continue
            if any(not cofactors[index] for index in range(12)
                   if index not in missing):
                continue
            return values, targets, cofactors, attempt
    raise RuntimeError(("failed to sample declared cofactor stratum",
                        missing, modulus, seed))


def response_rows(graphs, missing, modulus):
    rows_71 = []
    rows_332 = []
    for word in product(range(3), repeat=8):
        word_profile = profile(word)
        if word_profile not in ((7, 1), (3, 3, 2)):
            continue
        values = []
        for column in missing:
            site, tail = COLUMNS[column]
            if word[site] != 0 or word[tail] != 1:
                values.append(0)
                continue
            counts = Counter(word)
            counts[0] -= 1
            counts[1] -= 1
            if any(counts[colour] % 2 for colour in range(3)):
                values.append(0)
                continue
            coefficient = 1
            remaining = tuple(vertex for vertex in VERTICES
                              if vertex not in (site, tail))
            for colour in range(3):
                subset = tuple(vertex for vertex in remaining
                               if word[vertex] == colour)
                coefficient *= hafnian(graphs[colour], subset, modulus)
            values.append(coefficient % modulus)
        if any(values):
            (rows_71 if word_profile == (7, 1) else rows_332).append(values)
    return rows_71, rows_332


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    upstream = json.loads(UPSTREAM.read_text())
    require(upstream["logical_sha256"] ==
            "273c321313d8bea2dcd3ea19fe282c078dcfa481d956839607db35100a7612b9",
            "source-lift upstream digest changed")

    actions = fixed_tail_actions()
    orbit_records = {size: subset_orbits(size, actions) for size in (2, 3)}
    require([len(orbit_records[size]) for size in (2, 3)] == [5, 7],
            "cofactor subset orbit census changed")
    require(sum(row["orbit_size"] for row in orbit_records[2]) == 66
            and sum(row["orbit_size"] for row in orbit_records[3]) == 220,
            "cofactor subset orbit sizes changed")

    primes = (1009, 1013)
    rank_deficient = []
    for size in (2, 3):
        for orbit_index, record in enumerate(orbit_records[size]):
            missing = tuple(record["representative_indices"])
            screens = []
            for prime in primes:
                graph2, targets, cofactors, attempt = constrained_graph(
                    missing, prime, 100*size + 10*orbit_index)
                graphs = []
                for colour in (0, 1):
                    graph = {
                        edge: (1 + 29*(index+1)
                               + 13*(colour+1)*(orbit_index+3)*(index+2)**2)
                              % prime
                        for index, edge in enumerate(EDGES)
                    }
                    graphs.append({edge: value or 1
                                   for edge, value in graph.items()})
                graphs.append(graph2)
                rows_71, rows_332 = response_rows(graphs, missing, prime)
                rank_71 = matrix_rank(rows_71, prime)
                rank_332 = matrix_rank(rows_332, prime)
                rank_combined = matrix_rank(rows_71 + rows_332, prime)
                screens.append({
                    "prime": prime,
                    "target_edges": ["".join(map(str, edge))
                                     for edge in targets],
                    "sampling_attempt": attempt,
                    "missing_cofactor_values": [cofactors[index]
                                                 for index in missing],
                    "other_cofactors_nonzero": all(
                        cofactors[index] for index in range(12)
                        if index not in missing),
                    "row_counts": {"7+1": len(rows_71),
                                   "3+3+2": len(rows_332)},
                    "ranks": {"7+1": rank_71, "3+3+2": rank_332,
                              "combined": rank_combined},
                })
            record["screens"] = screens
            record["generic_screen_rank"] = min(
                screen["ranks"]["combined"] for screen in screens)
            record["generic_screen_full"] = (
                record["generic_screen_rank"] == size)
            if not record["generic_screen_full"]:
                rank_deficient.append({"size": size, **record})

    result = {
        "status": "PASS bounded generic multi-cofactor rank screen",
        "fixed_tail_stabilizer_order": len(actions),
        "subset_orbits": {str(size): orbit_records[size] for size in (2, 3)},
        "orbit_counts": {"2": 5, "3": 7},
        "rank_deficient_representatives": rank_deficient,
        "rank_deficient_count": len(rank_deficient),
        "method": (
            "For each orbit and each of p=1009,1013, solve the selected "
            "Hafnian-cofactor equations exactly as a linear system in "
            "pairwise-incident target edges, require all other 611 pivots "
            "nonzero, then rank the literal 7+1 plus 3+3+2 source rows."),
        "scope_guard": (
            "A full modular rank sample proves a nonempty full-rank open on "
            "the sampled component; it does not exclude lower-rank closed "
            "subvarieties or certify every irreducible component of a "
            "cofactor intersection. No Fitting ideal is computed."),
        "source_hashes": {"source_lift_result": file_hash(UPSTREAM)},
    }
    result["logical_sha256"] = logical_hash(result)
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("multi-cofactor generic rank screen: PASS",
          result["logical_sha256"])
    print("orbit counts", result["orbit_counts"],
          "rank-deficient", len(rank_deficient))
    for size in (2, 3):
        print("size", size, [(row["representative_columns"],
                              row["generic_screen_rank"])
                             for row in orbit_records[size]])


if __name__ == "__main__":
    main()
