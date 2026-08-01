#!/usr/bin/env python3
"""Exact audit of the overlap collapse for a one-sided level-two block.

Research evidence only.  Krenn's conjecture remains open, SP-CLEAN-BRIDGE is
untouched, and no certified dependency changes.

Let p,q carry the rare colour c, let R be the six residual vertices, and put

    P_x = A_px[c,{a,b}],  Q_x = A_qx[c,{a,b}],

with binary residual packet M.  On the one-sided locus Q=0 and
A_pq[c,c]=0, the L1 rows first kill the other two entries in the c-column of
A_pq.  If alpha_r=A_qr[c,c] is nonzero, the rows with p,q,r all coloured c
then impose the five-site cofactor equation Phi_r(P)=0.

On the rank-55 generic-kernel branch, a connected nonbipartite deletion graph
makes Phi_r injective on the five star sites away from r.  Thus two live
alpha anchors force P=0.  One live anchor also cannot support P != 0 when all
four-site binary cofactors are live: the rows with p,q,r,x all coloured c
kill every A_px[c,c], contradicting the pure-c target row.  Consequently the
full equations collapse the cofactor-open one-sided branch to P=Q=0.

This checker verifies every matching-factorization identity and all open
hypotheses on the integral rank-55 witness used by the preceding one-sided
guard.  It is standard-library only and remains live under python -O and
python -I -S.
"""

from itertools import combinations, product


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


SITES = tuple(range(6))
COLOURS = (0, 1)
RARE = 2
P_VERTEX = 6
Q_VERTEX = 7
EDGES = tuple(combinations(SITES, 2))
WORDS = tuple(product(COLOURS, repeat=6))
CELLS = tuple(
    (u, v, a, b)
    for u, v in EDGES
    for a, b in product(COLOURS, repeat=2)
)
CELL_INDEX = {cell: index for index, cell in enumerate(CELLS)}
PURE_ZERO = frozenset(((0, 1), (2, 3), (4, 5)))
PURE_ONE = frozenset(((0, 2), (1, 4), (3, 5)))


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
MATCHINGS8 = perfect_matchings(tuple(range(8)))


def build_internal_packet():
    packet = {}
    for u, v in EDGES:
        for a, b in product(COLOURS, repeat=2):
            if (u, v) in PURE_ZERO:
                value = u + v + 1 if (a, b) == (0, 0) else 0
            elif (u, v) in PURE_ONE:
                value = u + 2 * v + 1 if (a, b) == (1, 1) else 0
            else:
                value = 1 + ((17 * u + 31 * v + 7 * a + 11 * b
                              + 3 * u * v) % 13)
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
            complement = tuple(x for x in SITES if x not in (u, v))
            row.append(hafnian(packet, complement, word))
        rows.append(row)
    return rows


def rank_mod(matrix, prime):
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
        rows[pivot_row] = [(entry * inverse) % prime
                           for entry in rows[pivot_row]]
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


def matrix_vector_product(matrix, vector):
    return [sum(entry * coefficient
                for entry, coefficient in zip(row, vector))
            for row in matrix]


def gauge_vectors(packet):
    vectors = []
    for distinguished in range(5):
        mu = [0] * 6
        mu[distinguished] = 1
        mu[5] = -1
        vectors.append([
            (mu[u] + mu[v]) * packet[u, v, a, b]
            for u, v, a, b in CELLS
        ])
    return vectors


def five_site_map(packet, anchor):
    """Rows of Phi_anchor; columns are (x,t), x != anchor."""

    remaining = tuple(x for x in SITES if x != anchor)
    columns = tuple((x, t) for x in remaining for t in COLOURS)
    rows = []
    for local_word in product(COLOURS, repeat=5):
        word = [0] * 6
        for x, value in zip(remaining, local_word):
            word[x] = value
        row = []
        for x, t in columns:
            complement = tuple(y for y in SITES if y not in (anchor, x))
            row.append(
                hafnian(packet, complement, word) if word[x] == t else 0
            )
        rows.append(row)
    return rows, columns


def star_cell(anchor, output, neighbour, neighbour_colour):
    if anchor < neighbour:
        return anchor, neighbour, output, neighbour_colour
    return neighbour, anchor, neighbour_colour, output


def audit_derivative_slice_identity(packet, derivative):
    """Phi is literally a fixed-output slice of dPsi on an anchor star."""

    for anchor in SITES:
        phi, columns = five_site_map(packet, anchor)
        remaining = tuple(x for x in SITES if x != anchor)
        for output in COLOURS:
            selected_rows = [
                row_index
                for row_index, word in enumerate(WORDS)
                if word[anchor] == output
            ]
            sliced = [
                [derivative[row_index][CELL_INDEX[
                    star_cell(anchor, output, neighbour, colour)
                ]] for neighbour, colour in columns]
                for row_index in selected_rows
            ]
            require(sliced == phi,
                    ("five-site map is not a derivative slice", anchor, output))

            for word, row in zip(WORDS, derivative):
                if word[anchor] == output:
                    continue
                require(all(
                    row[CELL_INDEX[star_cell(
                        anchor, output, neighbour, colour
                    )]] == 0
                    for neighbour, colour in columns
                ), ("anchor-star derivative leaks outside its slice",
                    anchor, output, word))


def audit_rank_open_conditions(packet):
    derivative = differential(packet)
    gauges = gauge_vectors(packet)
    slope = [hafnian(packet, SITES, word) for word in WORDS]
    require(all(value != 0 for value in slope),
            "the level-two slope is not everywhere live")
    require(all(matrix_vector_product(derivative, gauge) == [0] * 64
                for gauge in gauges),
            "a trace-zero vertex gauge left the differential kernel")
    require(rank_mod(gauges, 101) == 5,
            "the five integral gauge directions are dependent")
    require(rank_mod(derivative, 101) == 55,
            "the rank-55 differential minor vanished")

    live_edges = {
        (u, v)
        for u, v in EDGES
        if any(packet[u, v, a, b] != 0
               for a, b in product(COLOURS, repeat=2))
    }
    require(live_edges == set(EDGES), "the residual live graph is not K6")

    phi_ranks = []
    for anchor in SITES:
        deletion = tuple(x for x in SITES if x != anchor)
        deletion_edges = {(u, v) for u, v in live_edges
                          if u in deletion and v in deletion}
        require(len(deletion_edges) == 10,
                ("a deletion graph is not K5", anchor))
        require(any(
            (u, v) in deletion_edges and (u, w) in deletion_edges
            and (v, w) in deletion_edges
            for u, v, w in combinations(deletion, 3)
        ), ("a deletion graph is bipartite", anchor))

        phi, _columns = five_site_map(packet, anchor)
        ranks = (rank_mod(phi, 101), rank_mod(phi, 1_000_003))
        require(ranks == (10, 10),
                ("five-site map lost injectivity", anchor, ranks))
        phi_ranks.append(ranks[0])

    cofactor_support = []
    for r, x in EDGES:
        complement = tuple(y for y in SITES if y not in (r, x))
        values = []
        for local_word in product(COLOURS, repeat=4):
            word = [0] * 6
            for y, value in zip(complement, local_word):
                word[y] = value
            values.append(hafnian(packet, complement, word))
        require(all(value != 0 for value in values),
                ("a four-site cofactor coordinate vanished", r, x))
        cofactor_support.append(sum(value != 0 for value in values))

    audit_derivative_slice_identity(packet, derivative)
    return phi_ranks, cofactor_support


def literal_value(packet, word):
    total = 0
    for matching in MATCHINGS8:
        term = 1
        for u, v in matching:
            term *= packet.get((u, v, word[u], word[v]), 0)
        total += term
    return total


def audit_matching_factorizations(packet):
    """Check the L1, three-c, and four-c expansions as literal matchings."""

    direct_matchings = [matching for matching in MATCHINGS8
                        if (P_VERTEX, Q_VERTEX) in matching]
    require(len(direct_matchings) == 15,
            "wrong number of matchings through the rare direct edge")
    require(
        {tuple(edge for edge in matching
               if edge != (P_VERTEX, Q_VERTEX))
         for matching in direct_matchings}
        == set(MATCHINGS[SITES]),
        "deleting the rare direct edge is not a matching bijection",
    )

    # L1: q=c, p is binary, and Q=0.  The only surviving q-edge is pq.
    direct_scalar = 17
    for p_colour in COLOURS:
        eight_packet = dict(packet)
        eight_packet[P_VERTEX, Q_VERTEX, p_colour, RARE] = direct_scalar
        for tail in WORDS:
            word = tail + (p_colour, RARE)
            expected = direct_scalar * hafnian(packet, SITES, tail)
            require(literal_value(eight_packet, word) == expected,
                    ("L1 direct-column factorization failed", word))

    # Three c's: if q has the sole diagonal-c anchor r, q-r is forced and
    # expansion at p is exactly alpha_r Phi_r(P).
    alpha = 19
    star = {x: (x + 2, 2 * x + 3) for x in SITES}
    for anchor in SITES:
        eight_packet = dict(packet)
        eight_packet[anchor, Q_VERTEX, RARE, RARE] = alpha
        for x in SITES:
            for colour in COLOURS:
                eight_packet[x, P_VERTEX, colour, RARE] = star[x][colour]
        remaining = tuple(x for x in SITES if x != anchor)
        for local_word in product(COLOURS, repeat=5):
            tail = [0] * 6
            tail[anchor] = RARE
            for x, value in zip(remaining, local_word):
                tail[x] = value
            word = tuple(tail) + (RARE, RARE)
            expected = 0
            for x in remaining:
                complement = tuple(y for y in SITES
                                   if y not in (anchor, x))
                expected += (star[x][tail[x]]
                             * hafnian(packet, complement, tail))
            expected *= alpha
            require(literal_value(eight_packet, word) == expected,
                    ("three-c cofactor factorization failed", anchor, word))

    # Four c's: after Phi_r has killed P away from r, the q-r and p-x
    # edges are forced, leaving precisely the binary four-site cofactor.
    beta = 23
    for anchor, x in ((r, x) for r in SITES for x in SITES if x != r):
        eight_packet = dict(packet)
        eight_packet[anchor, Q_VERTEX, RARE, RARE] = alpha
        eight_packet[x, P_VERTEX, RARE, RARE] = beta
        complement = tuple(y for y in SITES if y not in (anchor, x))
        for local_word in product(COLOURS, repeat=4):
            tail = [RARE] * 6
            for y, value in zip(complement, local_word):
                tail[y] = value
            word = tuple(tail) + (RARE, RARE)
            expected = alpha * beta * hafnian(packet, complement, tail)
            require(literal_value(eight_packet, word) == expected,
                    ("four-c cofactor factorization failed", anchor, x, word))


def main():
    packet = build_internal_packet()
    phi_ranks, cofactor_support = audit_rank_open_conditions(packet)
    audit_matching_factorizations(packet)
    print(
        "one-sided overlap collapse: rank dPsi=55, slope support=64/64; "
        f"Phi ranks={phi_ranks}; four-site support="
        f"{sum(cofactor_support)}/{len(cofactor_support) * 16}; "
        "L1/three-c/four-c factorizations exact"
    )


if __name__ == "__main__":
    main()
