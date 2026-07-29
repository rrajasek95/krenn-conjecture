#!/usr/bin/env python3
"""Clean-room audit of the induced-zero-shore hierarchy.

This file imports neither the primary proof note nor its checker.  It tests
the extremal ledgers, sparse-support implications, zero-shore injectivity,
the two-site coordinate anchor, endpoint ordering, fixed ternary projection,
parallel-edge aggregation, and the exact all-star matching expansion.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations, permutations, product
from math import ceil


Matrix = tuple[tuple[int, ...], ...]


def falling(value: int, length: int) -> int:
    answer = 1
    for offset in range(length):
        answer *= value - offset
    return answer


def odd_double_factorial(value: int) -> int:
    if value <= 1:
        return 1
    answer = 1
    for factor in range(value, 0, -2):
        answer *= factor
    return answer


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple[int, ...]) -> tuple[tuple[tuple[int, int], ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def audit_uniform_thresholds() -> int:
    checked = 0
    for k in range(1, 61):
        for order in range(8, 502, 2):
            if order < 7 * k + 7:
                continue
            fan = order - 7
            claimed_escapes = order - 7 * k - 6
            assert claimed_escapes >= 1
            for regular in range(fan + 1):
                escapes = fan - regular
                if regular <= 7 * k - 1:
                    assert escapes >= claimed_escapes
                else:
                    zero_neighbours = regular - 6
                    assert zero_neighbours >= 7 * k - 6
                    assert ceil(zero_neighbours / 7) >= k
                checked += 1

    # Check the stated first four-vertex boundary separately.
    k = 3
    order = 28
    assert order - 7 * k - 6 == 1
    assert ceil((7 * k - 6) / 7) == k
    return checked


def audit_four_deletion_and_degree_six() -> int:
    universe = tuple(range(8))
    checked = 0
    for support_mask in range(1 << len(universe)):
        support = {x for x in universe if support_mask & (1 << x)}
        for fan_mask in range(1 << len(universe)):
            fan = {x for x in universe if fan_mask & (1 << x)}
            if len(fan) < 4:
                continue
            if all(len(support - {deleted}) <= 2 for deleted in fan):
                assert len(support) <= 2
            checked += 1

    # Three row supports of size at most two can touch at most six blocks.
    row_supports = [
        frozenset(choice)
        for size in range(3)
        for choice in combinations(range(9), size)
    ]
    for first, second, third in product(row_supports, repeat=3):
        assert len(first | second | third) <= 6
        checked += 1
    return checked


def greedy_seven_colouring(adjacency: list[set[int]]) -> list[int]:
    colours: list[int] = []
    for vertex, neighbours in enumerate(adjacency):
        used = {colours[x] for x in neighbours if x < vertex}
        colour = next(c for c in range(7) if c not in used)
        colours.append(colour)
    return colours


def audit_independent_set_bound() -> int:
    checked = 0
    graph_sizes = list(range(1, 64))
    for size in graph_sizes:
        families: list[set[tuple[int, int]]] = []

        # The sharp family: disjoint K7 blocks, with a last partial clique.
        clique_edges = set()
        for start in range(0, size, 7):
            block = range(start, min(start + 7, size))
            clique_edges.update(combinations(block, 2))
        families.append(clique_edges)

        # Three deterministic degree-six circulant/subgraph families.
        for selector in range(3):
            edges = set()
            for left in range(size):
                for distance in (1, 2, 3):
                    right = (left + distance) % size
                    if left == right:
                        continue
                    edge = tuple(sorted((left, right)))
                    if (left * 17 + right * 11 + selector) % 4 != 0:
                        edges.add(edge)
            # Remove edges deterministically until every degree is at most six.
            while True:
                degrees = [0] * size
                for left, right in edges:
                    degrees[left] += 1
                    degrees[right] += 1
                overloaded = next((v for v, degree in enumerate(degrees) if degree > 6), None)
                if overloaded is None:
                    break
                edge = max(edge for edge in edges if overloaded in edge)
                edges.remove(edge)
            families.append(edges)

        for edges in families:
            adjacency = [set() for _ in range(size)]
            for left, right in edges:
                adjacency[left].add(right)
                adjacency[right].add(left)
            assert max(map(len, adjacency), default=0) <= 6
            colours = greedy_seven_colouring(adjacency)
            assert max(colours, default=0) < 7
            for left, right in edges:
                assert colours[left] != colours[right]
            classes = [[v for v, colour in enumerate(colours) if colour == c] for c in range(7)]
            largest = max(classes, key=len)
            assert len(largest) >= ceil(size / 7)
            assert not any(left in largest and right in largest for left, right in edges)
            checked += 1

    # The K7 union attains equality at all multiples of seven.
    for blocks in range(1, 10):
        assert ceil((7 * blocks) / 7) == blocks
    return checked


def zero_matrix(dimension: int) -> list[list[int]]:
    return [[0 for _ in range(dimension)] for _ in range(dimension)]


def add_oriented_cell(
    blocks: dict[tuple[int, int], list[list[int]]],
    left: int,
    left_colour: int,
    right: int,
    right_colour: int,
    value: int,
) -> None:
    if left < right:
        blocks[left, right][left_colour][right_colour] += value
    else:
        blocks[right, left][right_colour][left_colour] += value


def oriented_matrix(
    blocks: dict[tuple[int, int], list[list[int]]], left: int, right: int
) -> list[list[int]]:
    if left < right:
        return [row[:] for row in blocks[left, right]]
    stored = blocks[right, left]
    return [list(row) for row in zip(*stored, strict=True)]


def rank_mod(rows: list[list[int]], prime: int = 101) -> int:
    matrix = [[entry % prime for entry in row] for row in rows]
    if not matrix:
        return 0
    row = 0
    for column in range(len(matrix[0])):
        pivot = next((r for r in range(row, len(matrix)) if matrix[r][column]), None)
        if pivot is None:
            continue
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
        inverse = pow(matrix[row][column], prime - 2, prime)
        matrix[row] = [(entry * inverse) % prime for entry in matrix[row]]
        for other in range(len(matrix)):
            if other == row or not matrix[other][column]:
                continue
            multiple = matrix[other][column]
            matrix[other] = [
                (a - multiple * b) % prime
                for a, b in zip(matrix[other], matrix[row], strict=True)
            ]
        row += 1
        if row == len(matrix):
            break
    return row


def star_rows(
    blocks: dict[tuple[int, int], list[list[int]]],
    endpoint: int,
    neighbours: tuple[int, ...],
) -> list[list[int]]:
    rows = [[] for _ in range(3)]
    for neighbour in neighbours:
        matrix = oriented_matrix(blocks, endpoint, neighbour)
        for colour in range(3):
            rows[colour].extend(matrix[colour])
    return rows


def audit_literal_zero_shore_and_injectivity() -> int:
    sites = tuple(range(12))
    shore = (1, 4, 7, 10)
    complement = tuple(x for x in sites if x not in shore)
    blocks = {edge: zero_matrix(3) for edge in combinations(sites, 2)}

    # Give every named row a one-site coordinate anchor.  Some named sites
    # lie below their anchors and some above, so stored endpoint order flips.
    for position, endpoint in enumerate(shore):
        for colour in range(3):
            anchor = complement[(2 * position + colour) % len(complement)]
            add_oriented_cell(blocks, endpoint, colour, anchor, colour, position + colour + 1)

    for left, right in combinations(shore, 2):
        assert not any(any(row) for row in oriented_matrix(blocks, left, right))

    for endpoint in shore:
        full_neighbours = tuple(x for x in sites if x != endpoint)
        assert rank_mod(star_rows(blocks, endpoint, full_neighbours)) == 3
        assert rank_mod(star_rows(blocks, endpoint, complement)) == 3
        for deleted in shore:
            if deleted == endpoint:
                continue
            pair_star = tuple(x for x in sites if x not in (endpoint, deleted))
            assert rank_mod(star_rows(blocks, endpoint, pair_star)) == 3

        matrix_rows = star_rows(blocks, endpoint, complement)
        for colour, row in enumerate(matrix_rows):
            support = {
                complement[position // 3]
                for position, value in enumerate(row)
                if value
            }
            assert len(support) == 1
            local = row[3 * complement.index(next(iter(support))) :][:3]
            assert local[colour] != 0
            assert all(value == 0 for axis, value in enumerate(local) if axis != colour)
    return len(shore) * (len(shore) - 1)


def projective_lines(prime: int, dimension: int) -> tuple[tuple[int, ...], ...]:
    lines = set()
    for vector in product(range(prime), repeat=dimension):
        if not any(vector):
            continue
        leading = next(value for value in vector if value)
        inverse = pow(leading, prime - 2, prime)
        lines.add(tuple(value * inverse % prime for value in vector))
    return tuple(sorted(lines))


def audit_coordinate_anchor() -> int:
    # A target e_c(a)e_c(b)T lies in
    # p_a tensor (V_b tensor T) + (V_a tensor T) tensor p_b
    # iff one of p_a,p_b is the corresponding coordinate line.
    prime = 5
    endpoint_lines = projective_lines(prime, 3)
    tail_lines = projective_lines(prime, 2)
    tested = 0

    def position(a: int, b: int, tail: int) -> int:
        return (a * 3 + b) * 2 + tail

    for pa, pb in product(endpoint_lines, repeat=2):
        columns = []
        for b, tail in product(range(3), range(2)):
            column = [0] * 18
            for a in range(3):
                column[position(a, b, tail)] = pa[a]
            columns.append(column)
        for a, tail in product(range(3), range(2)):
            column = [0] * 18
            for b in range(3):
                column[position(a, b, tail)] = pb[b]
            columns.append(column)
        base_rank = rank_mod(columns, prime)
        for colour in range(3):
            axis = tuple(int(entry == colour) for entry in range(3))
            for tail_line in tail_lines:
                target = [0] * 18
                for tail, value in enumerate(tail_line):
                    target[position(colour, colour, tail)] = value
                belongs = rank_mod(columns + [target], prime) == base_rank
                assert belongs == (pa == axis or pb == axis)
                tested += 1
    return tested


def canonical_entry(blocks: dict[tuple[int, int], Matrix], i: int, ci: int, j: int, cj: int) -> int:
    if i < j:
        return blocks[i, j][ci][cj]
    return blocks[j, i][cj][ci]


def hafnian_coefficient(
    blocks: dict[tuple[int, int], Matrix], vertices: tuple[int, ...], colours: dict[int, int]
) -> int:
    total = 0
    for matching in perfect_matchings(vertices):
        term = 1
        for left, right in matching:
            term *= canonical_entry(blocks, left, colours[left], right, colours[right])
        total += term
    return total


def make_asymmetric_blocks(order: int, palette: int, zero_shore: frozenset[int]) -> dict[tuple[int, int], Matrix]:
    blocks = {}
    for left, right in combinations(range(order), 2):
        if left in zero_shore and right in zero_shore:
            blocks[left, right] = tuple(tuple(0 for _ in range(palette)) for _ in range(palette))
            continue
        matrix = []
        for a in range(palette):
            row = []
            for b in range(palette):
                raw = (31 * left + 17 * right + 7 * a + 13 * b + 5 * a * b) % 11
                value = raw - 5
                if (left + 2 * right + 3 * a + b) % 7 == 0:
                    value = 0
                row.append(value)
            matrix.append(tuple(row))
        blocks[left, right] = tuple(matrix)
    return blocks


def all_star_coefficient(
    blocks: dict[tuple[int, int], Matrix],
    named: tuple[int, ...],
    colours: dict[int, int],
    order: int,
) -> int:
    complement = tuple(x for x in range(order) if x not in named)
    total = 0
    for images in permutations(complement, len(named)):
        term = 1
        for source, target in zip(named, images, strict=True):
            term *= canonical_entry(
                blocks, source, colours[source], target, colours[target]
            )
        remaining = tuple(x for x in complement if x not in images)
        term *= hafnian_coefficient(blocks, remaining, colours)
        total += term
    return total


def audit_common_power_and_factorial() -> int:
    checked = 0
    # First audit the support count beyond the primary checker's largest order.
    for order in range(2, 15, 2):
        matchings = perfect_matchings(tuple(range(order)))
        for shore_size in range(1, min(5, order // 2) + 1):
            shore = frozenset(range(shore_size))
            survivors = [
                matching
                for matching in matchings
                if all(not (left in shore and right in shore) for left, right in matching)
            ]
            expected = falling(order - shore_size, shore_size) * odd_double_factorial(
                order - 2 * shore_size - 1
            )
            assert len(survivors) == expected
            checked += 1

    # Numeric coefficient audit with signed, zero, asymmetric cells and every
    # numerical ordering of representative shores through h=4.
    order = 8
    representatives = {
        1: (5,),
        2: (1, 6),
        3: (0, 4, 7),
        4: (1, 3, 5, 7),
    }
    complement_patterns = (
        (0, 0, 0, 0, 0, 0, 0),
        (1, 2, 0, 1, 2, 0, 1),
        (2, 1, 2, 0, 1, 0, 2),
    )
    for shore_size, base_named in representatives.items():
        shore_set = frozenset(base_named)
        blocks = make_asymmetric_blocks(order, 3, shore_set)
        for named in permutations(base_named):
            complement = tuple(x for x in range(order) if x not in named)
            for pattern in complement_patterns:
                internal_word = pattern[: len(complement)]
                for named_word in product(range(3), repeat=shore_size):
                    colours = dict(zip(complement, internal_word, strict=True))
                    colours.update(zip(named, named_word, strict=True))
                    full = hafnian_coefficient(blocks, tuple(range(order)), colours)
                    stars = all_star_coefficient(blocks, named, colours, order)
                    assert full == stars
                    checked += 1
    return checked


def multiply_near_top_by_form(
    tensor: dict[tuple[int, ...], int],
    form: dict[int, tuple[int, int, int]],
) -> dict[tuple[int, ...], int]:
    output: dict[tuple[int, ...], int] = {}
    for word, coefficient in tensor.items():
        holes = {site for site, colour in enumerate(word) if colour == -1}
        for site, vector in form.items():
            if site not in holes:
                continue
            for colour, value in enumerate(vector):
                if not value:
                    continue
                filled = list(word)
                filled[site] = colour
                key = tuple(filled)
                output[key] = output.get(key, 0) + coefficient * value
    return {word: coefficient for word, coefficient in output.items() if coefficient}


def cap_tensor_to_ports(
    tensor: dict[tuple[int, ...], int], ports: tuple[int, ...]
) -> dict[tuple[int, ...], int]:
    # The chosen covector is (1,1,1) at every omitted occupied site.
    port_set = set(ports)
    output: dict[tuple[int, ...], int] = {}
    for word, coefficient in tensor.items():
        assert all(word[site] != -1 for site in range(len(word)) if site not in port_set)
        key = tuple(word[site] for site in ports)
        output[key] = output.get(key, 0) + coefficient
    return {word: coefficient for word, coefficient in output.items() if coefficient}


def audit_h_hole_visibility_and_cap() -> int:
    checked = 0
    site_count = 8
    sites = tuple(range(site_count))

    for holes_count in range(1, 5):
        nominal_ports = min(site_count - 2, max(2, 2 * holes_count))
        frames: list[list[dict[int, tuple[int, int, int]]]] = []
        for frame in range(holes_count):
            colour_rows = []
            for colour in range(3):
                first = (2 * frame + colour) % nominal_ports
                second = (2 * frame + colour + 1) % nominal_ports
                colour_rows.append(
                    {
                        first: (
                            1 + frame,
                            colour - frame,
                            2 - colour,
                        ),
                        second: (
                            colour + 1,
                            -1 - frame,
                            1 + colour + frame,
                        ),
                    }
                )
            frames.append(colour_rows)

        ports = tuple(
            sorted(
                {
                    site
                    for frame in frames
                    for row in frame
                    for site in row
                }
            )
        )
        assert holes_count <= len(ports) <= 6 * holes_count

        q_power: dict[tuple[int, ...], int] = {}
        for holes in combinations(sites, holes_count):
            occupied = tuple(site for site in sites if site not in holes)
            for colours in product(range(3), repeat=len(occupied)):
                word = [-1] * site_count
                for site, colour in zip(occupied, colours, strict=True):
                    word[site] = colour
                value = (
                    (-1 if (sum(holes) + sum(colours)) % 2 else 1)
                    * (1 + sum((site + 2) * (colour + 1) for site, colour in zip(occupied, colours, strict=True)))
                )
                if (sum(holes) + 2 * sum(colours)) % 11 == 0:
                    value = 0
                if value:
                    q_power[tuple(word)] = value

        retained = {
            word: value
            for word, value in q_power.items()
            if {site for site, colour in enumerate(word) if colour == -1}.issubset(ports)
        }
        capped_q = cap_tensor_to_ports(retained, ports)

        for colour_word in product(range(3), repeat=holes_count):
            selected_forms = [
                frames[frame][colour]
                for frame, colour in enumerate(colour_word)
            ]

            full_product = q_power
            retained_product = retained
            for form in selected_forms:
                full_product = multiply_near_top_by_form(full_product, form)
                retained_product = multiply_near_top_by_form(retained_product, form)
            assert full_product == retained_product

            capped_full_product = cap_tensor_to_ports(full_product, ports)
            capped_product = capped_q
            local_index = {site: position for position, site in enumerate(ports)}
            for form in selected_forms:
                local_form = {
                    local_index[site]: vector
                    for site, vector in form.items()
                }
                capped_product = multiply_near_top_by_form(capped_product, local_form)
            assert capped_product == capped_full_product
            checked += 1

        # The selected product covector sends every pure diagonal target
        # tensor X_c^D to X_c^P.
        for colour in range(3):
            target = {(colour,) * site_count: 1}
            assert cap_tensor_to_ports(target, ports) == {(colour,) * len(ports): 1}
            checked += 1
    return checked


def audit_parallel_aggregation_and_fixed_projection() -> int:
    order = 6
    full_palette = 5
    selected = (0, 2, 4)
    decorations: dict[tuple[int, int], tuple[Matrix, ...]] = {}
    cancellation_count = 0

    for left, right in combinations(range(order), 2):
        variants = []
        first = []
        second = []
        third = []
        for a in range(full_palette):
            first_row = []
            second_row = []
            third_row = []
            for b in range(full_palette):
                seed = 1 + ((19 * left + 23 * right + 5 * a + 7 * b + a * b) % 9)
                sign = -1 if (left + right + a + 2 * b) % 2 else 1
                value = sign * seed
                first_row.append(value)
                # Force many exact cancellations but leave a nontrivial third summand.
                second_row.append(-value if (left + a + b) % 3 == 0 else 2 * value)
                third_row.append(0 if (right + a + 2 * b) % 4 else -value)
            first.append(tuple(first_row))
            second.append(tuple(second_row))
            third.append(tuple(third_row))
        variants = (tuple(first), tuple(second), tuple(third))
        decorations[left, right] = variants

    aggregate_full: dict[tuple[int, int], Matrix] = {}
    aggregate_projected: dict[tuple[int, int], Matrix] = {}
    for edge, variants in decorations.items():
        matrix = tuple(
            tuple(sum(variant[a][b] for variant in variants) for b in range(full_palette))
            for a in range(full_palette)
        )
        aggregate_full[edge] = matrix
        projected = tuple(tuple(matrix[a][b] for b in selected) for a in selected)
        aggregate_projected[edge] = projected
        for a, b in product(range(full_palette), repeat=2):
            if matrix[a][b] == 0 and any(variant[a][b] for variant in variants):
                cancellation_count += 1
    assert cancellation_count > 0

    matchings = perfect_matchings(tuple(range(order)))
    checked = 0
    for projected_word in product(range(3), repeat=order):
        full_word = tuple(selected[colour] for colour in projected_word)
        full_colours = dict(enumerate(full_word))
        projected_colours = dict(enumerate(projected_word))
        aggregate_value = hafnian_coefficient(
            aggregate_projected, tuple(range(order)), projected_colours
        )
        assert aggregate_value == hafnian_coefficient(
            aggregate_full, tuple(range(order)), full_colours
        )

        decorated_value = 0
        for matching in matchings:
            term_sum = 0
            for variant_choices in product(range(3), repeat=len(matching)):
                term = 1
                for (left, right), choice in zip(matching, variant_choices, strict=True):
                    term *= decorations[left, right][choice][full_colours[left]][full_colours[right]]
                term_sum += term
            decorated_value += term_sum
        assert decorated_value == aggregate_value

        target_full = int(len(set(full_word)) == 1)
        target_projected = int(len(set(projected_word)) == 1)
        assert target_full == target_projected
        checked += 1
    return checked


def main() -> None:
    thresholds = audit_uniform_thresholds()
    supports = audit_four_deletion_and_degree_six()
    graphs = audit_independent_set_bound()
    injections = audit_literal_zero_shore_and_injectivity()
    anchors = audit_coordinate_anchor()
    powers = audit_common_power_and_factorial()
    caps = audit_h_hole_visibility_and_cap()
    projections = audit_parallel_aggregation_and_fixed_projection()
    print(
        "independent induced-zero-shore audit: PASS",
        f"thresholds={thresholds}",
        f"supports={supports}",
        f"graphs={graphs}",
        f"injections={injections}",
        f"anchors={anchors}",
        f"power_cases={powers}",
        f"cap_cases={caps}",
        f"projection_words={projections}",
    )


if __name__ == "__main__":
    main()
