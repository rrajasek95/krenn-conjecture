#!/usr/bin/env python3
"""Exact rank-55 guard on the 1I+5Z generic-kernel/R2 stratum.

Research evidence only.  Krenn's conjecture remains open, SP-CLEAN-BRIDGE is
untouched, and no certified dependency changes.

For one selected level-two block, take endpoint matrices X_0=I_2 and
X_1=...=X_5=0, with every endpoint potential and the direct rare cell zero.
Then X_u J X_v^T=(nu_u+nu_v)M_uv is identically zero on every residual
edge, so the residual binary packet M is arbitrary.  The integral M below
has exact differential rank 55.  At the sole invertible endpoint-matrix
root, its two internal pure-column witnesses give the selected residual R2
exit; at the other five roots the selected pair is preserved.

This audits only the selected block and its six literal residual R2 rows.
It makes no claim about L0, L1, overlapping level-two blocks, other colour
pairs, or a full eight-site source.  Standard library only; all assertions
remain active under python -O and python -I -S.
"""

from itertools import combinations, product


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


SITES = tuple(range(6))
ENDPOINTS = (6, 7)
BINARY = (0, 1)
RARE = 2
EDGES = tuple(combinations(SITES, 2))
WORDS = tuple(product(BINARY, repeat=6))
CELLS = tuple(
    (u, v, a, b)
    for u, v in EDGES
    for a, b in product(BINARY, repeat=2)
)
PURE_ZERO = frozenset(((0, 1), (2, 3), (4, 5)))
PURE_ONE = frozenset(((0, 2), (1, 4), (3, 5)))
PRIME = 101


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    head = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        partner = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            answer.append(((head, partner),) + tail)
    return tuple(answer)


MATCHINGS = {
    vertices: perfect_matchings(vertices)
    for size in (0, 2, 4, 6)
    for vertices in combinations(SITES, size)
}
MATCHINGS_EIGHT = perfect_matchings(tuple(range(8)))


def build_internal_packet():
    """Integral packet with one pure-cell one-factor per binary output."""

    packet = {}
    for u, v in EDGES:
        for a, b in product(BINARY, repeat=2):
            if (u, v) in PURE_ZERO:
                value = u + v + 1 if (a, b) == (0, 0) else 0
            elif (u, v) in PURE_ONE:
                value = u + 2 * v + 1 if (a, b) == (1, 1) else 0
            else:
                value = 1 + (
                    (17 * u + 31 * v + 7 * a + 11 * b + 3 * u * v) % 13
                )
            packet[u, v, a, b] = value
    return packet


def hafnian(packet, vertices, word):
    vertices = tuple(sorted(vertices))
    total = 0
    for matching in MATCHINGS[vertices]:
        term = 1
        for u, v in matching:
            term *= packet[u, v, word[u], word[v]]
        total += term
    return total


def differential(packet):
    rows = []
    for word in WORDS:
        row = []
        for u, v, a, b in CELLS:
            if (word[u], word[v]) != (a, b):
                row.append(0)
                continue
            complement = tuple(site for site in SITES if site not in (u, v))
            row.append(hafnian(packet, complement, word))
        rows.append(row)
    return rows


def matrix_vector_product(matrix, vector):
    return [sum(a * b for a, b in zip(row, vector)) for row in matrix]


def rank_mod(matrix, prime=PRIME):
    rows = [[entry % prime for entry in row] for row in matrix]
    if not rows:
        return 0
    row_count = len(rows)
    column_count = len(rows[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inverse = pow(rows[pivot_row][column], prime - 2, prime)
        rows[pivot_row] = [
            (entry * inverse) % prime for entry in rows[pivot_row]
        ]
        for row in range(row_count):
            if row == pivot_row or not rows[row][column]:
                continue
            factor = rows[row][column]
            rows[row] = [
                (entry - factor * pivot_entry) % prime
                for entry, pivot_entry in zip(rows[row], rows[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def gauge_vectors(packet):
    vectors = []
    for distinguished in range(5):
        mu = [0] * 6
        mu[distinguished] = 1
        mu[5] = -1
        vectors.append(
            [
                (mu[u] + mu[v]) * packet[u, v, a, b]
                for u, v, a, b in CELLS
            ]
        )
    return vectors


def audit_differential(packet):
    derivative = differential(packet)
    require(
        len(derivative) == 64 and all(len(row) == 60 for row in derivative),
        "wrong differential dimensions",
    )

    base = [hafnian(packet, SITES, word) for word in WORDS]
    for column, cell in enumerate(CELLS):
        bumped = dict(packet)
        bumped[cell] += 1
        difference = [
            hafnian(bumped, SITES, word) - value
            for word, value in zip(WORDS, base)
        ]
        require(
            difference == [row[column] for row in derivative],
            ("cofactor matrix is not the literal derivative", cell),
        )

    gauges = gauge_vectors(packet)
    require(
        all(matrix_vector_product(derivative, gauge) == [0] * 64
            for gauge in gauges),
        "a universal vertex gauge left the differential kernel",
    )
    require(rank_mod(gauges) == 5, "the five gauge directions are dependent")
    require(rank_mod(derivative) == 55, "the rank-55 modular minor vanished")
    require(all(value != 0 for value in base), "the selected slope acquired a zero")
    return derivative, base


def endpoint_data():
    # X_x=[P_x Q_x].  Thus X_0=I_2 and every other X_x vanishes.
    p_star = [[1, 0]] + [[0, 0] for _site in range(1, 6)]
    q_star = [[0, 1]] + [[0, 0] for _site in range(1, 6)]
    potentials = [0] * 6
    direct = 0
    return p_star, q_star, potentials, direct


def endpoint_matrix(p_star, q_star, site):
    return [
        [p_star[site][row], q_star[site][row]]
        for row in BINARY
    ]


def determinant(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def audit_endpoint_ranks_and_generic_kernel(packet, p_star, q_star, potentials):
    matrices = [endpoint_matrix(p_star, q_star, site) for site in SITES]
    ranks = []
    for matrix in matrices:
        if determinant(matrix):
            ranks.append(2)
        elif any(entry for row in matrix for entry in row):
            ranks.append(1)
        else:
            ranks.append(0)
    require(ranks == [2, 0, 0, 0, 0, 0], ("wrong endpoint ranks", ranks))

    # Entrywise X_u J X_v^T equals P_u Q_v^T + Q_u P_v^T.
    for u, v in EDGES:
        for a, b in product(BINARY, repeat=2):
            numerator = (
                p_star[u][a] * q_star[v][b]
                + q_star[u][a] * p_star[v][b]
            )
            right = (potentials[u] + potentials[v]) * packet[u, v, a, b]
            require(
                numerator == right,
                ("generic-kernel identity failed", u, v, a, b),
            )
    return tuple(ranks)


def audit_selected_equations(packet, derivative, base, p_star, q_star, direct):
    tangent = []
    for u, v, a, b in CELLS:
        tangent.append(
            p_star[u][a] * q_star[v][b]
            + q_star[u][a] * p_star[v][b]
        )
    require(tangent == [0] * 60, "the endpoint tangent is not identically zero")
    residual = [
        direct * slope + value
        for slope, value in zip(base, matrix_vector_product(derivative, tangent))
    ]
    require(residual == [0] * 64, "a selected differential row is nonzero")

    # Independent literal eight-site matching expansion for this selected block.
    eight_packet = dict(packet)
    for site in SITES:
        for colour in BINARY:
            eight_packet[site, ENDPOINTS[0], colour, RARE] = p_star[site][colour]
            eight_packet[site, ENDPOINTS[1], colour, RARE] = q_star[site][colour]
    eight_packet[ENDPOINTS[0], ENDPOINTS[1], RARE, RARE] = direct
    for tail in WORDS:
        word = tail + (RARE, RARE)
        total = 0
        for matching in MATCHINGS_EIGHT:
            term = 1
            for u, v in matching:
                term *= eight_packet.get((u, v, word[u], word[v]), 0)
            total += term
        require(total == 0, ("literal selected block is nonzero", word, total))
    return eight_packet


def oriented_value(packet, root, neighbour, root_colour, neighbour_colour):
    if root < neighbour:
        return packet.get((root, neighbour, root_colour, neighbour_colour), 0)
    return packet.get((neighbour, root, neighbour_colour, root_colour), 0)


def pure_column(packet, root, neighbour, output):
    return (
        any(oriented_value(packet, root, neighbour, row, output)
            for row in BINARY)
        and all(
            oriented_value(packet, root, neighbour, row, column) == 0
            for row in BINARY
            for column in (0, 1, 2)
            if column != output
        )
    )


def audit_selected_residual_r2(eight_packet):
    audit = {}
    for root in SITES:
        preserves_pair = all(
            oriented_value(eight_packet, root, neighbour, row, RARE) == 0
            for neighbour in range(8)
            if neighbour != root
            for row in BINARY
        )
        witnesses = {}
        for output in BINARY:
            witnesses[output] = tuple(
                neighbour
                for neighbour in range(8)
                if neighbour != root
                and pure_column(eight_packet, root, neighbour, output)
            )

        if root == 0:
            require(not preserves_pair, "the invertible root unexpectedly preserves")
            require(witnesses[0] == (1,), ("wrong pure-zero witness", witnesses))
            require(witnesses[1] == (2,), ("wrong pure-one witness", witnesses))
            require(witnesses[0][0] != witnesses[1][0], "R2 witnesses coincide")
        else:
            require(preserves_pair, ("a zero-star root does not preserve", root))
        audit[root] = (preserves_pair, witnesses)

    # The two witnesses used at root 0 have nonzero complementary cofactors.
    for neighbour, output in ((1, 0), (2, 1)):
        complement = tuple(site for site in SITES if site not in (0, neighbour))
        active = any(
            hafnian(eight_packet, complement, word) != 0
            for word in WORDS
        )
        require(active, ("advertised R2 witness has zero cofactor", neighbour, output))
    return audit


def main():
    packet = build_internal_packet()
    derivative, base = audit_differential(packet)
    p_star, q_star, potentials, direct = endpoint_data()
    ranks = audit_endpoint_ranks_and_generic_kernel(
        packet, p_star, q_star, potentials
    )
    eight_packet = audit_selected_equations(
        packet, derivative, base, p_star, q_star, direct
    )
    r2 = audit_selected_residual_r2(eight_packet)
    print("one-invertible five-zero R2 guard: all checks passed")
    print(f"  endpoint ranks              : {ranks}")
    print("  exact differential rank     : 55")
    print("  generic-kernel identities   : 60/60")
    print("  selected level-two rows     : 64/64")
    print(f"  selected residual R2 rows   : {len(r2)}/6")
    print("  scope                       : selected block/R2 guard only")


if __name__ == "__main__":
    main()
