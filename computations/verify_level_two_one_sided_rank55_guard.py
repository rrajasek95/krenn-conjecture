#!/usr/bin/env python3
"""Exact guard for the one-sided rank-55 level-two branch at eight vertices.

Research evidence only.  Krenn's conjecture remains open, SP-CLEAN-BRIDGE is
untouched, and no certified dependency changes.

For one level-two block, write its six residual binary matrices as M, the two
endpoint stars as P,Q, and the rare direct cell as z.  The block equation is

    z Psi(M) + dPsi_M(P_x Q_y^T + Q_x P_y^T) = 0.

Consequently Q=0 and z=0 make all 64 equations vanish for arbitrary M and P.
This checker gives a sharp integral instance with all P_x nonzero, exact
rank(dPsi_M)=55, all 64 entries of Psi(M) nonzero, and the two pure-column
pair-pencil witnesses present at every residual vertex.

The rank proof is exact: five independent integral gauge kernels give the
upper bound 55 over Q, while rank 55 modulo 101 gives a nonzero integer minor
and hence the matching lower bound over Q.  Standard library only; all checks
remain live under python -O and python -I -S.
"""

from itertools import combinations, product


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


SITES = tuple(range(6))
COLOURS = (0, 1)
EDGES = tuple(combinations(SITES, 2))
WORDS = tuple(product(COLOURS, repeat=6))
CELLS = tuple(
    (u, v, a, b)
    for u, v in EDGES
    for a, b in product(COLOURS, repeat=2)
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


def build_internal_packet():
    """A deterministic integral M with two pure-cell one-factors."""

    packet = {}
    for u, v in EDGES:
        for a, b in product(COLOURS, repeat=2):
            if (u, v) in PURE_ZERO:
                value = u + v + 1 if (a, b) == (0, 0) else 0
            elif (u, v) in PURE_ONE:
                value = u + 2 * v + 1 if (a, b) == (1, 1) else 0
            else:
                value = 1 + ((17 * u + 31 * v + 7 * a + 11 * b + 3 * u * v) % 13)
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
    """The 64 by 60 matrix dPsi_M, with cells ordered by CELLS."""

    rows = []
    for word in WORDS:
        row = []
        for u, v, a, b in CELLS:
            if (word[u], word[v]) != (a, b):
                row.append(0)
                continue
            complement = tuple(x for x in SITES if x not in (u, v))
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
        rows[pivot_row] = [(entry * inverse) % prime for entry in rows[pivot_row]]
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
    """Five trace-zero vertex scalings, mu=e_i-e_5."""

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


def oriented_block(packet, root, neighbour):
    if root < neighbour:
        return [
            [packet[root, neighbour, a, b] for b in COLOURS]
            for a in COLOURS
        ]
    return [
        [packet[neighbour, root, b, a] for b in COLOURS]
        for a in COLOURS
    ]


def pure_column(block, output):
    return (
        any(block[row][output] for row in COLOURS)
        and all(
            block[row][column] == 0
            for row in COLOURS
            for column in COLOURS
            if column != output
        )
    )


def audit_rank_and_slope(packet):
    derivative = differential(packet)
    gauges = gauge_vectors(packet)
    require(len(derivative) == 64 and all(len(row) == 60 for row in derivative),
            "wrong differential dimensions")

    base = [hafnian(packet, SITES, word) for word in WORDS]
    for column, cell in enumerate(CELLS):
        bumped = dict(packet)
        bumped[cell] += 1
        difference = [
            hafnian(bumped, SITES, word) - value
            for word, value in zip(WORDS, base)
        ]
        require(difference == [row[column] for row in derivative],
                ("cofactor matrix is not the literal derivative", cell))

    require(all(matrix_vector_product(derivative, gauge) == [0] * 64
                for gauge in gauges),
            "a universal vertex gauge is not in ker dPsi")
    require(rank_mod(gauges) == 5, "the five gauge directions are dependent")
    require(rank_mod(derivative) == 55, "the rank-55 modular minor vanished")

    slope = base
    require(all(value != 0 for value in slope),
            "the advertised everywhere-live slope has acquired a zero")
    return slope


def audit_pair_pencil_witnesses(packet):
    witnesses = {}
    for root in SITES:
        for output, factor in ((0, PURE_ZERO), (1, PURE_ONE)):
            found = [
                neighbour
                for neighbour in SITES
                if neighbour != root
                and pure_column(oriented_block(packet, root, neighbour), output)
            ]
            expected = [
                next(v if u == root else u for u, v in factor if root in (u, v))
            ]
            require(found == expected,
                    ("pure-column witness mismatch", root, output, found, expected))
            edge = tuple(sorted((root, found[0])))
            complement = tuple(x for x in SITES if x not in edge)
            active = any(
                hafnian(packet, complement, word) != 0
                for word in WORDS
            )
            require(active, ("pure witness has zero residual cofactor", edge, output))
            witnesses[root, output] = found[0]
        require(witnesses[root, 0] != witnesses[root, 1],
                ("the two pair-pencil witnesses coincide", root))
    return witnesses


def audit_one_sided_block(packet, slope):
    # X_x=[P_x Q_x] has rank one at every site; Q and z vanish.
    P = [[site + 1, site + 2] for site in SITES]
    Q = [[0, 0] for _site in SITES]
    z = 0
    require(all(any(row) for row in P), "a P row vanished")

    residuals = []
    for word, h_value in zip(WORDS, slope):
        b_value = 0
        for x, y in EDGES:
            n_xy = (
                P[x][word[x]] * Q[y][word[y]]
                + Q[x][word[x]] * P[y][word[y]]
            )
            complement = tuple(site for site in SITES if site not in (x, y))
            b_value += n_xy * hafnian(packet, complement, word)
        residuals.append(z * h_value + b_value)
    require(residuals == [0] * 64,
            "the one-sided packet does not solve its selected block")

    # The same computation in the literal eight-site matching expansion.
    # Sites 6,7 are the rare endpoints, with endpoint 7's selected star zero.
    eight_packet = dict(packet)
    for site in SITES:
        for colour in COLOURS:
            eight_packet[site, 6, colour, 2] = P[site][colour]
            eight_packet[site, 7, colour, 2] = 0
    eight_packet[6, 7, 2, 2] = z
    matchings8 = perfect_matchings(tuple(range(8)))
    for tail in WORDS:
        word = tail + (2, 2)
        total = 0
        for matching in matchings8:
            term = 1
            for u, v in matching:
                term *= eight_packet.get((u, v, word[u], word[v]), 0)
            total += term
        require(total == 0, ("literal selected block is nonzero", word, total))
    return P


def audit_support_completion(packet, P):
    """Unused cells can make the full live graph complete without moving L2."""

    completed = dict(packet)
    for site in SITES:
        for colour in COLOURS:
            completed[site, 6, colour, 2] = P[site][colour]
        # This cell uses colour 2 at the residual site and colour 0 at endpoint
        # 7, so it is invisible when endpoint 7 has rare colour 2 and the tail
        # is binary.
        completed[site, 7, 2, 0] = site + 1
    completed[6, 7, 0, 0] = 1

    live_edges = {
        (u, v)
        for u, v in combinations(range(8), 2)
        if any(key[:2] == (u, v) and value != 0
               for key, value in completed.items())
    }
    require(live_edges == set(combinations(range(8), 2)),
            "the support completion is not K8")

    def value(root, neighbour, root_colour, neighbour_colour):
        if root < neighbour:
            return completed.get(
                (root, neighbour, root_colour, neighbour_colour), 0
            )
        return completed.get(
            (neighbour, root, neighbour_colour, root_colour), 0
        )

    def full_pair_pure(root, neighbour, output):
        return (
            any(value(root, neighbour, row, output) for row in COLOURS)
            and all(
                value(root, neighbour, row, column) == 0
                for row in COLOURS
                for column in (0, 1, 2)
                if column != output
            )
        )

    # This is the literal three-colour R2 alternative at the residual roots,
    # not merely its binary projection.  The P-star puts a nonzero entry in
    # outside column 2, so preservation fails, while the two internal
    # one-factors supply the required pure columns 0 and 1.
    for root in SITES:
        preservation = all(
            value(root, neighbour, row, 2) == 0
            for neighbour in range(8)
            if neighbour != root
            for row in COLOURS
        )
        require(not preservation,
                ("the completed root unexpectedly preserves", root))
        for output in COLOURS:
            pure = [
                neighbour
                for neighbour in range(8)
                if neighbour != root
                and full_pair_pure(root, neighbour, output)
            ]
            require(len(pure) == 1,
                    ("completed R2 pure-witness count", root, output, pure))

    matchings8 = perfect_matchings(tuple(range(8)))
    for tail in WORDS:
        word = tail + (2, 2)
        total = 0
        for matching in matchings8:
            term = 1
            for u, v in matching:
                term *= completed.get((u, v, word[u], word[v]), 0)
            total += term
        require(total == 0, ("support completion moved the selected block", word))
    return len(live_edges)


def main():
    packet = build_internal_packet()
    slope = audit_rank_and_slope(packet)
    witnesses = audit_pair_pencil_witnesses(packet)
    P = audit_one_sided_block(packet, slope)
    live_edges = audit_support_completion(packet, P)
    print(
        "one-sided level-two guard: "
        "rank dPsi=55, slope support=64/64, selected residuals=0/64; "
        f"pair-pencil witnesses={len(witnesses)}, completed live edges={live_edges}/28"
    )


if __name__ == "__main__":
    main()
