#!/usr/bin/env python3
"""Close the 1I+5R K1,4 antipodal-pencil residue by a rank-42 bound.

After covariant local output changes, the K1,4 normal form has a five-site
coordinate core C={0,2,3,4,5}: every block internal to C is supported in
the 00 cell.  The five spokes from the remaining hub 1 may be arbitrary.

For the differential of the binary six-site matching map, split output
words by their Hamming weight on C.  Weights zero and one occupy 12 rows,
weight two occupies 20 rows, and weight three can be reached only from the
ten 11 tangent cells on core edges.  No larger weight occurs.  Therefore
rank(dPsi)<=12+20+10=42.  This closes K1,4 without L0, L1, or R2.

Research evidence only.  Standard-library exact arithmetic; all checks
remain live under python -O and python -I -S.
"""

from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, product


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


SITES = tuple(range(6))
COLOURS = (0, 1)
HUB = 1
CORE = (0, 2, 3, 4, 5)
EDGES = tuple(combinations(SITES, 2))
CELLS = tuple(
    (u, v, a, b)
    for u, v in EDGES
    for a, b in product(COLOURS, repeat=2)
)
WORDS = tuple(product(COLOURS, repeat=6))
J = ((Q(0), Q(1)), (Q(1), Q(0)))
E0 = (Q(1), Q(0))
E1 = (Q(0), Q(1))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    head = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        partner = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            answer.append(((head, partner),) + tail)
    return tuple(answer)


MATCHINGS = {
    vertices: perfect_matchings(vertices)
    for size in (0, 2, 4, 6)
    for vertices in combinations(SITES, size)
}


def transpose(matrix):
    return tuple(
        tuple(matrix[column][row] for column in COLOURS)
        for row in COLOURS
    )


def matrix_product(left, right):
    return tuple(
        tuple(
            sum(left[row][middle] * right[middle][column]
                for middle in COLOURS)
            for column in COLOURS
        )
        for row in COLOURS
    )


def determinant(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def matrix_rank(matrix):
    if not any(value for row in matrix for value in row):
        return 0
    return 2 if determinant(matrix) else 1


def outer(left, right):
    return tuple(
        tuple(left[row] * right[column] for column in COLOURS)
        for row in COLOURS
    )


def scale_matrix(coefficient, matrix):
    return tuple(
        tuple(coefficient * matrix[row][column] for column in COLOURS)
        for row in COLOURS
    )


def transform_block(left, block, right):
    return matrix_product(matrix_product(left, block), transpose(right))


def packet_from_blocks(blocks):
    return {
        (u, v, a, b): blocks[u, v][a][b]
        for u, v in EDGES
        for a, b in product(COLOURS, repeat=2)
    }


def hafnian(packet, vertices, word):
    total = Q(0)
    for matching in MATCHINGS[tuple(sorted(vertices))]:
        term = Q(1)
        for u, v in matching:
            term *= packet[u, v, word[u], word[v]]
        total += term
    return total


def matching_tensor(packet):
    return tuple(hafnian(packet, SITES, word) for word in WORDS)


def cofactor(packet, word, u, v):
    remaining = tuple(site for site in SITES if site not in (u, v))
    return hafnian(packet, remaining, word)


def differential_matrix(packet):
    return [
        [
            cofactor(packet, word, u, v)
            if (word[u], word[v]) == (a, b) else Q(0)
            for u, v, a, b in CELLS
        ]
        for word in WORDS
    ]


def apply_differential(packet, tangent):
    return tuple(
        sum(
            tangent[u, v, word[u], word[v]]
            * cofactor(packet, word, u, v)
            for u, v in EDGES
        )
        for word in WORDS
    )


def rational_rank(matrix):
    rows = [[Q(value) for value in row] for row in matrix]
    rank = 0
    width = len(rows[0]) if rows else 0
    for column in range(width):
        pivot = next(
            (row for row in range(rank, len(rows)) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [value / scale for value in rows[rank]]
        for row in range(len(rows)):
            if row == rank or not rows[row][column]:
                continue
            multiple = rows[row][column]
            rows[row] = [
                left - multiple * right
                for left, right in zip(rows[row], rows[rank])
            ]
        rank += 1
    return rank


def modular_rank(matrix, prime):
    rows = [[
        value.numerator * pow(value.denominator, -1, prime) % prime
        if isinstance(value, Q) else value % prime
        for value in row
    ] for row in matrix]
    rank = 0
    width = len(rows[0]) if rows else 0
    for column in range(width):
        pivot = next(
            (row for row in range(rank, len(rows)) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = pow(rows[rank][column], -1, prime)
        rows[rank] = [value * inverse % prime for value in rows[rank]]
        for row in range(len(rows)):
            if row == rank or not rows[row][column]:
                continue
            multiple = rows[row][column]
            rows[row] = [
                (left - multiple * right) % prime
                for left, right in zip(rows[row], rows[rank])
            ]
        rank += 1
    return rank


# ---------------------------------------------------------------------------
# Exact K1,4 generic-kernel packet already in coordinate-core normal form.


NU = (Q(2), Q(1), Q(-1), Q(-1), Q(-1), Q(-1))
B_A = (Q(1), Q(1))
B_B = (Q(1), Q(-1))
X = {
    0: ((Q(-1, 2), Q(1, 2)), (Q(3, 2), Q(3, 2))),
    1: outer(E0, B_A),
    2: outer(E0, B_B),
    3: outer(E0, B_B),
    4: outer(E0, B_B),
    5: outer(E0, B_B),
}
FREE = {
    (1, site): (
        (Q(site), Q(site + 1)),
        (Q(site + 2), Q(site + 3)),
    )
    for site in (2, 3, 4, 5)
}


def build_exact_blocks():
    blocks = {}
    numerators = {}
    for u, v in EDGES:
        numerator = matrix_product(matrix_product(X[u], J), transpose(X[v]))
        numerators[u, v] = numerator
        multiplier = NU[u] + NU[v]
        if multiplier:
            blocks[u, v] = scale_matrix(Q(1, 1) / multiplier, numerator)
        else:
            require(not any(value for row in numerator for value in row),
                    ("a K1,4 zero-multiplier numerator survived", u, v))
            blocks[u, v] = FREE[u, v]
    return blocks, numerators


BLOCKS, NUMERATORS = build_exact_blocks()
PACKET = packet_from_blocks(BLOCKS)


def audit_covariant_normal_form():
    require([matrix_rank(X[site]) for site in SITES] == [2, 1, 1, 1, 1, 1],
            "the 1I+5R endpoint-rank pattern changed")
    require(determinant(X[0]) != 0, "the selected root stopped being invertible")
    require(B_A[0] * B_B[1] + B_A[1] * B_B[0] == 0,
            "the two selected pencil slopes stopped being antipodal")
    require(B_A[0] * B_A[1] and B_B[0] * B_B[1],
            "one antipodal selected pencil became isotropic")

    zero_graph = frozenset(
        edge for edge in EDGES if NU[edge[0]] + NU[edge[1]] == 0
    )
    expected = frozenset((1, site) for site in (2, 3, 4, 5))
    require(zero_graph == expected,
            ("the K1,4 potential graph changed", zero_graph))

    checked = 0
    for u, v in EDGES:
        multiplier = NU[u] + NU[v]
        for a, b in product(COLOURS, repeat=2):
            require(
                NUMERATORS[u, v][a][b]
                == multiplier * BLOCKS[u, v][a][b],
                ("the generic-kernel equation failed", u, v, a, b),
            )
            checked += 1

    e00 = outer(E0, E0)
    for edge in combinations(CORE, 2):
        require(BLOCKS[edge] == e00,
                ("a coordinate-core edge changed", edge, BLOCKS[edge]))
    require(BLOCKS[0, 1] == outer(E1, E0),
            "the fixed hub-root spoke changed")

    # The selected value row follows exactly from
    # N_uv=(nu_u+nu_v)M_uv and z=-sum(nu).
    numerator_packet = packet_from_blocks(NUMERATORS)
    slope = matching_tensor(PACKET)
    response = apply_differential(PACKET, numerator_packet)
    z_value = -sum(NU)
    require(all(z_value * left + right == 0
                for left, right in zip(slope, response)),
            "a selected level-two value row failed")
    return checked, len(zero_graph), sum(value != 0 for value in slope)


# ---------------------------------------------------------------------------
# Uniform coordinate-core image bound.


def base_cell_may_live(edge, word):
    # Broaden the K1,4 normal form: every hub spoke may be arbitrary, while
    # every core-core base edge is supported only in the 00 cell.
    if HUB in edge:
        return True
    return word[edge[0]] == 0 and word[edge[1]] == 0


def cofactor_may_live(tangent_edge, word):
    remaining = tuple(site for site in SITES if site not in tangent_edge)
    return any(
        all(base_cell_may_live(edge, word) for edge in matching)
        for matching in MATCHINGS[remaining]
    )


def audit_coordinate_core_bound():
    counts = Counter()
    live_rows = {weight: set() for weight in range(6)}
    live_cells = {weight: set() for weight in range(6)}

    for cell_index, (u, v, a, b) in enumerate(CELLS):
        for word_index, word in enumerate(WORDS):
            if (word[u], word[v]) != (a, b):
                continue
            if not cofactor_may_live((u, v), word):
                continue
            weight = sum(word[site] for site in CORE)
            counts[weight] += 1
            live_rows[weight].add(word_index)
            live_cells[weight].add(cell_index)

            require(weight <= 3,
                    ("a coordinate-core output reached weight >=4",
                     (u, v, a, b), word))
            if weight == 3:
                require(HUB not in (u, v) and a == 1 and b == 1,
                        ("weight three used a non-core-11 tangent",
                         (u, v, a, b), word))

    require(counts == Counter({0: 30, 1: 110, 2: 140, 3: 60}),
            ("the coordinate-core live-pair census changed", counts))
    require(tuple(len(live_rows[weight]) for weight in range(6))
            == (2, 10, 20, 20, 0, 0),
            ("the coordinate-core live-row census changed", live_rows))
    require(tuple(len(live_cells[weight]) for weight in range(6))
            == (20, 40, 30, 10, 0, 0),
            ("the coordinate-core live-cell census changed", live_cells))

    low_weight_rows = 2 * (1 + len(CORE))
    weight_two_rows = 2 * len(tuple(combinations(CORE, 2)))
    weight_three_columns = len(tuple(combinations(CORE, 2)))
    bound = low_weight_rows + weight_two_rows + weight_three_columns
    require((low_weight_rows, weight_two_rows, weight_three_columns, bound)
            == (12, 20, 10, 42),
            "the coordinate-core rank count changed")
    return counts, (low_weight_rows, weight_two_rows,
                    weight_three_columns, bound)


def audit_sharp_calibration_and_covariance():
    differential = differential_matrix(PACKET)
    ranks = (
        rational_rank(differential),
        modular_rank(differential, 101),
        modular_rank(differential, 1_000_003),
    )
    require(ranks == (42, 42, 42),
            ("the sharp K1,4 calibration rank changed", ranks))

    local = {
        0: ((Q(1), Q(1)), (Q(0), Q(1))),
        1: ((Q(2), Q(1)), (Q(1), Q(1))),
        2: ((Q(1), Q(2)), (Q(1), Q(3))),
        3: ((Q(2), Q(1)), (Q(3), Q(2))),
        4: ((Q(1), Q(-1)), (Q(2), Q(1))),
        5: ((Q(3), Q(1)), (Q(1), Q(1))),
    }
    require(all(determinant(local[site]) != 0 for site in SITES),
            "a covariance calibration basis became singular")
    transformed_blocks = {
        (u, v): transform_block(local[u], BLOCKS[u, v], local[v])
        for u, v in EDGES
    }
    transformed_rank = rational_rank(differential_matrix(
        packet_from_blocks(transformed_blocks)
    ))
    require(transformed_rank == 42,
            "local output covariance changed the differential rank")
    return ranks, transformed_rank


def main():
    normal = audit_covariant_normal_form()
    support = audit_coordinate_core_bound()
    calibration = audit_sharp_calibration_and_covariance()
    print("1I+5R K1,4 coordinate-core closure: passed")
    print(f"  generic-kernel scalars/free edges/slope support: {normal}")
    print(f"  weight live-pair census       : {support[0]}")
    print(f"  image slices and rank bound   : {support[1]}")
    print(f"  sharp ranks/covariant rank    : {calibration}")
    print("  L0/L1/R2 needed              : no")


if __name__ == "__main__":
    main()
