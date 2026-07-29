#!/usr/bin/env python3
"""Independent exact audit of the injective-star/Hessian bridge frontier.

This checker imports neither the primary note nor its executable.  It
reconstructs the deficiency count, the binary clean-cap warning, and the
fourteen-site rational structural countermodel with exact arithmetic.  The
matching coefficients are evaluated by a bit-mask recurrence rather than by
the primary checker's precomputed list of all perfect matchings.
"""

from __future__ import annotations

from collections import Counter, deque
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
from math import ceil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRIMARY_HASHES = {
    "notes/injective-star-hessian-bridge-frontier.md":
        "f49a525ddd7b95b3915c9aaa254c2854f2c3ed15d50cf00127fa3337feb7fa62",
    "computations/verify_injective_star_hessian_bridge_frontier.py":
        "6c5652d05ac4f355b183a725b99c705ed69f3b42464985775805a4dc25679ed8",
}

COLORS = tuple(range(3))
N = 14
SITES = tuple(range(N))
LEFT = tuple(range(7))
RIGHT = tuple(range(7, 14))
SHORES = (LEFT, RIGHT)

Matrix = tuple[tuple[Fraction, ...], ...]
Edge = tuple[int, int]
Matching = tuple[Edge, ...]


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def edge(u: int, v: int) -> Edge:
    return (u, v) if u < v else (v, u)


def transpose(matrix: Matrix) -> Matrix:
    return tuple(tuple(matrix[j][i] for j in range(len(matrix)))
                 for i in range(len(matrix)))


def zero_matrix(size: int = 3) -> Matrix:
    return tuple(tuple(Fraction(0) for _ in range(size)) for _ in range(size))


def matrix_rank(matrix: list[list[Fraction]] | Matrix) -> int:
    rows = [list(row) for row in matrix]
    if not rows:
        return 0
    pivot_row = 0
    for column in range(len(rows[0])):
        pivot = next((row for row in range(pivot_row, len(rows))
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        value = rows[pivot_row][column]
        rows[pivot_row] = [entry / value for entry in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or rows[row][column] == 0:
                continue
            multiple = rows[row][column]
            rows[row] = [entry - multiple * pivot_entry
                         for entry, pivot_entry
                         in zip(rows[row], rows[pivot_row], strict=True)]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivot_row


def determinant_three(matrix: Matrix) -> Fraction:
    return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def audit_frozen_inputs() -> None:
    for relative, expected in PRIMARY_HASHES.items():
        actual = digest(ROOT / relative)
        assert actual == expected, (relative, expected, actual)


def audit_deficiency_ledger() -> None:
    # A bad unordered pair chooses one of its deficient orientations.  This
    # is an injection because two different unordered pairs cannot have the
    # same oriented pair.
    for order in range(10, 62, 2):
        total = order * (order - 1) // 2
        maximum_deficient_directions = 6 * order
        lower = total - maximum_deficient_directions
        assert lower == order * (order - 13) // 2
        if order >= 14:
            assert lower >= 0
            assert ceil(2 * lower / order) == order - 13
    assert 14 * (14 - 13) // 2 == 7
    assert 16 * (16 - 13) // 2 == 24

    # Recheck the integer step in b_r(N-2) <= 6(N-1).
    for order in range(10, 62):
        possible = [b for b in range(order)
                    if b * (order - 2) <= 6 * (order - 1)]
        assert max(possible) == 6


def binary_rank(vectors: set[int] | frozenset[int]) -> int:
    """Rank of vectors encoded as three-bit integers over F_2."""
    basis: dict[int, int] = {}
    for vector in vectors:
        value = vector
        while value:
            pivot = value.bit_length() - 1
            if pivot in basis:
                value ^= basis[pivot]
            else:
                basis[pivot] = value
                break
    return len(basis)


def generated_binary_subspace(generators: tuple[int, ...]) -> frozenset[int]:
    values = {0}
    for generator in generators:
        values |= {value ^ generator for value in tuple(values)}
    return frozenset(values)


def audit_sharper_endpoint_essential_count() -> None:
    # If subspaces L_r span a three-dimensional endpoint space, at most three
    # of them can be essential: choosing x_r outside the span of the others
    # produces an independent family.  Exhaust every set-family of subspaces
    # of F_2^3 as a finite clean-room check of this dimension argument.
    subspaces = sorted({
        generated_binary_subspace(tuple(
            vector for vector in range(8) if mask & (1 << vector)
        ))
        for mask in range(1 << 8)
    }, key=lambda space: (len(space), tuple(space)))
    assert Counter(binary_rank(space) for space in subspaces) == Counter({
        0: 1, 1: 7, 2: 7, 3: 1,
    })
    maximum_essential = 0
    for family_mask in range(1 << len(subspaces)):
        family = [subspaces[index] for index in range(len(subspaces))
                  if family_mask & (1 << index)]
        total_vectors = set().union(*family) if family else {0}
        if binary_rank(total_vectors) != 3:
            continue
        essential = 0
        for omitted in range(len(family)):
            remaining = [family[index] for index in range(len(family))
                         if index != omitted]
            remaining_vectors = set().union(*remaining) if remaining else {0}
            essential += int(binary_rank(remaining_vectors) < 3)
        maximum_essential = max(maximum_essential, essential)
        assert essential <= 3
    assert maximum_essential == 3

    # The mode-u support of a ternary GHZ target is all of V_u, so the
    # incident endpoint subspaces span dimension three.  Summing the
    # essential-neighbour bound over u gives at most 3N deficient directions.
    for order in range(8, 62, 2):
        stronger = order * (order - 1) // 2 - 3 * order
        assert stronger == order * (order - 7) // 2
        assert ceil(2 * stronger / order) == order - 7
        if order >= 14:
            primary = order * (order - 13) // 2
            assert stronger > primary
    assert 14 * (14 - 7) // 2 == 49


def binary_matchings(vertices: tuple[int, ...]) -> tuple[Matching, ...]:
    if not vertices:
        return ((),)
    pivot = vertices[-1]
    output: list[Matching] = []
    for position, partner in enumerate(vertices[:-1]):
        remainder = vertices[:position] + vertices[position + 1:-1]
        for tail in binary_matchings(remainder):
            output.append(tuple(sorted(tail + (edge(pivot, partner),))))
    return tuple(output)


def audit_binary_clean_cap_boundary() -> tuple[tuple[int, int], Fraction]:
    vertices = tuple(range(6))
    colours = (0, 1)
    blocks = {pair: zero_matrix(2) for pair in combinations(vertices, 2)}

    def put(pair: Edge, cells: tuple[tuple[int, int, Fraction | int], ...]) -> None:
        mutable = [list(row) for row in zero_matrix(2)]
        for row, column, value in cells:
            mutable[row][column] = Fraction(value)
        blocks[pair] = tuple(tuple(row) for row in mutable)

    put((0, 1), ((0, 0, 1), (1, 0, 1)))
    put((2, 3), ((0, 0, 1),))
    put((4, 5), ((0, 0, 1),))
    put((1, 3), ((0, 0, 1),))
    put((0, 2), ((1, 0, -1),))
    put((0, 5), ((1, 1, 1),))
    put((1, 2), ((1, 1, 1),))
    put((3, 4), ((1, 1, Fraction(3, 4)),))
    put((0, 4), ((1, 1, Fraction(1, 2)),))
    put((3, 5), ((1, 1, Fraction(1, 2)),))

    matchings = binary_matchings(vertices)
    assert len(matchings) == 15

    def coefficient(word: tuple[int, ...]) -> Fraction:
        return sum(product_for_matching(blocks, matching, word)
                   for matching in matchings)

    for mask in range(1 << 6):
        word = tuple((mask >> site) & 1 for site in vertices)
        target = Fraction(int(word == (0,) * 6 or word == (1,) * 6))
        assert coefficient(word) == target

    deleted = (0, 2)
    internal = tuple(site for site in vertices if site not in deleted)

    def oriented(endpoint: int, neighbour: int) -> Matrix:
        pair = edge(endpoint, neighbour)
        return blocks[pair] if endpoint == pair[0] else transpose(blocks[pair])

    for endpoint in deleted:
        rows: list[list[Fraction]] = []
        for colour in colours:
            row: list[Fraction] = []
            for neighbour in internal:
                row.extend(oriented(endpoint, neighbour)[colour])
            rows.append(row)
        assert matrix_rank(rows) == 2

    # A linear form in (k00,k01,k10,k11) is represented by four entries.
    effective: dict[Edge, list[list[list[Fraction]]]] = {}
    p, q = deleted
    for u, v in combinations(internal, 2):
        cell = [[[Fraction(0) for _ in range(4)] for _ in colours]
                for _ in colours]
        p_u, p_v = oriented(p, u), oriented(p, v)
        q_u, q_v = oriented(q, u), oriented(q, v)
        for x in colours:
            for y in colours:
                for a in colours:
                    for b in colours:
                        variable = 2 * a + b
                        cell[x][y][variable] += (
                            p_u[a][x] * q_v[b][y]
                            + q_u[b][x] * p_v[a][y]
                        )
        effective[(u, v)] = cell

    selected = {1: 1, 3: 0, 4: 1, 5: 1}
    polynomial: Counter[tuple[int, int]] = Counter()
    for matching in binary_matchings(internal):
        first, second = matching
        first_form = effective[first][selected[first[0]]][selected[first[1]]]
        second_form = effective[second][selected[second[0]]][selected[second[1]]]
        for first_variable, first_value in enumerate(first_form):
            for second_variable, second_value in enumerate(second_form):
                polynomial[tuple(sorted((first_variable, second_variable)))] += (
                    first_value * second_value
                )
    polynomial = Counter({term: value for term, value in polynomial.items() if value})
    assert polynomial == Counter({(2, 3): Fraction(1)})

    # The direct block is -e_1 at p tensor e_0 at q, so s=-k10, while
    # retaining both target colours means k00*k11 is nonzero.  The displayed
    # correction k10*k11 can therefore never vanish in the active locus.
    direct = blocks[edge(p, q)]
    assert direct == ((0, 0), (-1, 0))
    return (2, 3), Fraction(1)


def product_for_matching(
    blocks: dict[Edge, Matrix], matching: Matching, word: tuple[int, ...]
) -> Fraction:
    value = Fraction(1)
    for u, v in matching:
        value *= blocks[(u, v)][word[u]][word[v]]
        if value == 0:
            break
    return value


D: Matrix = (
    (Fraction(1), Fraction(1), Fraction(1)),
    (Fraction(1), Fraction(2), Fraction(4)),
    (Fraction(1), Fraction(3), Fraction(9)),
)

CYCLE_EDGES: set[Edge] = set()
for shore in SHORES:
    for index, site in enumerate(shore):
        CYCLE_EDGES.add(edge(site, shore[(index + 1) % 7]))

ANCHORS = tuple(
    frozenset(edge(site, 7 + (site + colour) % 7) for site in LEFT)
    for colour in COLORS
)
ANCHOR_COLOUR = {
    pair: colour for colour, matching in enumerate(ANCHORS) for pair in matching
}


def coordinate_anchor(colour: int) -> Matrix:
    return tuple(tuple(Fraction(int(row == colour == column)) for column in COLORS)
                 for row in COLORS)


def construct_base_blocks() -> dict[Edge, Matrix]:
    blocks: dict[Edge, Matrix] = {}
    for pair in combinations(SITES, 2):
        if pair in CYCLE_EDGES:
            blocks[pair] = D
        elif pair in ANCHOR_COLOUR:
            blocks[pair] = coordinate_anchor(ANCHOR_COLOUR[pair])
        else:
            blocks[pair] = zero_matrix()
    return blocks


def coefficient_by_masks(blocks: dict[Edge, Matrix], word: tuple[int, ...]) -> Fraction:
    @lru_cache(maxsize=None)
    def recurse(mask: int) -> Fraction:
        if mask == 0:
            return Fraction(1)
        low_bit = mask & -mask
        first = low_bit.bit_length() - 1
        remainder = mask ^ low_bit
        total = Fraction(0)
        scan = remainder
        while scan:
            partner_bit = scan & -scan
            partner = partner_bit.bit_length() - 1
            total += (
                blocks[edge(first, partner)][word[first]][word[partner]]
                * recurse(remainder ^ partner_bit)
            )
            scan ^= partner_bit
        return total

    return recurse((1 << len(word)) - 1)


def cycle_histogram() -> Counter[int]:
    support = CYCLE_EDGES | set(ANCHORS[0])

    @lru_cache(maxsize=None)
    def recurse(mask: int) -> tuple[tuple[int, int], ...]:
        if mask == 0:
            return ((0, 1),)
        low_bit = mask & -mask
        first = low_bit.bit_length() - 1
        remainder = mask ^ low_bit
        result: Counter[int] = Counter()
        scan = remainder
        while scan:
            partner_bit = scan & -scan
            partner = partner_bit.bit_length() - 1
            pair = edge(first, partner)
            if pair in support:
                shift = int(pair in CYCLE_EDGES)
                for degree, count in recurse(remainder ^ partner_bit):
                    result[degree + shift] += count
            scan ^= partner_bit
        return tuple(sorted(result.items()))

    return Counter(dict(recurse((1 << N) - 1)))


def normalize_at_site_zero(
    base: dict[Edge, Matrix], denominators: tuple[Fraction, ...]
) -> dict[Edge, Matrix]:
    normalized = dict(base)
    for pair in combinations(SITES, 2):
        if 0 not in pair:
            continue
        matrix = base[pair]
        normalized[pair] = tuple(
            tuple(matrix[row][column] / denominators[row] for column in COLORS)
            for row in COLORS
        )
    return normalized


def oriented(blocks: dict[Edge, Matrix], endpoint: int, neighbour: int) -> Matrix:
    pair = edge(endpoint, neighbour)
    return blocks[pair] if endpoint == pair[0] else transpose(blocks[pair])


def components(vertices: tuple[int, ...], graph_edges: set[Edge]) -> tuple[frozenset[int], ...]:
    adjacency = {site: set() for site in vertices}
    for u, v in graph_edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    unseen = set(vertices)
    output: list[frozenset[int]] = []
    while unseen:
        start = min(unseen)
        unseen.remove(start)
        reached = {start}
        queue = deque([start])
        while queue:
            current = queue.popleft()
            for neighbour in adjacency[current]:
                if neighbour in unseen:
                    unseen.remove(neighbour)
                    reached.add(neighbour)
                    queue.append(neighbour)
        output.append(frozenset(reached))
    return tuple(output)


def all_matchings(vertices: tuple[int, ...]) -> tuple[Matching, ...]:
    # Deliberately pivot on the greatest vertex, unlike the primary checker.
    if not vertices:
        return ((),)
    pivot = vertices[-1]
    output: list[Matching] = []
    for position, partner in enumerate(vertices[:-1]):
        remainder = vertices[:position] + vertices[position + 1:-1]
        for tail in all_matchings(remainder):
            output.append(tuple(sorted(tail + (edge(pivot, partner),))))
    return tuple(output)


def audit_structural_countermodel() -> tuple[dict[Edge, Matrix], tuple[Fraction, ...], tuple[int, ...], Fraction]:
    assert len(CYCLE_EDGES) == 14
    assert len(ANCHOR_COLOUR) == 21
    assert not CYCLE_EDGES.intersection(ANCHOR_COLOUR)
    assert all(len(anchor) == 7 for anchor in ANCHORS)
    assert determinant_three(D) == 2
    assert D != transpose(D)

    base = construct_base_blocks()
    assert cycle_histogram() == Counter({0: 1, 2: 7, 4: 14, 6: 7})
    diagonal = tuple(D[colour][colour] for colour in COLORS)
    denominators = tuple(
        1 + 7 * value**2 + 14 * value**4 + 7 * value**6
        for value in diagonal
    )
    assert denominators == (Fraction(29), Fraction(701), Fraction(3_812_509))
    for colour in COLORS:
        assert coefficient_by_masks(base, (colour,) * N) == denominators[colour]

    blocks = normalize_at_site_zero(base, denominators)
    for colour in COLORS:
        assert coefficient_by_masks(blocks, (colour,) * N) == 1

    # This is a single invertible diagonal change at site zero.  It preserves
    # ranks and row-zero masks while retaining nonsymmetric endpoint order.
    for pair in combinations(SITES, 2):
        if 0 not in pair:
            assert blocks[pair] == base[pair]
    assert oriented(blocks, 0, 1) == blocks[(0, 1)]
    assert oriented(blocks, 1, 0) == transpose(blocks[(0, 1)])
    assert oriented(blocks, 0, 1) != oriented(blocks, 1, 0)
    assert all(entry >= 0 for matrix in blocks.values() for row in matrix for entry in row)

    checked_pairs = 0
    for p, q in combinations(SITES, 2):
        internal = tuple(site for site in SITES if site not in (p, q))
        for endpoint in (p, q):
            aggregate: list[list[Fraction]] = []
            for colour in COLORS:
                row: list[Fraction] = []
                for neighbour in internal:
                    row.extend(oriented(blocks, endpoint, neighbour)[colour])
                aggregate.append(row)
            assert matrix_rank(aggregate) == 3

            retained_anchors = [neighbour for neighbour in internal
                                if edge(endpoint, neighbour) in ANCHOR_COLOUR]
            assert len(retained_anchors) >= 2
            for neighbour in retained_anchors:
                endpoint_block = oriented(blocks, endpoint, neighbour)
                zero_rows = sum(all(entry == 0 for entry in endpoint_block[colour])
                                for colour in COLORS)
                assert zero_rows == 2

        rank_three = {
            pair for pair in combinations(internal, 2)
            if matrix_rank(blocks[pair]) == 3
        }
        assert rank_three == CYCLE_EDGES.intersection(set(combinations(internal, 2)))
        pieces = components(internal, rank_three)
        assert len(pieces) >= 2
        assert any(piece.issubset(LEFT) for piece in pieces)
        assert any(piece.issubset(RIGHT) for piece in pieces)
        checked_pairs += 1
    assert checked_pairs == 91

    mixed_word = tuple(map(int, "01010111010101"))
    assert len(set(mixed_word)) > 1
    mixed_value = coefficient_by_masks(blocks, mixed_word)
    assert mixed_value == Fraction(4, 29)
    assert mixed_value > 0
    return blocks, denominators, mixed_word, mixed_value


def audit_pair_chart_exchange(
    blocks: dict[Edge, Matrix], mixed_word: tuple[int, ...]
) -> tuple[int, int]:
    matchings = all_matchings(SITES)
    assert len(matchings) == 135_135

    def chart(pair: Edge, word: tuple[int, ...]) -> tuple[int, int, Fraction, Fraction]:
        direct_count = 0
        star_count = 0
        direct_value = Fraction(0)
        star_value = Fraction(0)
        for matching in matchings:
            value = product_for_matching(blocks, matching, word)
            if pair in matching:
                direct_count += 1
                direct_value += value
            else:
                # Each deleted endpoint has a unique matching edge and their
                # internal neighbours are distinct.  This is exactly the
                # two-star branch of the pair contraction.
                p, q = pair
                p_edge = next(item for item in matching if p in item)
                q_edge = next(item for item in matching if q in item)
                p_neighbour = p_edge[0] if p_edge[1] == p else p_edge[1]
                q_neighbour = q_edge[0] if q_edge[1] == q else q_edge[1]
                assert p_neighbour != q_neighbour
                star_count += 1
                star_value += value
        return direct_count, star_count, direct_value, star_value

    charts = ((0, 7), (0, 1))
    words = ((0,) * N, (1,) * N, (2,) * N, mixed_word)
    for word in words:
        exact = coefficient_by_masks(blocks, word)
        for pair in charts:
            direct_count, star_count, direct_value, star_value = chart(pair, word)
            assert (direct_count, star_count) == (10_395, 124_740)
            assert direct_value + star_value == exact

    # The overlapping charts are two partitions of the identical set of
    # matching monomials.  Fixing all endpoint colours above is an exact
    # coefficient-level audit of contraction commutation, including the
    # transpose used when a stored block is traversed backwards.
    assert set(matchings) == set(all_matchings(SITES))
    return 10_395, 124_740


def audit_hessian_frontier_bookkeeping() -> None:
    # Once the nonbipartite Hessian theorem bounds each of three nonzero rows
    # by two sites, one endpoint reaches at most six internal sites.
    for internal_size in range(12, 31, 2):
        maximum_union = sum((2, 2, 2))
        assert internal_size - maximum_union == internal_size - 6
        total_order = internal_size + 2
        assert internal_size - 6 == total_order - 8

    # The connected row-full synchronization packages all nine outputs as
    # a_cd Q + t_c u_d R: two output directions versus three independent
    # diagonal target directions.
    assert matrix_rank([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) == 3
    arbitrary_two_output_coordinates = [
        [Fraction(row + column + 1), Fraction((row + 1) * (column + 2))]
        for row in range(3) for column in range(3)
    ]
    assert matrix_rank(arbitrary_two_output_coordinates) <= 2


def main() -> None:
    audit_frozen_inputs()
    audit_deficiency_ledger()
    audit_sharper_endpoint_essential_count()
    defect_term, defect_value = audit_binary_clean_cap_boundary()
    blocks, denominators, mixed_word, mixed_value = audit_structural_countermodel()
    direct, two_star = audit_pair_chart_exchange(blocks, mixed_word)
    audit_hessian_frontier_bookkeeping()
    print("frozen primary inputs: OK")
    print("primary good-pair bound: N(N-13)/2 (valid but nonsharp)")
    print("mode-support sharpening: N(N-7)/2; N=14 gives 49")
    print(f"binary cap defect: variables={defect_term}, coefficient={defect_value}")
    print(f"pure denominators: {tuple(int(value) for value in denominators)}; normalized=1")
    print("all 91 deleted pairs: aggregate ranks 3/3, local zero rows, disconnected G3")
    print(f"mixed residual: {''.join(map(str, mixed_word))} -> {mixed_value}")
    print(f"overlapping chart partitions: {direct} direct + {two_star} two-star")
    print("PASS")


if __name__ == "__main__":
    main()
