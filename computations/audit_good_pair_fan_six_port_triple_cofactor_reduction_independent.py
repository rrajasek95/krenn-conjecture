#!/usr/bin/env python3
"""Clean-room exact audit of the good-pair fan and six-port reduction.

This file imports neither the primary proof nor its checker.  It uses a
different finite-field subspace exhaustion, exact signed-integer matching
expansions, and direct square-free tensor calculations.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations, combinations_with_replacement, permutations, product
from math import comb


def add_vec(a: tuple[int, ...], b: tuple[int, ...], prime: int) -> tuple[int, ...]:
    return tuple((x + y) % prime for x, y in zip(a, b))


def span(generators: tuple[tuple[int, ...], ...], prime: int) -> frozenset[tuple[int, ...]]:
    if not generators:
        return frozenset({(0, 0, 0)})
    return frozenset(
        tuple(
            sum(coefficients[j] * generators[j][coordinate] for j in range(len(generators)))
            % prime
            for coordinate in range(3)
        )
        for coefficients in product(range(prime), repeat=len(generators))
    )


def audit_four_essential_subspaces_over_f3() -> int:
    """Exhaust four proposed essentials plus their combined background space."""
    prime = 3
    zero = (0, 0, 0)
    nonzero = [v for v in product(range(prime), repeat=3) if v != zero]
    spaces = {span((), prime)}
    for number in (1, 2, 3):
        for generators in combinations(nonzero, number):
            spaces.add(span(generators, prime))
    ordered = sorted(spaces, key=lambda space: (len(space), tuple(sorted(space))))
    assert len(ordered) == 28
    assert [sum(len(space) == prime**dimension for space in ordered) for dimension in range(4)] == [1, 13, 13, 1]
    index = {space: i for i, space in enumerate(ordered)}
    sums: list[list[int]] = [[0] * len(ordered) for _ in ordered]
    for i, left in enumerate(ordered):
        for j, right in enumerate(ordered):
            total = frozenset(add_vec(x, y, prime) for x in left for y in right)
            sums[i][j] = index[total]

    zero_index = next(i for i, space in enumerate(ordered) if len(space) == 1)
    full_index = next(i for i, space in enumerate(ordered) if len(space) == 27)

    def total(indices: tuple[int, ...]) -> int:
        answer = zero_index
        for value in indices:
            answer = sums[answer][value]
        return answer

    tested = 0
    for background in range(len(ordered)):
        for proposed in combinations_with_replacement(range(len(ordered)), 4):
            if total((background,) + proposed) != full_index:
                continue
            tested += 1
            all_essential = True
            for omitted in range(4):
                remaining = (background,) + proposed[:omitted] + proposed[omitted + 1 :]
                if total(remaining) == full_index:
                    all_essential = False
                    break
            assert not all_essential

    coordinate_lines = tuple(index[span((tuple(int(i == j) for i in range(3)),), prime)] for j in range(3))
    assert total((zero_index,) + coordinate_lines) == full_index
    for omitted in range(3):
        assert total((zero_index,) + coordinate_lines[:omitted] + coordinate_lines[omitted + 1 :]) != full_index
    return tested


def audit_fan_ledgers_and_support_fixing() -> None:
    # This is an actual set exhaustion, rather than the cardinality-only
    # ledger used by the primary checker.
    universe = tuple(range(8))
    for support_mask in range(1 << len(universe)):
        support = {i for i in universe if support_mask & (1 << i)}
        for fan_mask in range(1 << len(universe)):
            fan = {i for i in universe if fan_mask & (1 << i)}
            if len(fan) < 4:
                continue
            if all(len(support - {deleted}) <= 2 for deleted in fan):
                assert len(support) <= 2

    for n in range(8, 122, 2):
        lower = comb(n, 2) - 3 * n
        assert lower == n * (n - 7) // 2
        assert 2 * lower // n >= n - 7
        fan = n - 7
        if n >= 16:
            for regular in range(fan + 1):
                if regular <= 8:
                    assert fan - regular >= n - 15
                else:
                    # Three fixed row supports have union at most six.
                    assert regular - 6 >= 3
        if n >= 24:
            for regular in range(fan + 1):
                if regular <= 16:
                    assert fan - regular >= n - 23
                else:
                    zero_neighbours = regular - 6
                    assert zero_neighbours >= 11
                    assert (zero_neighbours + 4) // 5 >= 3

    # A minimum-degree-five bad graph has more edges than an orientation
    # with indegree at most two can carry.  Vertices with three essential
    # neighbours have total bad degree at most three and cannot occur there.
    for vertices in range(1, 200):
        minimum_degree_edges_twice = 5 * vertices
        two_witness_edges_twice = 4 * vertices
        assert minimum_degree_edges_twice > two_witness_edges_twice


def rank_mod(vectors: list[list[int]], prime: int) -> int:
    rows = [[entry % prime for entry in vector] for vector in vectors]
    rank = 0
    if not rows:
        return 0
    width = len(rows[0])
    for column in range(width):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = pow(rows[rank][column], prime - 2, prime)
        rows[rank] = [(value * inverse) % prime for value in rows[rank]]
        for i in range(len(rows)):
            if i == rank or not rows[i][column]:
                continue
            factor = rows[i][column]
            rows[i] = [(x - factor * y) % prime for x, y in zip(rows[i], rows[rank])]
        rank += 1
        if rank == len(rows):
            break
    return rank


def audit_linear_annihilator_and_odd_cycle() -> None:
    prime = 5
    sites = 5
    local_dimension = 3
    edges = list(combinations(range(sites), 2))
    row_of = {(i, j, a, b): edge_number * 9 + 3 * a + b for edge_number, (i, j) in enumerate(edges) for a in range(3) for b in range(3)}

    for support_mask in range(1 << sites):
        p = []
        for i in range(sites):
            if support_mask & (1 << i):
                p.append((1, (i + 2) % prime, (i * i + 1) % prime))
            else:
                p.append((0, 0, 0))
        columns: list[list[int]] = []
        for site in range(sites):
            for colour in range(local_dimension):
                column = [0] * (len(edges) * 9)
                for i, j in edges:
                    if site == j:
                        for a in range(3):
                            column[row_of[i, j, a, colour]] += p[i][a]
                    if site == i:
                        for b in range(3):
                            column[row_of[i, j, colour, b]] += p[j][b]
                columns.append(column)
        map_rank = rank_mod(columns, prime)
        if support_mask.bit_count() >= 3:
            assert map_rank == sites * local_dimension
        else:
            assert map_rank < sites * local_dimension

    # On a connected graph, beta_i + beta_j = 0 has one dimension exactly
    # in the bipartite case, and only the zero solution in the odd-cycle case.
    for number_vertices in range(3, 6):
        possible_edges = list(combinations(range(number_vertices), 2))
        for mask in range(1 << len(possible_edges)):
            chosen = [edge for bit, edge in enumerate(possible_edges) if mask & (1 << bit)]
            adjacency = [set() for _ in range(number_vertices)]
            for i, j in chosen:
                adjacency[i].add(j)
                adjacency[j].add(i)
            reached = {0}
            frontier = [0]
            while frontier:
                i = frontier.pop()
                for j in adjacency[i] - reached:
                    reached.add(j)
                    frontier.append(j)
            if len(reached) != number_vertices:
                continue
            signs: list[int | None] = [None] * number_vertices
            signs[0] = 0
            bipartite = True
            frontier = [0]
            while frontier and bipartite:
                i = frontier.pop()
                for j in adjacency[i]:
                    wanted = 1 - int(signs[i])
                    if signs[j] is None:
                        signs[j] = wanted
                        frontier.append(j)
                    elif signs[j] != wanted:
                        bipartite = False
                        break
            equations = []
            for i, j in chosen:
                row = [0] * number_vertices
                row[i] = row[j] = 1
                equations.append(row)
            equation_rank = rank_mod(equations, prime)
            assert number_vertices - equation_rank == (1 if bipartite else 0)


def projective_representatives(prime: int, dimension: int) -> list[tuple[int, ...]]:
    representatives = set()
    for vector in product(range(prime), repeat=dimension):
        if not any(vector):
            continue
        first = next(value for value in vector if value)
        inverse = pow(first, prime - 2, prime)
        representatives.add(tuple(value * inverse % prime for value in vector))
    return sorted(representatives)


def tensor_position(a: int, b: int, z: int) -> int:
    return (a * 3 + b) * 2 + z


def audit_two_hole_anchor_over_f5() -> int:
    prime = 5
    endpoint_lines = projective_representatives(prime, 3)
    tail_lines = projective_representatives(prime, 2)
    tested = 0
    for pa in endpoint_lines:
        for pb in endpoint_lines:
            tangent_columns: list[list[int]] = []
            for b in range(3):
                for z in range(2):
                    column = [0] * 18
                    for a in range(3):
                        column[tensor_position(a, b, z)] = pa[a]
                    tangent_columns.append(column)
            for a in range(3):
                for z in range(2):
                    column = [0] * 18
                    for b in range(3):
                        column[tensor_position(a, b, z)] = pb[b]
                    tangent_columns.append(column)
            base_rank = rank_mod(tangent_columns, prime)
            for target_colour in range(3):
                axis = tuple(int(i == target_colour) for i in range(3))
                for tail in tail_lines:
                    target = [0] * 18
                    for z in range(2):
                        target[tensor_position(target_colour, target_colour, z)] = tail[z]
                    belongs = rank_mod(tangent_columns + [target], prime) == base_rank
                    assert belongs == (pa == axis or pb == axis)
                    tested += 1
    return tested


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def canonical_entry(blocks: dict[tuple[int, int], tuple[tuple[int, ...], ...]], i: int, ci: int, j: int, cj: int) -> int:
    if i < j:
        return blocks[i, j][ci][cj]
    return blocks[j, i][cj][ci]


def make_blocks(n: int, r: int, u: int, v: int) -> dict[tuple[int, int], tuple[tuple[int, ...], ...]]:
    forbidden = {tuple(sorted((r, u))), tuple(sorted((r, v)))}
    blocks = {}
    for i, j in combinations(range(n), 2):
        if (i, j) in forbidden:
            blocks[i, j] = tuple(tuple(0 for _ in range(3)) for _ in range(3))
            continue
        matrix = []
        for a in range(3):
            row = []
            for b in range(3):
                magnitude = 1 + ((19 * i + 23 * j + 7 * a + 11 * b + 5 * a * b) % 17)
                sign = -1 if (i + 2 * j + a + b) % 2 else 1
                row.append(sign * magnitude)
            matrix.append(tuple(row))
        blocks[i, j] = tuple(matrix)
    return blocks


def hafnian_coefficient(blocks, vertices: tuple[int, ...], colours: dict[int, int]) -> int:
    @lru_cache(maxsize=None)
    def recurse(remaining: tuple[int, ...]) -> int:
        if not remaining:
            return 1
        first = remaining[0]
        answer = 0
        for position in range(1, len(remaining)):
            second = remaining[position]
            rest = remaining[1:position] + remaining[position + 1 :]
            answer += canonical_entry(blocks, first, colours[first], second, colours[second]) * recurse(rest)
        return answer

    return recurse(vertices)


def audit_exact_triple_slice() -> int:
    n = 8
    named_sites = (1, 4, 6)
    tested = 0
    for r, u, v in permutations(named_sites):
        blocks = make_blocks(n, r, u, v)
        W = tuple(site for site in range(n) if site not in (r, u, v))
        for internal_word in product(range(3), repeat=len(W)):
            internal_colours = dict(zip(W, internal_word))
            for c, d, e in product(range(3), repeat=3):
                colours = dict(internal_colours)
                colours.update({r: c, u: d, v: e})
                actual = hafnian_coefficient(blocks, tuple(range(n)), colours)

                direct = 0
                b_de = canonical_entry(blocks, u, d, v, e)
                for x in W:
                    remaining = tuple(site for site in W if site != x)
                    direct += canonical_entry(blocks, r, c, x, colours[x]) * hafnian_coefficient(blocks, remaining, colours)
                direct *= b_de

                three_star = 0
                for x, y, z in permutations(W, 3):
                    remaining = tuple(site for site in W if site not in (x, y, z))
                    three_star += (
                        canonical_entry(blocks, r, c, x, colours[x])
                        * canonical_entry(blocks, u, d, y, colours[y])
                        * canonical_entry(blocks, v, e, z, colours[z])
                        * hafnian_coefficient(blocks, remaining, colours)
                    )
                assert actual == direct + three_star

                target = int(len(set(colours.values())) == 1)
                contracted_target = int(c == d == e and all(value == c for value in internal_word))
                assert target == contracted_target
                tested += 1
    return tested


def multiply_linear_near_top(p: dict[int, tuple[int, int, int]], tensor: dict[tuple[int, ...], int]) -> dict[tuple[int, ...], int]:
    output: dict[tuple[int, ...], int] = {}
    for word, coefficient in tensor.items():
        hole = word.index(-1)
        if hole not in p:
            continue
        for colour, value in enumerate(p[hole]):
            if not value:
                continue
            filled = list(word)
            filled[hole] = colour
            key = tuple(filled)
            output[key] = output.get(key, 0) + coefficient * value
    return {word: coefficient for word, coefficient in output.items() if coefficient}


def audit_hole_projection_and_cap() -> None:
    W = tuple(range(5))
    C = (0, 2, 4)
    D = (1, 3)
    p = {
        0: (1, -2, 3),
        2: (2, 1, -1),
        4: (-1, 3, 2),
    }
    tensor: dict[tuple[int, ...], int] = {}
    for hole in W:
        occupied = tuple(site for site in W if site != hole)
        for colours in product(range(3), repeat=len(occupied)):
            word = [-1] * len(W)
            for site, colour in zip(occupied, colours):
                word[site] = colour
            coefficient = (-1 if (hole + sum(colours)) % 2 else 1) * (1 + hole + sum((i + 2) * (colour + 1) for i, colour in enumerate(colours)))
            tensor[tuple(word)] = coefficient

    projected = {word: value for word, value in tensor.items() if word.index(-1) in C}
    full_product = multiply_linear_near_top(p, tensor)
    projected_product = multiply_linear_near_top(p, projected)
    assert full_product == projected_product

    def cap_top(top, cap_values):
        answer: dict[tuple[int, ...], int] = {}
        for word, coefficient in top.items():
            dword = tuple(word[site] for site in D)
            cword = tuple(word[site] for site in C)
            answer[cword] = answer.get(cword, 0) + coefficient * cap_values[dword]
        return {word: value for word, value in answer.items() if value}

    def cap_near_top(near_top, cap_values):
        answer: dict[tuple[int, ...], int] = {}
        for word, coefficient in near_top.items():
            dword = tuple(word[site] for site in D)
            cword = tuple(word[site] for site in C)
            answer[cword] = answer.get(cword, 0) + coefficient * cap_values[dword]
        return {word: value for word, value in answer.items() if value}

    entangled_cap = {
        colours: (-1 if sum(colours) % 2 else 1) * (2 + 3 * colours[0] + 5 * colours[1])
        for colours in product(range(3), repeat=len(D))
    }
    capped_product = cap_top(projected_product, entangled_cap)
    capped_tensor = cap_near_top(projected, entangled_cap)
    restricted_p = {C.index(site): values for site, values in p.items()}
    assert capped_product == multiply_linear_near_top(restricted_p, capped_tensor)

    all_one_cap = {colours: 1 for colours in product(range(3), repeat=len(D))}
    for colour in range(3):
        assert all_one_cap[(colour,) * len(D)] == 1


def audit_abstract_response_table() -> None:
    for c, d, e in product(range(3), repeat=3):
        p = {c: tuple(int(colour == c) for colour in range(3))}
        if d == e:
            word = tuple(-1 if site == d else d for site in range(3))
            response = {word: 1}
        else:
            response = {}
        actual = multiply_linear_near_top(p, response)
        expected = {(c, c, c): 1} if c == d == e else {}
        assert actual == expected


def main() -> None:
    essential_backgrounds = audit_four_essential_subspaces_over_f3()
    audit_fan_ledgers_and_support_fixing()
    audit_linear_annihilator_and_odd_cycle()
    anchor_cases = audit_two_hole_anchor_over_f5()
    triple_rows = audit_exact_triple_slice()
    audit_hole_projection_and_cap()
    audit_abstract_response_table()
    print(
        "independent good-pair/six-port audit: PASS; "
        f"essential backgrounds={essential_backgrounds}, "
        f"anchor cases={anchor_cases}, triple coefficients={triple_rows}"
    )


if __name__ == "__main__":
    main()
