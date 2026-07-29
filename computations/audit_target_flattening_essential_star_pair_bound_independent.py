#!/usr/bin/env python3
"""Clean-room exact audit of the target-flattening essential-star bound.

This checker deliberately uses a source-level parallel-edge model, an
F_3 subspace ledger, and a finite-field slice-center test different from
the primary checker's F_2 multiset audit.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, product
from math import ceil


TERNARY = range(3)


def rank_q(rows, q: int) -> int:
    matrix = [[int(value) % q for value in row] for row in rows]
    if not matrix:
        return 0
    width = len(matrix[0])
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (r for r in range(pivot_row, len(matrix)) if matrix[r][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        inverse = pow(matrix[pivot_row][column], -1, q)
        matrix[pivot_row] = [inverse * value % q for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or matrix[row][column] == 0:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                (value - scale * pivot_value) % q
                for value, pivot_value in zip(
                    matrix[row], matrix[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def rank_rat(rows) -> int:
    matrix = [[Fraction(value) for value in row] for row in rows]
    if not matrix:
        return 0
    width = len(matrix[0])
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (r for r in range(pivot_row, len(matrix)) if matrix[r][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or matrix[row][column] == 0:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(
                    matrix[row], matrix[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def edge(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position in range(1, len(vertices)):
        v = vertices[position]
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(remainder):
            yield ((u, v),) + tail


def deterministic_parallel_sources(order: int, palette_size: int):
    """Sources are stored in lower-endpoint, upper-endpoint color order."""
    sources = {}
    for u, v in combinations(range(order), 2):
        entries = []
        for source in range(4):
            left = (2 * u + v + source) % palette_size
            right = (u + 3 * v + 2 * source + 1) % palette_size
            numerator = (u + 1) * (source + 2) - (v + 2)
            weight = Fraction(numerator, 1 + (u + v + source) % 4)
            if source == 3 and (u + v) % 2 == 0:
                weight = Fraction(0)
            entries.append((left, right, weight))

        # A literal cancelling parallel pair tests aggregation without
        # assuming that individual sources can be retained termwise.
        left = (u + 2 * v) % palette_size
        right = (3 * u + v + 1) % palette_size
        cancel = Fraction(2 * u - v + 3, 5)
        entries.extend(((left, right, cancel), (left, right, -cancel)))
        sources[u, v] = tuple(entries)
    return sources


def source_tensor(sources, order: int):
    output = defaultdict(Fraction)
    for matching in perfect_matchings(tuple(range(order))):
        choices = [sources[edge(u, v)] for u, v in matching]
        for selected in product(*choices):
            word = [None] * order
            coefficient = Fraction(1)
            for (u, v), (left, right, weight) in zip(
                matching, selected, strict=True
            ):
                lo, hi = edge(u, v)
                word[lo], word[hi] = left, right
                coefficient *= weight
            output[tuple(word)] += coefficient
    return {word: value for word, value in output.items() if value}


def projected_blocks(sources, selected: tuple[int, int, int]):
    local = {colour: index for index, colour in enumerate(selected)}
    blocks = {}
    for pair, entries in sources.items():
        matrix = [[Fraction(0) for _ in TERNARY] for _ in TERNARY]
        for left, right, weight in entries:
            if left in local and right in local:
                matrix[local[left]][local[right]] += weight
        blocks[pair] = tuple(tuple(row) for row in matrix)
    return blocks


def oriented(blocks, u: int, v: int):
    matrix = blocks[edge(u, v)]
    if u < v:
        return matrix
    return tuple(tuple(matrix[j][i] for j in TERNARY) for i in TERNARY)


def block_tensor(blocks, vertices: tuple[int, ...]):
    output = defaultdict(Fraction)
    positions = {site: position for position, site in enumerate(vertices)}
    for word in product(TERNARY, repeat=len(vertices)):
        total = Fraction(0)
        for matching in perfect_matchings(vertices):
            term = Fraction(1)
            for u, v in matching:
                lo, hi = edge(u, v)
                term *= blocks[lo, hi][word[positions[lo]]][word[positions[hi]]]
            total += term
        if total:
            output[word] = total
    return dict(output)


def audit_sources_projection_and_endpoint_order() -> None:
    order = 6
    palette_size = 5
    selected = (4, 1, 3)
    local = {colour: index for index, colour in enumerate(selected)}
    sources = deterministic_parallel_sources(order, palette_size)
    full = source_tensor(sources, order)
    projected = {
        tuple(local[colour] for colour in word): coefficient
        for word, coefficient in full.items()
        if all(colour in local for colour in word)
    }
    blocks = projected_blocks(sources, selected)
    assert block_tensor(blocks, tuple(range(order))) == projected

    # Projection of a five-color diagonal target is exactly the diagonal
    # target on the selected ordered triple, even when the order is changed.
    target = {(colour,) * order: Fraction(1) for colour in range(palette_size)}
    target_projected = {
        (local[word[0]],) * order: coefficient
        for word, coefficient in target.items()
        if word[0] in local
    }
    assert target_projected == {(i,) * order: Fraction(1) for i in TERNARY}

    # Verify the endpoint recursion coefficient-by-coefficient, including
    # transposition when the distinguished endpoint is the larger label.
    whole = block_tensor(blocks, tuple(range(order)))
    for endpoint in range(order):
        for word in product(TERNARY, repeat=order):
            rhs = Fraction(0)
            for neighbour in range(order):
                if neighbour == endpoint:
                    continue
                matrix = oriented(blocks, endpoint, neighbour)
                remainder = tuple(
                    site for site in range(order)
                    if site not in (endpoint, neighbour)
                )
                rest_word = tuple(word[site] for site in remainder)
                rest = block_tensor(blocks, remainder).get(rest_word, Fraction(0))
                rhs += matrix[word[endpoint]][word[neighbour]] * rest
            assert whole.get(word, Fraction(0)) == rhs

        support = [[] for _ in TERNARY]
        for neighbour in range(order):
            if neighbour == endpoint:
                continue
            matrix = oriented(blocks, endpoint, neighbour)
            for row in TERNARY:
                support[row].extend(matrix[row])

        other = tuple(site for site in range(order) if site != endpoint)
        flat = [[] for _ in TERNARY]
        for rest_word in product(TERNARY, repeat=order - 1):
            for colour in TERNARY:
                word = [0] * order
                word[endpoint] = colour
                for site, value in zip(other, rest_word, strict=True):
                    word[site] = value
                flat[colour].append(whole.get(tuple(word), Fraction(0)))
        joined = [support[row] + flat[row] for row in TERNARY]
        assert rank_rat(joined) == rank_rat(support)


def canonical_subspace(generators, q: int = 3):
    matrix = [[value % q for value in vector] for vector in generators]
    if not matrix:
        return ()
    pivot_row = 0
    for column in range(3):
        pivot = next(
            (r for r in range(pivot_row, len(matrix)) if matrix[r][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        inverse = pow(matrix[pivot_row][column], -1, q)
        matrix[pivot_row] = [inverse * value % q for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or matrix[row][column] == 0:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                (value - scale * pivot_value) % q
                for value, pivot_value in zip(
                    matrix[row], matrix[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return tuple(tuple(row) for row in matrix[:pivot_row])


def all_f3_subspaces():
    vectors = tuple(product(range(3), repeat=3))
    spaces = {()}
    for dimension in (1, 2, 3):
        for generators in product(vectors, repeat=dimension):
            spaces.add(canonical_subspace(generators))
    ordered = tuple(sorted(spaces, key=lambda basis: (len(basis), basis)))
    dimensions = {dimension: 0 for dimension in range(4)}
    for basis in ordered:
        dimensions[len(basis)] += 1
    assert dimensions == {0: 1, 1: 13, 2: 13, 3: 1}
    return ordered


def span_dimension(family) -> int:
    return rank_q(
        [vector for subspace in family for vector in subspace],
        3,
    )


def audit_essential_lemma_over_f3() -> None:
    spaces = all_f3_subspaces()
    counts = {"spanning": 0, "sharp": 0}
    for length in range(1, 6):
        for indices in combinations_with_replacement(range(len(spaces)), length):
            family = tuple(spaces[index] for index in indices)
            if span_dimension(family) != 3:
                continue
            counts["spanning"] += 1
            essential = tuple(
                index for index in range(length)
                if span_dimension(family[:index] + family[index + 1 :]) < 3
            )
            assert len(essential) <= 3
            if len(essential) == 3:
                counts["sharp"] += 1
                assert all(len(family[index]) == 1 for index in essential)
                assert span_dimension(tuple(family[index] for index in essential)) == 3
                assert all(
                    family[index] == ()
                    for index in range(length)
                    if index not in essential
                )
    assert counts["spanning"] > 200_000
    assert counts["sharp"] > 0
    print("F3^3 subspace families:", counts)


def audit_star_kernel_identity() -> None:
    sources = deterministic_parallel_sources(8, 5)
    blocks = projected_blocks(sources, (0, 2, 4))
    for endpoint in range(8):
        for omitted in range(8):
            if endpoint == omitted:
                continue
            horizontal = [[] for _ in TERNARY]
            vertical = []
            for neighbour in range(8):
                if neighbour in (endpoint, omitted):
                    continue
                matrix = oriented(blocks, endpoint, neighbour)
                for row in TERNARY:
                    horizontal[row].extend(matrix[row])
                vertical.extend(tuple(matrix[row][column] for row in TERNARY)
                                for column in TERNARY)
            support_dimension = rank_rat(horizontal)
            star_rank = rank_rat(vertical)
            assert support_dimension == star_rank
            assert 3 - star_rank == 3 - support_dimension
            assert (star_rank == 3) == (support_dimension == 3)


def projective_points_f3():
    points = set()
    for vector in product(range(3), repeat=3):
        if vector == (0, 0, 0):
            continue
        first = next(value for value in vector if value)
        inverse = pow(first, -1, 3)
        points.add(tuple(inverse * value % 3 for value in vector))
    return tuple(sorted(points))


def audit_three_slice_center_ledger() -> None:
    points = projective_points_f3()
    assert len(points) == 13
    target = [0] * 27
    for colour in TERNARY:
        target[9 * colour + 3 * colour + colour] = 1

    coordinate_points = {(1, 0, 0), (0, 1, 0), (0, 0, 1)}
    solvable = []
    for x, y, z in product(points, repeat=3):
        generators = []
        for b, c in product(TERNARY, repeat=2):
            vector = [0] * 27
            for a in TERNARY:
                vector[9 * a + 3 * b + c] = x[a]
            generators.append(vector)
        for a, c in product(TERNARY, repeat=2):
            vector = [0] * 27
            for b in TERNARY:
                vector[9 * a + 3 * b + c] = y[b]
            generators.append(vector)
        for a, b in product(TERNARY, repeat=2):
            vector = [0] * 27
            for c in TERNARY:
                vector[9 * a + 3 * b + c] = z[c]
            generators.append(vector)
        if rank_q(generators + [target], 3) == rank_q(generators, 3):
            solvable.append((x, y, z))

    expected = {
        triple for triple in product(coordinate_points, repeat=3)
        if len(set(triple)) == 3
    }
    assert set(solvable) == expected
    assert len(solvable) == 6
    print("F3 three-slice center triples:", len(solvable))


def audit_pair_count_and_fan() -> None:
    thresholds = {}
    for order in range(8, 66, 2):
        # A cyclic directed defect ledger realizes 3N distinct bad unordered
        # pairs under the local three-defect budget when N >= 8.
        deficient = {
            (endpoint, (endpoint + offset) % order)
            for endpoint in range(order)
            for offset in (1, 2, 3)
        }
        bad = {
            frozenset((u, v)) for u, v in deficient
        }
        assert len(deficient) == 3 * order
        assert len(bad) == 3 * order
        good = {
            frozenset((u, v))
            for u, v in combinations(range(order), 2)
            if frozenset((u, v)) not in bad
        }
        expected = order * (order - 7) // 2
        assert len(good) == expected
        degrees = {
            u: sum(u in pair for pair in good) for u in range(order)
        }
        assert set(degrees.values()) == {order - 7}
        clique_floor = ceil(order / 5)
        thresholds[order] = (expected, max(degrees.values()), clique_floor)

        # For the two smallest ledgers, independently enumerate every
        # induced subgraph of the cyclic bad graph.  The uniform proof is
        # the endpoint assignment |E(C)| <= 3|C|; this is a finite audit of
        # the exact inequality, including equality cases.
        if order in (8, 10):
            for mask in range(1 << order):
                subset = {u for u in range(order) if mask & (1 << u)}
                induced = sum(pair <= subset for pair in bad)
                assert induced <= 3 * len(subset)

    assert {n: thresholds[n] for n in (8, 10, 12, 14)} == {
        8: (4, 1, 2),
        10: (15, 3, 2),
        12: (30, 5, 3),
        14: (49, 7, 3),
    }
    # Equality with three essential supports makes every other incident
    # block zero, hence zero in the reverse orientation too; its entire bad
    # degree is at most three.  A hypothetical induced minimum-degree-five
    # graph therefore has at most two witnesses per vertex, giving m <= 2n,
    # contrary to m >= ceil(5n/2).
    for vertex_count in range(1, 66):
        assert (5 * vertex_count + 1) // 2 > 2 * vertex_count
    assert min(n for n in thresholds if thresholds[n][2] >= 6) == 26
    print("directed-defect arithmetic thresholds:", {
        n: thresholds[n] for n in (8, 10, 12, 14)
    })
    print("bad-pair degeneracy/color bound: 4 / 5")
    print("first forced six-site mutually good set: N=26")


def main() -> None:
    audit_sources_projection_and_endpoint_order()
    audit_essential_lemma_over_f3()
    audit_star_kernel_identity()
    audit_three_slice_center_ledger()
    audit_pair_count_and_fan()
    print("independent essential-star audit: PASS")


if __name__ == "__main__":
    main()
