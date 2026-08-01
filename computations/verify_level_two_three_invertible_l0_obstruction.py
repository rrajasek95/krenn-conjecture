#!/usr/bin/env python3
"""Exact L0 obstruction to the displayed 3I+1R+2Z level-two guard.

Research evidence only.  This does not prove Krenn's conjecture and does not
exclude every three-invertible packet.  It proves that the *specific* binary
residual packet in verify_level_two_three_invertible_r2_guard.py cannot be
completed to the full eight-site equations, regardless of all cells outside
that residual packet.

For a binary residual packet M on six sites, let Psi(M) be its matching tensor
and D=dPsi_M.  If p,q are two new sites, then every fixed-colour binary slice
of an arbitrary extension has the exact form

    T_{s,t} = W_{s,t} Psi(M) + D(N^{s,t}),

where N^{s,t}_{ru}=U_r(s,-) V_u(t,-)^T +
V_r(t,-) U_u(s,-)^T.  Euler gives D(M)=3 Psi(M), so every such slice belongs
to im(D) over characteristic zero.  The two pure L0 target slices would be
the coordinate vectors e_(0^6) and e_(1^6).

For the guard packet, rank(D)=55 while adjoining either pure vector raises
the rank to 56, and adjoining both raises it to 57.  Deleting the two pure
rows still leaves rank 55, whereas any full solution with rank(D)=55 would
have mixed-row rank 53.  Thus no binary endpoint completion exists.  The full
slice formula is checked below as a formal matching-monomial identity on all
4*64 slices; no arbitrary zero completion is used.  All arithmetic is exact,
standard-library only, and checks remain live under python -O and python -I
-S.

The necessary rank screen is itself sharp.  A second integral packet below
has rank(D)=55, mixed-row rank 53, and two literal columns of D equal to the
two pure basis vectors.  This sharpness packet is not asserted to satisfy the
factored two-star endpoint equations.
"""

from collections import Counter
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
P_SITE = 6
Q_SITE = 7


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
MATCHINGS8 = perfect_matchings(tuple(range(8)))


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


M = {
    (u, v, a, b): BLOCKS[u, v][a][b]
    for u, v in EDGES
    for a, b in product(COLOURS, repeat=2)
}


def outer(left, right, scale=1):
    return tuple(
        tuple(scale * left[a] * right[b] for b in COLOURS)
        for a in COLOURS
    )


# A rank-sharp packet for the universal tangent-incidence screen.  On
# vertices 2,3,4,5 its K4 tensor is e_(0^4), while on vertices 0,1,2,3 it is
# e_(1^4).  In each K4 the two non-target matching products cancel as equal
# rank-one site products with opposite signs.
SHARP_SITE_VECTORS = {site: (site + 1, site + 2) for site in SITES}
E_ZERO = ((1, 0), (0, 0))
E_ONE = ((0, 0), (0, 1))
SHARP_BLOCKS = {
    (0, 1): outer(SHARP_SITE_VECTORS[0], SHARP_SITE_VECTORS[1]),
    (0, 2): E_ONE,
    (0, 3): outer(SHARP_SITE_VECTORS[0], (1, 0)),
    (0, 4): ((5, 6), (11, 8)),
    (0, 5): ((6, 7), (13, 9)),
    (1, 2): outer(SHARP_SITE_VECTORS[1], (1, 0), -1),
    (1, 3): E_ONE,
    (1, 4): ((6, 8), (12, 11)),
    (1, 5): ((7, 9), (14, 12)),
    (2, 3): E_ZERO,
    (2, 4): outer(SHARP_SITE_VECTORS[2], SHARP_SITE_VECTORS[4]),
    (2, 5): outer(SHARP_SITE_VECTORS[2], SHARP_SITE_VECTORS[5]),
    (3, 4): outer(SHARP_SITE_VECTORS[3], SHARP_SITE_VECTORS[4], -1),
    (3, 5): outer(SHARP_SITE_VECTORS[3], SHARP_SITE_VECTORS[5]),
    (4, 5): E_ZERO,
}
SHARP_M = {
    (u, v, a, b): SHARP_BLOCKS[u, v][a][b]
    for u, v in EDGES
    for a, b in product(COLOURS, repeat=2)
}


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
    return [
        [
            cofactor(packet, word, u, v)
            if (word[u], word[v]) == (a, b) else 0
            for u, v, a, b in CELLS
        ]
        for word in WORDS
    ]


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


def add_term(counter, monomial, coefficient):
    if not coefficient:
        return
    counter[tuple(sorted(monomial))] += coefficient
    if not counter[tuple(sorted(monomial))]:
        del counter[tuple(sorted(monomial))]


def literal_slice_counter(word, p_colour, q_colour):
    """Formal endpoint monomials from all 105 eight-site matchings."""

    answer = Counter()
    for matching in MATCHINGS8:
        coefficient = 1
        endpoint_factors = []
        for u, v in matching:
            if v < P_SITE:
                coefficient *= M[u, v, word[u], word[v]]
            elif (u, v) == (P_SITE, Q_SITE):
                endpoint_factors.append(("W", p_colour, q_colour))
            elif v == P_SITE:
                endpoint_factors.append(("U", u, p_colour, word[u]))
            elif v == Q_SITE:
                endpoint_factors.append(("V", u, q_colour, word[u]))
            else:
                raise RuntimeError(("unclassified matching edge", u, v))
        add_term(answer, endpoint_factors, coefficient)
    return answer


def derived_slice_counter(word, p_colour, q_colour):
    """The formal counter for W*Psi + dPsi(U wedge V)."""

    answer = Counter()
    add_term(
        answer,
        (("W", p_colour, q_colour),),
        hafnian(M, SITES, word),
    )
    for r, u in EDGES:
        coefficient = cofactor(M, word, r, u)
        add_term(
            answer,
            (("U", r, p_colour, word[r]),
             ("V", u, q_colour, word[u])),
            coefficient,
        )
        add_term(
            answer,
            (("V", r, q_colour, word[r]),
             ("U", u, p_colour, word[u])),
            coefficient,
        )
    return answer


def audit_matching_partition_and_slice_formula():
    direct = (P_SITE, Q_SITE)
    containing = tuple(matching for matching in MATCHINGS8
                       if direct in matching)
    avoiding = tuple(matching for matching in MATCHINGS8
                     if direct not in matching)
    require(len(MATCHINGS8) == 105, "the eight-site matching count changed")
    require(len(containing) == 15 and len(avoiding) == 90,
            "the direct-edge matching partition changed")
    require(
        {tuple(edge for edge in matching if edge != direct)
         for matching in containing} == set(MATCHINGS[SITES]),
        "removing pq is not the residual-matching bijection",
    )

    avoiding_data = set()
    for matching in avoiding:
        p_edge = next(edge for edge in matching if P_SITE in edge)
        q_edge = next(edge for edge in matching if Q_SITE in edge)
        r = p_edge[0]
        u = q_edge[0]
        require(r != u, "p and q meet the same residual vertex")
        residual = tuple(edge for edge in matching
                         if edge not in (p_edge, q_edge))
        avoiding_data.add((r, u, residual))
    expected = {
        (r, u, matching)
        for r in SITES
        for u in SITES if u != r
        for matching in MATCHINGS[tuple(
            site for site in SITES if site not in (r, u)
        )]
    }
    require(avoiding_data == expected,
            "the ordered two-star matching parametrization failed")

    checked = 0
    for p_colour, q_colour in product(COLOURS, repeat=2):
        for word in WORDS:
            require(
                literal_slice_counter(word, p_colour, q_colour)
                == derived_slice_counter(word, p_colour, q_colour),
                ("formal L0 slice formula failed", p_colour, q_colour, word),
            )
            checked += 1
    require(checked == 4 * 64, "not every binary L0 slice was checked")
    return checked


def append_columns(matrix, *columns):
    require(all(len(column) == len(matrix) for column in columns),
            "an augmented column has the wrong height")
    return [row[:] + [column[index] for column in columns]
            for index, row in enumerate(matrix)]


def ranks_over_three_fields(matrix):
    return (
        rational_rank(matrix),
        modular_rank(matrix, 101),
        modular_rank(matrix, 1_000_003),
    )


def audit_euler_and_l0_image_obstruction():
    slope = matching_tensor(M)
    require(apply_differential(M, M) == [3 * value for value in slope],
            "Euler's identity dPsi_M(M)=3 Psi(M) failed")

    derivative = differential_matrix(M)
    pure_zero = [int(word == (0,) * 6) for word in WORDS]
    pure_one = [int(word == (1,) * 6) for word in WORDS]
    mixed_derivative = [
        row for row, word in zip(derivative, WORDS)
        if word not in ((0,) * 6, (1,) * 6)
    ]
    ranks = {
        "D": ranks_over_three_fields(derivative),
        "D_mixed": ranks_over_three_fields(mixed_derivative),
        "D|e0": ranks_over_three_fields(
            append_columns(derivative, pure_zero)
        ),
        "D|e1": ranks_over_three_fields(
            append_columns(derivative, pure_one)
        ),
        "D|e0,e1": ranks_over_three_fields(
            append_columns(derivative, pure_zero, pure_one)
        ),
    }
    require(ranks == {
        "D": (55, 55, 55),
        "D_mixed": (55, 55, 55),
        "D|e0": (56, 56, 56),
        "D|e1": (56, 56, 56),
        "D|e0,e1": (57, 57, 57),
    }, ("the tangent-image rank certificate changed", ranks))
    return ranks


def audit_tangent_incidence_sharpness():
    derivative = differential_matrix(SHARP_M)
    mixed_derivative = [
        row for row, word in zip(derivative, WORDS)
        if word not in ((0,) * 6, (1,) * 6)
    ]
    ranks = {
        "D": ranks_over_three_fields(derivative),
        "D_mixed": ranks_over_three_fields(mixed_derivative),
    }
    require(ranks == {
        "D": (55, 55, 55),
        "D_mixed": (53, 53, 53),
    }, ("the sharp tangent-incidence ranks changed", ranks))

    pure_zero = [int(word == (0,) * 6) for word in WORDS]
    pure_one = [int(word == (1,) * 6) for word in WORDS]
    zero_column = CELLS.index((0, 1, 0, 0))
    one_column = CELLS.index((4, 5, 1, 1))
    require([row[zero_column] for row in derivative] == pure_zero,
            "the literal e_(0^6) tangent column changed")
    require([row[one_column] for row in derivative] == pure_one,
            "the literal e_(1^6) tangent column changed")
    return ranks


def audit_fixed_and_free_cell_scope():
    total = len(tuple(combinations(range(8), 2))) * 3 * 3
    residual_binary = len(EDGES) * 2 * 2
    selected_endpoint_stars = 2 * len(SITES) * 2
    selected_direct = 1
    minimal_fixed = residual_binary + selected_endpoint_stars + selected_direct

    # endpoint_blocks() in the R2 guard optionally assigns all 2x2 binary
    # endpoint/residual subblocks: 48 cells beyond the selected c-columns.
    optional_r2_binary_endpoint = 2 * len(SITES) * 2 * 2
    r2_fixed = minimal_fixed + optional_r2_binary_endpoint
    require(
        (total, residual_binary, minimal_fixed, total - minimal_fixed,
         r2_fixed, total - r2_fixed)
        == (252, 60, 85, 167, 133, 119),
        "the fixed/free cell census changed",
    )
    return minimal_fixed, total - minimal_fixed, r2_fixed, total - r2_fixed


def main():
    checked = audit_matching_partition_and_slice_formula()
    ranks = audit_euler_and_l0_image_obstruction()
    sharp_ranks = audit_tangent_incidence_sharpness()
    minimal_fixed, minimal_free, r2_fixed, r2_free = (
        audit_fixed_and_free_cell_scope()
    )
    print("three-invertible L0 image obstruction: all checks passed")
    print("  formal eight-site slices : %d/256 exact" % checked)
    print("  ranks Q/mod101/mod1000003:")
    for label in ("D", "D_mixed", "D|e0", "D|e1", "D|e0,e1"):
        print("    %-9s: %s" % (label, ranks[label]))
    print("  minimal guard cells      : %d fixed, %d free"
          % (minimal_fixed, minimal_free))
    print("  optional R2 completion   : %d fixed, %d free"
          % (r2_fixed, r2_free))
    print("  incidence sharpness      : D=%s, D_mixed=%s"
          % (sharp_ranks["D"], sharp_ranks["D_mixed"]))
    print("  conclusion               : no full completion of this fixed M")


if __name__ == "__main__":
    main()
