#!/usr/bin/env python3
"""Search for three simultaneous complete five-cut quotient identities.

This is a discovery script.  It starts from the sharp two-cut order-eight
family and appends one arbitrary endpoint-decorated perfect matching.  All
tests are exact modulo a user-selected prime; any hit is intended to be
replayed over Q in a separate verifier.
"""

from __future__ import annotations

import argparse
import random
from functools import lru_cache
from itertools import combinations, combinations_with_replacement, product


B = tuple(range(8))
S = tuple(range(6))
R = (6, 7)
ACTIVE = (2, 3, 4)
BASE = {
    0: ((0, 1), (2, 3), (4, 5), (6, 7)),
    1: ((0, 2), (1, 4), (3, 6), (5, 7)),
    2: ((0, 4), (1, 3), (2, 7), (5, 6)),
}


def edge(a: int, b: int) -> tuple[int, int]:
    return (a, b) if a < b else (b, a)


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index, second in enumerate(vertices[1:]):
        rest = vertices[1:index + 1] + vertices[index + 2:]
        for matching in perfect_matchings(rest):
            answer.append((edge(first, second),) + matching)
    return tuple(answer)


ALL_MATCHINGS = perfect_matchings(B)


def base_cells():
    result = {}
    for colour, matching in BASE.items():
        for a, b in matching:
            result.setdefault((a, b), []).append((colour, colour, 1))
    return result


def augmented_cells(matching, word, weight):
    result = {pair: list(cells) for pair, cells in base_cells().items()}
    for a, b in matching:
        result.setdefault((a, b), []).append((word[a], word[b], weight))
    return result


def minimal_countermodel_cells():
    result = base_cells()
    result.pop((2, 3))
    result.pop((6, 7))
    result.setdefault((2, 5), []).append((0, 0, 1))
    result.setdefault((3, 5), []).append((1, 0, 1))
    return result


def mixed_repair_cells():
    result = minimal_countermodel_cells()
    result.setdefault((2, 3), []).append((2, 1, 1))
    result.setdefault((6, 7), []).append((1, 2, -1))
    return result


def matching_tensor(vertices, cells, prime):
    positions = {vertex: index for index, vertex in enumerate(vertices)}
    answer = {}
    for matching in perfect_matchings(tuple(vertices)):
        choices = [cells.get(pair, ()) for pair in matching]
        if any(not choice for choice in choices):
            continue
        for picked in product(*choices):
            word = [-1] * len(vertices)
            coefficient = 1
            for (a, b), (ca, cb, weight) in zip(matching, picked):
                word[positions[a]] = ca
                word[positions[b]] = cb
                coefficient = coefficient * weight % prime
            key = tuple(word)
            answer[key] = (answer.get(key, 0) + coefficient) % prime
            if not answer[key]:
                del answer[key]
    return answer


def sparse_basis(vectors, prime):
    basis = {}
    for source in vectors:
        vector = {i: value % prime for i, value in source.items() if value % prime}
        while vector:
            pivot = min(vector)
            reducer = basis.get(pivot)
            if reducer is None:
                inv = pow(vector[pivot], -1, prime)
                basis[pivot] = {i: value * inv % prime for i, value in vector.items()}
                break
            coefficient = vector[pivot]
            for i, value in reducer.items():
                new = (vector.get(i, 0) - coefficient * value) % prime
                if new:
                    vector[i] = new
                else:
                    vector.pop(i, None)
    return basis


def member(source, basis, prime):
    vector = {i: value % prime for i, value in source.items() if value % prime}
    while vector:
        pivot = min(vector)
        reducer = basis.get(pivot)
        if reducer is None:
            return False
        coefficient = vector[pivot]
        for i, value in reducer.items():
            new = (vector.get(i, 0) - coefficient * value) % prime
            if new:
                vector[i] = new
            else:
                vector.pop(i, None)
    return True


WORDS5 = tuple(product(range(3), repeat=5))
WORD5_INDEX = {word: index for index, word in enumerate(WORDS5)}


def cut_record(z, cells, prime):
    u_set = tuple(x for x in S if x != z)
    c_set = (z, 6, 7)
    columns = []
    for hole in u_set:
        remaining = tuple(x for x in u_set if x != hole)
        cofactor = matching_tensor(remaining, cells, prime)
        for colour in range(3):
            column = {}
            for hword, coefficient in cofactor.items():
                assignment = {hole: colour}
                assignment.update(zip(remaining, hword))
                word = tuple(assignment[x] for x in u_set)
                index = WORD5_INDEX[word]
                column[index] = (column.get(index, 0) + coefficient) % prime
            if column:
                columns.append(column)
    basis = sparse_basis(columns, prime)

    rows = {}
    left = set(c_set)
    for matching in ALL_MATCHINGS:
        if sum((a in left) != (b in left) for a, b in matching) != 3:
            continue
        choices = [cells.get(pair, ()) for pair in matching]
        if any(not choice for choice in choices):
            continue
        for picked in product(*choices):
            word = [-1] * 8
            coefficient = 1
            for (a, b), (ca, cb, weight) in zip(matching, picked):
                word[a], word[b] = ca, cb
                coefficient = coefficient * weight % prime
            cword = tuple(word[x] for x in c_set)
            uword = tuple(word[x] for x in u_set)
            index = WORD5_INDEX[uword]
            row = rows.setdefault(cword, {})
            row[index] = (row.get(index, 0) + coefficient) % prime
            if not row[index]:
                del row[index]
    for colour in range(3):
        row = rows.setdefault((colour,) * 3, {})
        index = WORD5_INDEX[(colour,) * 5]
        row[index] = (row.get(index, 0) - 1) % prime
        if not row[index]:
            del row[index]
    full = all(member(row, basis, prime) for row in rows.values())
    if not full:
        return False, 0
    constants = [{WORD5_INDEX[(colour,) * 5]: 1} for colour in range(3)]
    augmented = sparse_basis(columns + constants, prime)
    return True, len(augmented) - len(basis)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=100000)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--prime", type=int, default=32003)
    parser.add_argument("--exhaustive", action="store_true")
    parser.add_argument("--single-cells", action="store_true")
    parser.add_argument("--two-cells", action="store_true")
    parser.add_argument("--minimize-found", action="store_true")
    parser.add_argument("--fourth-single-cell", action="store_true")
    parser.add_argument("--fourth-two-cells", action="store_true")
    parser.add_argument("--kill-mixed-single-cell", action="store_true")
    parser.add_argument("--kill-mixed-two-cells", action="store_true")
    parser.add_argument("--fourth-from-repair-single", action="store_true")
    parser.add_argument("--fourth-from-repair-two", action="store_true")
    args = parser.parse_args()
    rng = random.Random(args.seed)

    if args.fourth_from_repair_two:
        pool = tuple(
            (pair, colours, weight)
            for pair in tuple((a, b) for a in B for b in B if a < b)
            for colours in product(range(3), repeat=2)
            for weight in (1, -1)
        )
        best = 3
        for index, (first, second) in enumerate(
            combinations_with_replacement(pool, 2), 1
        ):
            cells = mixed_repair_cells()
            for pair, colours, weight in (first, second):
                cells.setdefault(pair, []).append((colours[0], colours[1], weight))
            preliminary = tuple(cut_record(z, cells, args.prime) for z in ACTIVE)
            if not all(full and defect for full, defect in preliminary):
                continue
            records = tuple(cut_record(z, cells, args.prime) for z in S)
            active = tuple(
                z for z, (full, defect) in enumerate(records) if full and defect
            )
            if len(active) > best:
                best = len(active)
                print(
                    f"index={index} best={best} first={first} second={second} "
                    f"active={active} records={records}",
                    flush=True,
                )
            if len(active) >= 4:
                return
        print(f"done fourth_from_repair_two={index} best={best}")
        return
    if args.fourth_from_repair_single:
        pool = tuple(
            (pair, colours, weight)
            for pair in tuple((a, b) for a in B for b in B if a < b)
            for colours in product(range(3), repeat=2)
            for weight in (1, -1, 2, -2)
        )
        best = 3
        for index, (pair, colours, weight) in enumerate(pool, 1):
            cells = mixed_repair_cells()
            cells.setdefault(pair, []).append((colours[0], colours[1], weight))
            records = tuple(cut_record(z, cells, args.prime) for z in S)
            active = tuple(
                z for z, (full, defect) in enumerate(records) if full and defect
            )
            if len(active) > best:
                best = len(active)
                print(
                    f"index={index} best={best} cell={(pair,colours,weight)} "
                    f"active={active} records={records}",
                    flush=True,
                )
            if len(active) >= 4:
                return
        print(f"done fourth_from_repair_single={index} best={best}")
        return
    if args.kill_mixed_two_cells:
        pool = tuple(
            (pair, colours, weight)
            for pair in tuple((a, b) for a in B for b in B if a < b)
            for colours in product(range(3), repeat=2)
            for weight in (1, -1)
        )
        target_word = (0, 0, 2, 1, 0, 0, 1, 2)
        for index, (first, second) in enumerate(
            combinations_with_replacement(pool, 2), 1
        ):
            cells = minimal_countermodel_cells()
            for pair, colours, weight in (first, second):
                cells.setdefault(pair, []).append((colours[0], colours[1], weight))
            if matching_tensor(B, cells, args.prime).get(target_word, 0):
                continue
            records = tuple(cut_record(z, cells, args.prime) for z in ACTIVE)
            if all(full and defect for full, defect in records):
                all_records = tuple(cut_record(z, cells, args.prime) for z in S)
                print(
                    f"index={index} first={first} second={second} "
                    f"records={all_records} tensor={matching_tensor(B,cells,args.prime)}",
                    flush=True,
                )
                return
        print(f"done kill_mixed_two_cells={index} no_hit=True")
        return
    if args.kill_mixed_single_cell:
        pool = tuple(
            (pair, colours, weight)
            for pair in tuple((a, b) for a in B for b in B if a < b)
            for colours in product(range(3), repeat=2)
            for weight in (1, -1, 2, -2)
        )
        target_word = (0, 0, 2, 1, 0, 0, 1, 2)
        for index, (pair, colours, weight) in enumerate(pool, 1):
            cells = minimal_countermodel_cells()
            cells.setdefault(pair, []).append((colours[0], colours[1], weight))
            if matching_tensor(B, cells, args.prime).get(target_word, 0):
                continue
            records = tuple(cut_record(z, cells, args.prime) for z in ACTIVE)
            if all(full and defect for full, defect in records):
                print(
                    f"index={index} cell={(pair,colours,weight)} records={records} "
                    f"tensor={matching_tensor(B,cells,args.prime)}",
                    flush=True,
                )
                return
        print(f"done kill_mixed_single_cell={index} no_hit=True")
        return
    if args.fourth_two_cells:
        pool = tuple(
            (pair, colours, weight)
            for pair in tuple((a, b) for a in B for b in B if a < b)
            for colours in product(range(3), repeat=2)
            for weight in (1, -1)
        )
        best = 3
        for index, (first, second) in enumerate(
            combinations_with_replacement(pool, 2), 1
        ):
            cells = minimal_countermodel_cells()
            for pair, colours, weight in (first, second):
                cells.setdefault(pair, []).append((colours[0], colours[1], weight))
            preliminary = tuple(cut_record(z, cells, args.prime) for z in ACTIVE)
            if not all(full and defect for full, defect in preliminary):
                continue
            records_for_cuts = tuple(cut_record(z, cells, args.prime) for z in S)
            active = tuple(
                z for z, (full, defect) in enumerate(records_for_cuts)
                if full and defect
            )
            if len(active) > best:
                best = len(active)
                print(
                    f"index={index} best={best} first={first} second={second} "
                    f"active={active} records={records_for_cuts}",
                    flush=True,
                )
            if len(active) >= 4:
                return
        print(f"done fourth_two_cells={index} best={best}")
        return
    if args.fourth_single_cell:
        best = 3
        pool = tuple(
            (pair, colours, weight)
            for pair in tuple((a, b) for a in B for b in B if a < b)
            for colours in product(range(3), repeat=2)
            for weight in (1, -1, 2, -2)
        )
        for index, (pair, colours, weight) in enumerate(pool, 1):
            cells = minimal_countermodel_cells()
            cells.setdefault(pair, []).append((colours[0], colours[1], weight))
            records_for_cuts = tuple(cut_record(z, cells, args.prime) for z in S)
            active = tuple(
                z for z, (full, defect) in enumerate(records_for_cuts)
                if full and defect
            )
            if len(active) > best:
                best = len(active)
                print(
                    f"index={index} best={best} cell={(pair, colours, weight)} "
                    f"active={active} records={records_for_cuts}",
                    flush=True,
                )
            if len(active) >= 4:
                return
        print(f"done fourth_single_cell={index} best={best}")
        return
    if args.minimize_found:
        sources = tuple(
            (pair, (colour, colour, 1))
            for colour, matching in BASE.items()
            for pair in matching
        ) + (
            ((2, 5), (0, 0, 1)),
            ((3, 5), (1, 0, 1)),
        )
        for size in range(1, len(sources) + 1):
            found = []
            for selected in combinations(range(len(sources)), size):
                cells = {}
                for index in selected:
                    pair, cell = sources[index]
                    cells.setdefault(pair, []).append(cell)
                records_for_cuts = tuple(
                    cut_record(z, cells, args.prime) for z in S
                )
                active = tuple(
                    z for z, (full, defect) in enumerate(records_for_cuts)
                    if full and defect
                )
                if len(active) >= 3:
                    found.append((selected, active, records_for_cuts))
                    print(
                        f"size={size} selected={selected} active={active} "
                        f"records={records_for_cuts}",
                        flush=True,
                    )
                    if len(found) >= 10:
                        break
            if found:
                return
        return
    if args.two_cells:
        pool = tuple(
            (pair, colours, weight)
            for pair in tuple((a, b) for a in B for b in B if a < b)
            for colours in product(range(3), repeat=2)
            for weight in (1, -1)
        )
        best = 0
        for index, (first, second) in enumerate(
            combinations_with_replacement(pool, 2), 1
        ):
            cells = base_cells()
            for pair, colours, weight in (first, second):
                cells.setdefault(pair, []).append((colours[0], colours[1], weight))
            preliminary = tuple(cut_record(z, cells, args.prime) for z in (2, 3))
            if not all(full and defect for full, defect in preliminary):
                continue
            records_for_cuts = tuple(cut_record(z, cells, args.prime) for z in S)
            active = tuple(
                z for z, (full, defect) in enumerate(records_for_cuts)
                if full and defect
            )
            if len(active) > best:
                best = len(active)
                print(
                    f"index={index} best={best} first={first} second={second} "
                    f"active={active} records={records_for_cuts}",
                    flush=True,
                )
            if len(active) >= 3:
                return
        print(f"done two_cells={index} best={best}")
        return
    if args.single_cells:
        best = 0
        for index, (pair, colours, weight) in enumerate(
            product(
                tuple((a, b) for a in B for b in B if a < b),
                tuple(product(range(3), repeat=2)),
                (1, -1, 2, -2),
            ),
            1,
        ):
            cells = base_cells()
            cells.setdefault(pair, []).append((colours[0], colours[1], weight))
            records_for_cuts = tuple(cut_record(z, cells, args.prime) for z in S)
            active = tuple(
                z for z, (full, defect) in enumerate(records_for_cuts)
                if full and defect
            )
            if len(active) > best:
                best = len(active)
                print(
                    f"index={index} best={best} pair={pair} colours={colours} "
                    f"weight={weight} active={active} records={records_for_cuts}",
                    flush=True,
                )
            if len(active) >= 3:
                return
        print(f"done single_cells={index} best={best}")
        return
    if args.exhaustive:
        records = (
            (matching, word, weight)
            for matching in ALL_MATCHINGS
            for word in product(range(3), repeat=8)
            for weight in (1, -1)
        )
    else:
        records = (
            (
                rng.choice(ALL_MATCHINGS),
                tuple(rng.randrange(3) for _ in B),
                rng.choice((1, -1, 2, -2)),
            )
            for _ in range(args.trials)
        )

    best = 0
    for index, (matching, word, weight) in enumerate(records, 1):
        if not args.exhaustive and index > args.trials:
            break
        cells = augmented_cells(matching, word, weight)
        records_for_cuts = tuple(cut_record(z, cells, args.prime) for z in S)
        active = tuple(z for z, (full, defect) in enumerate(records_for_cuts) if full and defect)
        if len(active) > best:
            best = len(active)
            print(
                f"index={index} best={best} matching={matching} word={word} "
                f"weight={weight} active={active} records={records_for_cuts}",
                flush=True,
            )
        if len(active) >= 3:
            return
    print(f"done records={index} best={best}")


if __name__ == "__main__":
    main()
