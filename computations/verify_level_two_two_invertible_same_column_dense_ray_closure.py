#!/usr/bin/env python3
"""Close the dense same-column 2I+2R+2Z potential ray.

On the potential ray (1,1,1,1,-1,-1), normalize the two invertible endpoint
matrices to I and the two same-column rank-one matrices to e_0 e_0^T.  The
generic-kernel equations then force

    M_01 = J,                  M_it = e_1 e_0^T,
    M_23 = M_45 = 0,

while the eight core-to-zero blocks are arbitrary.

For each zero site z and binary covector q, the tangent

    K_0z = e_1 q^T,   K_1z = -e_1 q^T

lies in the matching differential kernel.  These four directions join the
five trace-zero vertex gauges on a dense open set, giving rank at most 51;
polynomiality extends the bound to every specialization.

Standard library only; checks remain live under python -O and python -I -S.
"""

from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


SITES = tuple(range(6))
COLOURS = (0, 1)
CORE = (0, 1, 2, 3)
ZERO = (4, 5)
EDGES = tuple(combinations(SITES, 2))
CELLS = tuple(
    (u, v, a, b)
    for u, v in EDGES
    for a, b in product(COLOURS, repeat=2)
)
CELL_INDEX = {cell: index for index, cell in enumerate(CELLS)}
J = ((0, 1), (1, 0))
IDENTITY = ((1, 0), (0, 1))
E00 = ((1, 0), (0, 0))
E10 = ((0, 0), (1, 0))
ZERO_MATRIX = ((0, 0), (0, 0))
POTENTIAL = (Q(1, 2),) * 4 + (Q(-1, 2),) * 2
X = {
    0: IDENTITY,
    1: IDENTITY,
    2: E00,
    3: E00,
    4: ZERO_MATRIX,
    5: ZERO_MATRIX,
}


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
    return tuple(zip(*matrix))


def matrix_product(left, right):
    return tuple(
        tuple(
            sum(left[row][middle] * right[middle][column]
                for middle in COLOURS)
            for column in COLOURS
        )
        for row in COLOURS
    )


def add_polynomial(*polynomials):
    answer = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] = answer.get(monomial, Q(0)) + coefficient
            if not answer[monomial]:
                del answer[monomial]
    return answer


def scale_polynomial(coefficient, polynomial):
    return {
        monomial: Q(coefficient) * value
        for monomial, value in polynomial.items()
        if coefficient * value
    }


def multiply_polynomial(left, right):
    answer = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            answer[monomial] = (
                answer.get(monomial, Q(0))
                + left_coefficient * right_coefficient
            )
            if not answer[monomial]:
                del answer[monomial]
    return answer


def constant(value):
    return {(): Q(value)} if value else {}


def variable(name):
    return {(name,): Q(1)}


def normalized_block(pair):
    if pair == (0, 1):
        return J
    if pair in ((0, 2), (0, 3), (1, 2), (1, 3)):
        return E10
    if pair in ((2, 3), (4, 5)):
        return ZERO_MATRIX
    return tuple(
        tuple(variable(f"m{pair[0]}{pair[1]}{a}{b}") for b in COLOURS)
        for a in COLOURS
    )


FORMAL_BLOCKS = {pair: normalized_block(pair) for pair in EDGES}


def formal_value(pair, colours):
    value = FORMAL_BLOCKS[pair][colours[0]][colours[1]]
    return value if isinstance(value, dict) else constant(value)


def formal_hafnian(vertices, word):
    terms = []
    for matching in MATCHINGS[tuple(sorted(vertices))]:
        term = constant(1)
        for pair in matching:
            term = multiply_polynomial(
                term, formal_value(pair, (word[pair[0]], word[pair[1]]))
            )
        terms.append(term)
    return add_polynomial(*terms)


def kernel_tangent(zero, output):
    tangent = {cell: Q(0) for cell in CELLS}
    tangent[0, zero, 1, output] = Q(1)
    tangent[1, zero, 1, output] = Q(-1)
    return tangent


def apply_formal_differential(tangent):
    answer = []
    for word in product(COLOURS, repeat=6):
        terms = []
        for cell, coefficient in tangent.items():
            if not coefficient:
                continue
            u, v, a, b = cell
            if (word[u], word[v]) != (a, b):
                continue
            complement = tuple(site for site in SITES if site not in (u, v))
            terms.append(scale_polynomial(
                coefficient, formal_hafnian(complement, word)
            ))
        answer.append(add_polynomial(*terms))
    return answer


def audit_normal_form():
    checks = 0
    for pair in EDGES:
        numerator = matrix_product(
            matrix_product(X[pair[0]], J),
            transpose(X[pair[1]]),
        )
        block = FORMAL_BLOCKS[pair]
        multiplier = POTENTIAL[pair[0]] + POTENTIAL[pair[1]]
        for a, b in product(COLOURS, repeat=2):
            right = (
                scale_polynomial(multiplier, block[a][b])
                if isinstance(block[a][b], dict)
                else constant(multiplier * block[a][b])
            )
            require(constant(numerator[a][b]) == right,
                    ("normalized generic-kernel equation failed",
                     pair, a, b))
            checks += 1
    require(checks == 60, "normal-form scalar census changed")
    return checks


def audit_universal_kernel():
    directions = []
    identity_checks = 0
    for zero in ZERO:
        for output in COLOURS:
            tangent = kernel_tangent(zero, output)
            image = apply_formal_differential(tangent)
            require(not any(image),
                    ("extra tangent left the formal kernel", zero, output))
            directions.append([tangent[cell] for cell in CELLS])
            identity_checks += len(image)
    require(identity_checks == 4 * 64,
            "universal kernel identity census changed")
    require(rational_rank(directions) == 4,
            "the four extra directions became dependent")
    return directions, identity_checks


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


OPEN_EDGES = ((0, 1), (0, 2), (1, 2), (0, 3), (2, 4), (2, 5))


def audit_dense_open_independence():
    # The unsigned vertex-edge incidence matrix has full rank because these
    # edges form a connected graph containing the odd triangle 0-1-2.
    incidence = [
        [int(vertex in pair) for vertex in SITES]
        for pair in OPEN_EDGES
    ]
    require(rational_rank(incidence) == 6,
            "the dense-open support graph lost full unsigned incidence rank")
    return len(OPEN_EDGES), 6


def build_numeric_packet():
    packet = {}
    for edge_index, pair in enumerate(EDGES):
        block = FORMAL_BLOCKS[pair]
        for a, b in product(COLOURS, repeat=2):
            value = block[a][b]
            if isinstance(value, dict):
                value = 1 + (
                    17 * edge_index + 7 * a + 11 * b
                    + 3 * edge_index * edge_index
                ) % 29
            packet[pair[0], pair[1], a, b] = value
    return packet


def gauge_tangent(packet, mu):
    return [
        (mu[u] + mu[v]) * packet[u, v, a, b]
        for u, v, a, b in CELLS
    ]


def audit_sharp_calibration(extra_directions):
    core = run_path(str(Path(__file__).with_name(
        "verify_level_two_one_sided_overlap_collapse.py"
    )))
    packet = build_numeric_packet()
    derivative = core["differential"](packet)
    gauges = []
    for basis in range(5):
        mu = [0] * 6
        mu[basis] = 1
        mu[5] = -1
        gauge = gauge_tangent(packet, mu)
        require(not any(core["matrix_vector_product"](derivative, gauge)),
                ("vertex gauge left the kernel", basis))
        gauges.append(gauge)

    for index, tangent in enumerate(extra_directions):
        require(not any(core["matrix_vector_product"](derivative, tangent)),
                ("extra calibration tangent left the kernel", index))
    require(rational_rank(gauges + extra_directions) == 9,
            "the nine calibration kernel directions became dependent")

    ranks = (
        rational_rank(derivative),
        core["rank_mod"](derivative, 101),
        core["rank_mod"](derivative, 1_000_003),
    )
    require(ranks == (51, 51, 51),
            ("sharp differential calibration changed", ranks))
    return ranks


def main():
    normal = audit_normal_form()
    directions, identities = audit_universal_kernel()
    open_edges, incidence_rank = audit_dense_open_independence()
    ranks = audit_sharp_calibration(directions)
    print("2I+2R+2Z same-column dense-ray closure: all checks passed")
    print(f"  normalized kernel scalars     : {normal}/60")
    print(f"  universal kernel identities   : {identities}/256")
    print(f"  extra kernel directions       : {len(directions)}")
    print(f"  dense-open incidence edges/rank: {open_edges}/{incidence_rank}")
    print(f"  total independent kernels     : 9")
    print(f"  exact ranks Q/mod primes      : {ranks}")
    print(f"  differential-rank bound       : 51")


if __name__ == "__main__":
    main()
