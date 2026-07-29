#!/usr/bin/env python3
"""Exact finite search for three-cut high-sector countermodels.

This is a discovery/falsification search, not a Krenn certificate.  It
enumerates unions of three one-factors on eight vertices; the factors may
overlap, in which case their diagonal colour tensors share an edge block.
Each one-factor carries one of the three constant colours.  For
each of the six cuts C_z={z,6,7}, it tests exactly whether

    (T_3,z)^flat | K_U = (iota delta_U) | K_U,

where K_U is the annihilator of the complete cofactor-insertion space.
Every one of the 11,130 normalized factor triples is tested over Q; no modular inference
is used for the upper bound.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations_with_replacement, product


B = tuple(range(8))
S = tuple(range(6))
R = (6, 7)
PRIMES = (32003, 65521)


def edge(a: int, b: int) -> tuple[int, int]:
    return (a, b) if a < b else (b, a)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:]):
        rest = vertices[1:index + 1] + vertices[index + 2:]
        for matching in perfect_matchings(rest):
            yield (edge(first, second),) + matching


ALL_MATCHINGS = tuple(perfect_matchings(B))


def matching_tensor(
    vertices: tuple[int, ...],
    edge_colours: dict[tuple[int, int], int | tuple[int, ...]],
) -> dict[tuple[int, ...], int]:
    positions = {vertex: index for index, vertex in enumerate(vertices)}
    answer: dict[tuple[int, ...], int] = {}
    for matching in perfect_matchings(vertices):
        if any(pair not in edge_colours for pair in matching):
            continue
        choices = [
            value if isinstance(value, tuple) else (value,)
            for value in (edge_colours[pair] for pair in matching)
        ]
        for selected_colours in product(*choices):
            word = [-1] * len(vertices)
            for (a, b), colour in zip(matching, selected_colours):
                word[positions[a]] = colour
                word[positions[b]] = colour
            key = tuple(word)
            answer[key] = answer.get(key, 0) + 1
    return answer


def cofactor_columns(
    u_set: tuple[int, ...],
    edge_colours: dict[tuple[int, int], int | tuple[int, ...]],
) -> list[dict[int, int]]:
    words = tuple(product(range(3), repeat=5))
    index = {word: i for i, word in enumerate(words)}
    columns: list[dict[int, int]] = []
    for hole in u_set:
        remaining = tuple(x for x in u_set if x != hole)
        cofactor = matching_tensor(remaining, edge_colours)
        for colour in range(3):
            column: dict[int, int] = {}
            for h_word, coefficient in cofactor.items():
                assignment = {hole: colour}
                assignment.update(zip(remaining, h_word))
                word = tuple(assignment[x] for x in u_set)
                coordinate = index[word]
                column[coordinate] = column.get(coordinate, 0) + coefficient
            if column:
                columns.append(column)
    return columns


def high_residual_rows(
    z: int,
    edge_colours: dict[tuple[int, int], int | tuple[int, ...]],
) -> list[dict[int, int]]:
    u_set = tuple(x for x in S if x != z)
    c_set = (z, 6, 7)
    u_words = tuple(product(range(3), repeat=5))
    u_index = {word: i for i, word in enumerate(u_words)}
    rows: dict[tuple[int, ...], dict[int, int]] = {}

    left = set(c_set)
    positions = {vertex: vertex for vertex in B}
    for matching in ALL_MATCHINGS:
        if any(pair not in edge_colours for pair in matching):
            continue
        crossings = sum((a in left) != (b in left) for a, b in matching)
        if crossings != 3:
            continue
        choices = [
            value if isinstance(value, tuple) else (value,)
            for value in (edge_colours[pair] for pair in matching)
        ]
        for selected_colours in product(*choices):
            word = [-1] * 8
            for (a, b), colour in zip(matching, selected_colours):
                word[positions[a]] = colour
                word[positions[b]] = colour
            c_word = tuple(word[x] for x in c_set)
            u_word = tuple(word[x] for x in u_set)
            row = rows.setdefault(c_word, {})
            coordinate = u_index[u_word]
            row[coordinate] = row.get(coordinate, 0) + 1

    for colour in range(3):
        c_word = (colour,) * 3
        u_word = (colour,) * 5
        row = rows.setdefault(c_word, {})
        coordinate = u_index[u_word]
        row[coordinate] = row.get(coordinate, 0) - 1
        if row[coordinate] == 0:
            del row[coordinate]
    return [row for row in rows.values() if row]


def modular_basis(
    vectors: list[dict[int, int]], prime: int
) -> dict[int, dict[int, int]]:
    basis: dict[int, dict[int, int]] = {}
    for source in vectors:
        vector = {i: value % prime for i, value in source.items() if value % prime}
        while vector:
            pivot = min(vector)
            if pivot not in basis:
                inverse = pow(vector[pivot], -1, prime)
                vector = {i: value * inverse % prime for i, value in vector.items()}
                basis[pivot] = vector
                break
            coefficient = vector[pivot]
            reducer = basis[pivot]
            for i, value in reducer.items():
                new_value = (vector.get(i, 0) - coefficient * value) % prime
                if new_value:
                    vector[i] = new_value
                elif i in vector:
                    del vector[i]
    return basis


def modular_member(
    source: dict[int, int], basis: dict[int, dict[int, int]], prime: int
) -> bool:
    vector = {i: value % prime for i, value in source.items() if value % prime}
    while vector:
        pivot = min(vector)
        if pivot not in basis:
            return False
        coefficient = vector[pivot]
        for i, value in basis[pivot].items():
            new_value = (vector.get(i, 0) - coefficient * value) % prime
            if new_value:
                vector[i] = new_value
            elif i in vector:
                del vector[i]
    return True


def rational_basis(vectors: list[dict[int, int]]) -> dict[int, dict[int, Fraction]]:
    basis: dict[int, dict[int, Fraction]] = {}
    for source in vectors:
        vector = {i: Fraction(value) for i, value in source.items() if value}
        while vector:
            pivot = min(vector)
            if pivot not in basis:
                scale = vector[pivot]
                vector = {i: value / scale for i, value in vector.items()}
                basis[pivot] = vector
                break
            coefficient = vector[pivot]
            for i, value in basis[pivot].items():
                new_value = vector.get(i, Fraction(0)) - coefficient * value
                if new_value:
                    vector[i] = new_value
                elif i in vector:
                    del vector[i]
    return basis


def rational_member(
    source: dict[int, int], basis: dict[int, dict[int, Fraction]]
) -> bool:
    vector = {i: Fraction(value) for i, value in source.items() if value}
    while vector:
        pivot = min(vector)
        if pivot not in basis:
            return False
        coefficient = vector[pivot]
        for i, value in basis[pivot].items():
            new_value = vector.get(i, Fraction(0)) - coefficient * value
            if new_value:
                vector[i] = new_value
            elif i in vector:
                del vector[i]
    return True


def cut_record(
    z: int,
    edge_colours: dict[tuple[int, int], int | tuple[int, ...]],
    exact: bool = False,
) -> tuple[bool, int]:
    u_set = tuple(x for x in S if x != z)
    columns = cofactor_columns(u_set, edge_colours)
    residual_rows = high_residual_rows(z, edge_colours)
    words = tuple(product(range(3), repeat=5))
    word_index = {word: i for i, word in enumerate(words)}
    constants = [{word_index[(colour,) * 5]: 1} for colour in range(3)]

    if exact:
        basis = rational_basis(columns)
        full = all(rational_member(row, basis) for row in residual_rows)
        augmented = rational_basis(columns + constants)
    else:
        full = True
        ranks = []
        augmented_ranks = []
        for prime in PRIMES:
            basis = modular_basis(columns, prime)
            if not all(modular_member(row, basis, prime) for row in residual_rows):
                full = False
                break
            augmented = modular_basis(columns + constants, prime)
            ranks.append(len(basis))
            augmented_ranks.append(len(augmented))
        if not full:
            return False, 0
        assert len(set(ranks)) == 1 and len(set(augmented_ranks)) == 1
        return True, augmented_ranks[0] - ranks[0]

    return full, len(augmented) - len(basis)


def edge_colour_map(matchings: tuple[tuple[tuple[int, int], ...], ...]):
    result: dict[tuple[int, int], tuple[int, ...]] = {}
    for colour, matching in enumerate(matchings):
        for pair in matching:
            result[pair] = result.get(pair, ()) + (colour,)
    return result


def scan_one(m0: tuple[tuple[int, int], ...]):
    best = -1
    best_records = []
    scanned = 0
    for m1, m2 in combinations_with_replacement(ALL_MATCHINGS, 2):
        scanned += 1
        edge_colours = edge_colour_map((m0, m1, m2))
        records = [cut_record(z, edge_colours, exact=True) for z in S]
        good = tuple(z for z, (full, defect) in enumerate(records) if full and defect)
        if len(good) > best:
            best = len(good)
            best_records = [(m1, m2, good, records)]
        elif len(good) == best:
            best_records.append((m1, m2, good, records))

    return scanned, best, best_records


def main() -> None:
    representatives = (
        ((0, 1), (2, 3), (4, 5), (6, 7)),
        ((0, 6), (1, 7), (2, 3), (4, 5)),
    )
    for m0 in representatives:
        scanned, best, records = scan_one(m0)
        print(f"base={m0} scanned={scanned} max_active_complete_cuts={best}")
        for m1, m2, good, replay in records[:10]:
            print(f"  m1={m1} m2={m2} cuts={good} records={replay}")
        print(f"  maximizing_records={len(records)}")


if __name__ == "__main__":
    main()
