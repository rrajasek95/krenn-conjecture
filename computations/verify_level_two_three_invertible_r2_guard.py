#!/usr/bin/env python3
"""Exact guard for the 3-invertible/3-singular rank-55 L2 branch.

Research evidence only.  Krenn's conjecture remains open, SP-CLEAN-BRIDGE
is untouched, and no certified dependency changes.

The six residual endpoint-star matrices have ranks (2,2,2,1,0,0).  This
checker gives an integral binary residual packet M and half-integral gauge
parameters nu for which

    X_u J X_v^T = (nu_u + nu_v) M_uv,
    z = -sum(nu) = -1,

the selected 64 level-two equations hold, rank(dPsi_M)=55 exactly, and the
literal R2 pure-column exit is realized at all six residual roots.  At the
two zero-star roots the witnesses are compatible endpoint completions whose
outside-c columns are zero.

This is a selected-block/R2 guard, not a full eight-vertex solution.  It
shows that the generic-kernel equation plus R2 cannot by themselves exclude
the entire three-invertible/three-singular pattern.  Standard library only;
all checks remain live under python -O and python -I -S.
"""

from fractions import Fraction as Q
from itertools import combinations, product


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


SITES = tuple(range(6))
COLOURS = (0, 1)
EDGES = tuple(combinations(SITES, 2))
CELLS = tuple((u, v, a, b) for u, v in EDGES
              for a, b in product(COLOURS, repeat=2))
WORDS = tuple(product(COLOURS, repeat=6))
J = ((0, 1), (1, 0))


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
    return tuple(tuple(matrix[column][row] for column in COLOURS)
                 for row in COLOURS)


def matrix_product(left, right):
    return tuple(
        tuple(sum(left[row][middle] * right[middle][column]
                  for middle in COLOURS)
              for column in COLOURS)
        for row in COLOURS
    )


def determinant(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def matrix_rank(matrix):
    if not any(value for row in matrix for value in row):
        return 0
    return 2 if determinant(matrix) else 1


X = {
    0: ((7, 13), (7, 1)),
    1: ((5, 9), (8, 7)),
    2: ((13, 5), (8, 6)),
    3: ((1, 1), (0, 0)),
    4: ((0, 0), (0, 0)),
    5: ((0, 0), (0, 0)),
}

# rho=2*nu keeps the generic-kernel audit integral.
RHO = (1, 1, 1, 1, -1, -1)
Z = Q(-1)

BLOCKS = {
    (0, 1): ((128, 153), (68, 57)),
    (0, 2): ((204, 146), (48, 50)),
    (0, 3): ((20, 0), (8, 0)),
    (0, 4): ((0, 10), (0, 4)),
    (0, 5): ((9, 3), (5, 3)),
    (1, 2): ((142, 102), (131, 104)),
    (1, 3): ((14, 0), (15, 0)),
    (1, 4): ((0, 13), (0, 2)),
    (1, 5): ((10, 13), (5, 9)),
    (2, 3): ((18, 0), (14, 0)),
    (2, 4): ((0, 12), (0, 13)),
    (2, 5): ((10, 3), (5, 2)),
    (3, 4): ((12, 0), (2, 0)),
    (3, 5): ((0, 11), (0, 6)),
    (4, 5): ((0, 0), (0, 0)),
}


def packet_from_blocks(blocks):
    return {
        (u, v, a, b): blocks[u, v][a][b]
        for u, v in EDGES
        for a, b in product(COLOURS, repeat=2)
    }


M = packet_from_blocks(BLOCKS)


def hafnian(packet, vertices, word):
    vertices = tuple(sorted(vertices))
    total = 0
    for matching in MATCHINGS[vertices]:
        term = 1
        for u, v in matching:
            term *= packet[u, v, word[u], word[v]]
        total += term
    return total


def cofactor(packet, word, u, v):
    remaining = tuple(site for site in SITES if site not in (u, v))
    return hafnian(packet, remaining, word)


def matching_tensor(packet):
    return [hafnian(packet, SITES, word) for word in WORDS]


def apply_differential(packet, tangent):
    answer = []
    for word in WORDS:
        value = 0
        for u, v in EDGES:
            value += tangent[u, v, word[u], word[v]] * cofactor(
                packet, word, u, v
            )
        answer.append(value)
    return answer


def differential_matrix(packet):
    answer = []
    for word in WORDS:
        row = []
        for u, v, a, b in CELLS:
            row.append(
                cofactor(packet, word, u, v)
                if (word[u], word[v]) == (a, b) else 0
            )
        answer.append(row)
    return answer


def rational_rank(matrix):
    rows = [[Q(value) for value in row] for row in matrix]
    rank = 0
    width = len(rows[0]) if rows else 0
    for column in range(width):
        pivot = next((slot for slot in range(rank, len(rows))
                      if rows[slot][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [value / scale for value in rows[rank]]
        for slot in range(len(rows)):
            if slot == rank or not rows[slot][column]:
                continue
            multiple = rows[slot][column]
            rows[slot] = [left - multiple * right
                          for left, right in zip(rows[slot], rows[rank])]
        rank += 1
        if rank == len(rows):
            break
    return rank


def modular_rank(matrix, prime):
    rows = [[value % prime for value in row] for row in matrix]
    rank = 0
    width = len(rows[0]) if rows else 0
    for column in range(width):
        pivot = next((slot for slot in range(rank, len(rows))
                      if rows[slot][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = pow(rows[rank][column], -1, prime)
        rows[rank] = [(value * inverse) % prime for value in rows[rank]]
        for slot in range(len(rows)):
            if slot == rank or not rows[slot][column]:
                continue
            multiple = rows[slot][column]
            rows[slot] = [
                (left - multiple * right) % prime
                for left, right in zip(rows[slot], rows[rank])
            ]
        rank += 1
        if rank == len(rows):
            break
    return rank


def audit_generic_kernel_equation():
    require([matrix_rank(X[site]) for site in SITES] == [2, 2, 2, 1, 0, 0],
            "the endpoint-star rank pattern changed")
    require(sum(Q(value, 2) for value in RHO) == 1,
            "the gauge parameters no longer sum to one")
    require(Z == -sum(Q(value, 2) for value in RHO),
            "z is not minus the gauge-parameter sum")

    n_blocks = {}
    for u, v in EDGES:
        n_block = matrix_product(matrix_product(X[u], J), transpose(X[v]))
        n_blocks[u, v] = n_block
        for a, b in product(COLOURS, repeat=2):
            require(
                2 * n_block[a][b] == (RHO[u] + RHO[v]) * BLOCKS[u, v][a][b],
                ("generic-kernel block equation failed", u, v, a, b),
            )

    n_packet = packet_from_blocks(n_blocks)
    slope = matching_tensor(M)
    d_n = apply_differential(M, n_packet)
    require(all(Z * slope_value + tangent_value == 0
                for slope_value, tangent_value in zip(slope, d_n)),
            "a selected level-two equation failed")
    return slope


def gauge_tangent(mu):
    return {
        (u, v, a, b): (mu[u] + mu[v]) * M[u, v, a, b]
        for u, v in EDGES
        for a, b in product(COLOURS, repeat=2)
    }


def audit_rank_55():
    derivative = differential_matrix(M)
    ranks = (
        rational_rank(derivative),
        modular_rank(derivative, 101),
        modular_rank(derivative, 1_000_003),
    )
    require(ranks == (55, 55, 55), ("differential rank changed", ranks))

    gauge_vectors = []
    for basis in range(5):
        mu = [0] * 6
        mu[basis] = 1
        mu[5] = -1
        tangent = gauge_tangent(mu)
        require(not any(apply_differential(M, tangent)),
                ("a universal gauge direction left the kernel", basis))
        gauge_vectors.append([tangent[cell] for cell in CELLS])
    require(rational_rank(gauge_vectors) == 5,
            "the five displayed gauge directions are dependent")
    return ranks


def orient_internal_block(root, neighbour):
    if root < neighbour:
        return BLOCKS[root, neighbour]
    return transpose(BLOCKS[neighbour, root])


def pure_column(block, output):
    width = len(block[0])
    return (
        any(block[row][output] for row in COLOURS)
        and all(block[row][column] == 0
                for row in COLOURS
                for column in range(width)
                if column != output)
    )


def endpoint_blocks(root):
    if root <= 3:
        # Columns are a,b,c.  The selected outside-c columns are P and Q,
        # the first and second columns of X_root respectively.
        p_block = tuple((0, 0, X[root][row][0]) for row in COLOURS)
        q_block = tuple((0, 0, X[root][row][1]) for row in COLOURS)
        return p_block, q_block
    # At a zero-star root the outside-c columns must vanish.  The unused
    # binary entries can therefore supply literal pure-a and pure-b exits.
    scale = root - 2
    p_block = ((scale, 0, 0), (scale + 1, 0, 0))
    q_block = ((0, scale + 2, 0), (0, scale + 3, 0))
    return p_block, q_block


EXPECTED_INTERNAL_WITNESSES = {
    0: ((3, 0), (4, 1)),
    1: ((3, 0), (4, 1)),
    2: ((3, 0), (4, 1)),
    3: ((4, 0), (5, 1)),
}


def audit_literal_r2():
    witness_table = {}
    for root in SITES:
        p_block, q_block = endpoint_blocks(root)
        require(tuple(p_block[row][2] for row in COLOURS)
                == tuple(X[root][row][0] for row in COLOURS),
                ("p endpoint outside-c column mismatch", root))
        require(tuple(q_block[row][2] for row in COLOURS)
                == tuple(X[root][row][1] for row in COLOURS),
                ("q endpoint outside-c column mismatch", root))

        incident = {
            f"r{neighbour}": orient_internal_block(root, neighbour)
            for neighbour in SITES if neighbour != root
        }
        incident["p"] = p_block
        incident["q"] = q_block
        pure = {
            output: tuple(label for label, block in incident.items()
                          if pure_column(block, output))
            for output in COLOURS
        }
        require(pure[0] and pure[1],
                ("R2 lacks a pure-column exit", root, pure))
        require(any(left != right for left in pure[0] for right in pure[1]),
                ("R2 witnesses are not on distinct edges", root, pure))
        witness_table[root] = pure

        if root in EXPECTED_INTERNAL_WITNESSES:
            for neighbour, output in EXPECTED_INTERNAL_WITNESSES[root]:
                require(f"r{neighbour}" in pure[output],
                        ("planned internal R2 witness vanished",
                         root, neighbour, output, pure))
        else:
            require("p" in pure[0] and "q" in pure[1],
                    ("zero-star endpoint completion vanished", root, pure))
    return witness_table


def main():
    slope = audit_generic_kernel_equation()
    ranks = audit_rank_55()
    witnesses = audit_literal_r2()
    print("three-invertible R2 guard: all checks passed")
    print("  endpoint-star ranks       : 2,2,2,1,0,0")
    print("  generic-kernel parameters : nu=(1,1,1,1,-1,-1)/2, z=-1")
    print("  selected L2 rows          : 64/64 exact")
    print("  differential ranks        : Q=%d, mod101=%d, mod1000003=%d" % ranks)
    print("  slope support             : %d/64" % sum(value != 0 for value in slope))
    print("  literal residual R2 exits : %d/6 roots" % len(witnesses))
    print("  scope                     : selected-block/R2 guard; not a full solution")


if __name__ == "__main__":
    main()
