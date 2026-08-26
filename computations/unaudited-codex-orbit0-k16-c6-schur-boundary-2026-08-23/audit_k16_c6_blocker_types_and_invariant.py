#!/usr/bin/env python3
"""Classify the 28 C6 blockers and test their corrected signed Schur projection.

The frozen Schur JSON is not used: its producer applied Counter's positive-part
cleanup.  This audit replays only the 28-row projection of the 1,114 incident
columns, eliminating c>=7 K16 heads with exact signed arithmetic.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import product
from math import gcd, lcm
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
PROVIDER = HERE / "audit_k16_c6_schur_boundary.py"
SEED = HERE / "results_k16_c6_schur_boundary.json"
PAGE = HERE / "boundary_incident_interface.json"
OUT = HERE / "results_k16_c6_blocker_types_and_invariant.json"
TYPES = HERE / "k16_c6_blocker_types.tsv"
INVARIANT = HERE / "k16_c6_relative_invariant.tsv"


def load_provider():
    spec = importlib.util.spec_from_file_location("c6_boundary_provider", PROVIDER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


G = load_provider()


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


@lru_cache(None)
def perfect_matchings(vertices):
    if not vertices:
        return ((),)
    u = vertices[0]
    answer = []
    for index, v in enumerate(vertices[1:], 1):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            answer.append(((u, v),) + tail)
    return tuple(answer)


PM8 = perfect_matchings(tuple(range(8)))


def canonical_necklace(word):
    word = tuple(word)
    candidates = []
    for oriented in (word, tuple(reversed(word))):
        candidates.extend(oriented[index:] + oriented[:index]
                          for index in range(len(word)))
    return min(candidates)


def coloured_necklaces(row):
    edges = []
    adjacency = [[] for _ in range(24)]
    for cell in row:
        u, v, a, b = G.D24.BASE.CELLS[cell]
        left, right = 3 * u + a, 3 * v + b
        edge_id = len(edges)
        edges.append((left, right))
        adjacency[left].append(edge_id)
        adjacency[right].append(edge_id)
    require(all(len(entries) == 2 for entries in adjacency), row.hex())
    used = set()
    cycles = []
    for seed in range(len(edges)):
        if seed in used:
            continue
        start, _ = edges[seed]
        vertex, edge = start, seed
        word = []
        while True:
            require(edge not in used, (row.hex(), edge))
            used.add(edge)
            word.append(vertex % 3)
            left, right = edges[edge]
            vertex = right if vertex == left else left
            choices = [candidate for candidate in adjacency[vertex]
                       if candidate != edge]
            require(len(choices) == 1, (row.hex(), vertex, choices))
            edge = choices[0]
            if edge == seed:
                require(vertex == start, (row.hex(), vertex, start))
                break
        cycles.append(canonical_necklace(word))
    return tuple(sorted(cycles, key=lambda word: (len(word), word)))


def necklace_text(state):
    return ".".join("".join(map(str, word)) for word in state)


def matching_failure(row):
    _, root_id = G.graph_data(row)
    by_edge = {}
    for cell in set(row):
        u, v, a, b = G.D24.BASE.CELLS[cell]
        by_edge.setdefault((u, v), []).append((cell, root_id[3 * u + a], a, b))
    physical_with_transversal = set()
    transversal_count = 0
    monochromatic = 0
    mixed = 0
    for matching_index, matching in enumerate(PM8):
        choices = [by_edge.get(edge, ()) for edge in matching]
        if any(not entries for entries in choices):
            continue
        for selected in product(*choices):
            cycles = [entry[1] for entry in selected]
            if len(set(cycles)) != 4:
                continue
            physical_with_transversal.add(matching_index)
            transversal_count += 1
            colours = []
            for (_, _, a, b) in selected:
                colours.extend((a, b))
            if len(set(colours)) == 1:
                monochromatic += 1
            else:
                mixed += 1
    require(mixed == 0, (row.hex(), mixed))
    reason = "NO_FOUR_CYCLE_PHYSICAL_TRANSVERSAL" if transversal_count == 0 \
        else "ALL_FOUR_CYCLE_TRANSVERSALS_MONOCHROMATIC"
    return reason, len(physical_with_transversal), transversal_count, monochromatic, mixed


def retain(counter):
    return Counter({key: value for key, value in counter.items() if value})


def primitive(values):
    denominator = 1
    for value in values:
        denominator = lcm(denominator, value.denominator)
    integers = [value.numerator * (denominator // value.denominator)
                for value in values]
    divisor = 0
    for value in integers:
        divisor = gcd(divisor, abs(value))
    require(divisor, integers)
    integers = [value // divisor for value in integers]
    first = next(value for value in integers if value)
    return [-value for value in integers] if first < 0 else integers


def rref_basis(rows, width):
    basis = {}
    for original in rows:
        row = {index: Fraction(value) for index, value in enumerate(original) if value}
        while row:
            pivot = min(row)
            if pivot not in basis:
                scale = row[pivot]
                row = {index: value / scale for index, value in row.items()}
                basis[pivot] = row
                break
            scale = row[pivot]
            for index, value in basis[pivot].items():
                updated = row.get(index, 0) - scale * value
                if updated:
                    row[index] = updated
                else:
                    row.pop(index, None)
    free = [index for index in range(width) if index not in basis]
    nullspace = []
    for free_index in free:
        vector = [Fraction(0) for _ in range(width)]
        vector[free_index] = 1
        for pivot in sorted(basis, reverse=True):
            vector[pivot] = -sum(value * vector[index]
                                 for index, value in basis[pivot].items()
                                 if index != pivot)
        nullspace.append(vector)
    return basis, nullspace


def build(mutate=False):
    seed = json.loads(SEED.read_text())
    page = json.loads(PAGE.read_text())
    require(seed["blocker_orbits"] == 28 and seed["incident_H_column_orbits"] == 1114,
            seed)
    require(page["column_orbits"] == 1114, page["column_orbits"])
    blockers = [bytes.fromhex(record["row"]) for record in seed["blockers"]]
    blocker_index = {row: index for index, row in enumerate(blockers)}
    require(len(blocker_index) == 28, len(blocker_index))

    classifications = []
    for index, (row, record) in enumerate(zip(blockers, seed["blockers"], strict=True)):
        state = coloured_necklaces(row)
        orbit = {G.F.move_row(row, action) for action in G.H}
        require(len(G.H) % len(orbit) == 0, len(orbit))
        reason, physical, transversals, mono, mixed = matching_failure(row)
        classifications.append({
            "index": index,
            "row": row.hex(),
            "necklace_type": necklace_text(state),
            "H_orbit_size": len(orbit),
            "H_stabilizer_order": len(G.H) // len(orbit),
            "failure_reason": reason,
            "physical_matchings_with_transversal": physical,
            "four_cycle_transversals": transversals,
            "monochromatic_transversals": mono,
            "mixed_transversals": mixed,
            "literal_incident_columns": record["literal_incident_columns"],
        })

    partition_cache = {}
    def cycle_count(row):
        if row not in partition_cache:
            partition_cache[row] = len(G.graph_data(row)[0])
        return partition_cache[row]

    def reducible(row):
        return G.D24.row_k_degree(row) == 16 and cycle_count(row) >= 7

    memo = {}
    active = set()
    pivot_count = Counter()
    def projected_normal(row):
        if row in memo:
            return memo[row]
        require(reducible(row) and row not in active, row.hex())
        active.add(row)
        column = G.pivot_column(row)
        representative, orbit_size, entries, _ = G.HQ.column_vector(column)
        require(representative == column and entries[row] == orbit_size,
                (row.hex(), orbit_size, entries.get(row)))
        answer = Counter()
        source_cycles = cycle_count(row)
        pivot_count[source_cycles] += 1
        for tail, value in entries.items():
            if tail == row:
                continue
            multiplier = Fraction(value, orbit_size)
            if reducible(tail):
                require(cycle_count(tail) < source_cycles,
                        (row.hex(), tail.hex(), source_cycles, cycle_count(tail)))
                for blocker, coefficient in projected_normal(tail).items():
                    answer[blocker] -= multiplier * coefficient
            elif tail in blocker_index:
                answer[tail] -= multiplier
        active.remove(row)
        answer = retain(answer)
        memo[row] = answer
        return answer

    columns = []
    word_profiles = Counter()
    for record in page["columns"]:
        word = record["key"].split(":", 1)[0]
        profile = tuple(sorted(Counter(word).values(), reverse=True))
        word_profiles[profile] += 1
        vector = Counter()
        for row_hex, value in record["entries"]:
            row = bytes.fromhex(row_hex)
            if reducible(row):
                for blocker, coefficient in projected_normal(row).items():
                    vector[blocker_index[blocker]] += value * coefficient
            elif row in blocker_index:
                vector[blocker_index[row]] += value
        vector = retain(vector)
        columns.append([vector.get(index, 0) for index in range(28)])
    if mutate:
        columns[0][0] += 1

    basis, nullspace = rref_basis(columns, 28)
    target = [Fraction(*record["target_mass"]) for record in seed["blockers"]]
    candidates = []
    for vector in nullspace:
        pairing = sum(left * right for left, right in zip(vector, target, strict=True))
        integers = primitive(vector)
        candidates.append((pairing != 0, sum(value != 0 for value in integers),
                           max(map(abs, integers)), integers, pairing))
    candidates.sort(key=lambda item: (not item[0], item[1], item[2], item[3]))
    chosen = candidates[0] if candidates else None
    exact_pairings_zero = 0
    if chosen:
        invariant = chosen[3]
        exact_pairings_zero = sum(
            sum(invariant[index] * column[index] for index in range(28)) == 0
            for column in columns)
        require(exact_pairings_zero == 1114, exact_pairings_zero)
        target_pairing = sum(Fraction(invariant[index]) * target[index]
                             for index in range(28))
        require((target_pairing != 0) == chosen[0], (target_pairing, chosen))
    else:
        invariant = []
        target_pairing = Fraction(0)

    type_lines = [
        "index\trow\tnecklace_type\tH_orbit_size\tH_stabilizer_order\tfailure_reason\t"
        "physical_matchings_with_transversal\tfour_cycle_transversals\t"
        "monochromatic_transversals\tmixed_transversals\tliteral_incident_columns"
    ]
    keys = ("index", "row", "necklace_type", "H_orbit_size", "H_stabilizer_order",
            "failure_reason", "physical_matchings_with_transversal", "four_cycle_transversals",
            "monochromatic_transversals", "mixed_transversals", "literal_incident_columns")
    type_lines.extend("\t".join(str(record[key]) for key in keys)
                      for record in classifications)
    types_payload = "\n".join(type_lines) + "\n"
    invariant_lines = ["index\trow\tcoefficient"]
    invariant_lines.extend(f"{index}\t{row.hex()}\t{invariant[index]}"
                           for index, row in enumerate(blockers) if invariant[index])
    invariant_payload = "\n".join(invariant_lines) + "\n"

    necklace_hist = Counter(record["necklace_type"] for record in classifications)
    stabilizer_hist = Counter(record["H_stabilizer_order"] for record in classifications)
    failure_hist = Counter(record["failure_reason"] for record in classifications)
    result = {
        "schema": "orbit0-k16-c6-blocker-types-relative-invariant-v1",
        "status": "EXACT_RELATIVE_INVARIANT" if invariant else "NO_28_ROW_LEFT_KERNEL",
        "signed_counter_bug_guard": (
            "boundary_schur_interface.json is not used because its producer applies "
            "Counter += Counter(), which deletes negative coefficients"
        ),
        "blocker_rows": 28,
        "incident_column_orbits": len(columns),
        "corrected_high_pivot_rows": len(memo),
        "corrected_high_pivot_cycle_histogram": dict(sorted(pivot_count.items())),
        "projected_matrix_rank_Q": len(basis),
        "projected_left_nullity_Q": len(nullspace),
        "necklace_type_histogram": dict(sorted(necklace_hist.items())),
        "stabilizer_order_histogram": dict(sorted(stabilizer_hist.items())),
        "matching_failure_histogram": dict(sorted(failure_hist.items())),
        "incident_source_word_profile_histogram": {
            "+".join(map(str, profile)): count
            for profile, count in sorted(word_profiles.items())
        },
        "chosen_invariant_support": sum(value != 0 for value in invariant),
        "chosen_invariant_max_abs_coefficient": max(map(abs, invariant), default=0),
        "chosen_invariant_target_pairing": [target_pairing.numerator,
                                             target_pairing.denominator],
        "all_incident_column_pairings_zero": exact_pairings_zero,
        "types_tsv_sha256": sha256(types_payload.encode()).hexdigest(),
        "invariant_tsv_sha256": sha256(invariant_payload.encode()).hexdigest(),
        "scope_guard": (
            "This is the exact signed 28-row projection after deterministic c>=7 head "
            "elimination on the frozen one-page incident interface. Any invariant is "
            "relative until the omitted Schur feed/ancestors are included."
        ),
    }
    logical = dict(result)
    result["logical_sha256"] = sha256(
        json.dumps(logical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return result, types_payload, invariant_payload


def main():
    result, types_payload, invariant_payload = build(mutate="--mutate" in sys.argv)
    result_payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if "--verify" in sys.argv:
        require(TYPES.read_text() == types_payload, "types ledger differs")
        require(INVARIANT.read_text() == invariant_payload, "invariant ledger differs")
        require(OUT.read_text() == result_payload, "result differs")
    else:
        TYPES.write_text(types_payload)
        INVARIANT.write_text(invariant_payload)
        OUT.write_text(result_payload)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
