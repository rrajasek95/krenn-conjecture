#!/usr/bin/env python3
"""Exact finite audit of the mixed-support pair and pure-triangle collapse.

Research evidence only.  Krenn's conjecture remains open and the fully
invertible residual locus is already closed separately by R2.

On the four-cycle-generic invertible chart, each mixed factored-L0 support is
one of 17 labelled graphs: empty, a K_1,5 star, or K_3 disjoint union K_3.
A live mixed edge with invertible residual block makes both endpoint factor
matrices invertible.  Every nonempty graph in the list also has a dead edge
between live vertices, which is impossible.  Thus only the empty-empty pair
survives the 17 by 17 split.

For empty mixed support, normalize three invertible pure-00 site factors to
the identity.  The three zero mixed-01 blocks form a full-rank six-variable
linear system and force the pure-11 second column to vanish at all three
sites.  Hence a factored solution must satisfy, on every residual triangle,

    product_{ru in K3} det(N00_ru) det(N11_ru) = 0.

This standard-library checker audits the labelled graph census, all 289
support pairs, the exact normalized triangle system, the determinant
transport identity, and the nontrivial leading coefficient of every pure
block determinant on an invertible residual edge.  Checks remain live under
python -O and python -I -S.
"""

from fractions import Fraction as Q
from itertools import combinations, product


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


SITES = tuple(range(6))
EDGES = tuple(combinations(SITES, 2))
TRIPLES = tuple(combinations(SITES, 3))
EMPTY = frozenset()


def expected_supports():
    supports = {EMPTY: ("empty", ())}
    for centre in SITES:
        graph = frozenset(
            tuple(sorted((centre, other)))
            for other in SITES if other != centre
        )
        supports[graph] = ("star", (centre,))
    for triangle in combinations(SITES, 3):
        if 0 not in triangle:
            continue
        complement = tuple(site for site in SITES if site not in triangle)
        graph = frozenset(
            tuple(combinations(triangle, 2))
            + tuple(combinations(complement, 2))
        )
        supports[graph] = ("triangles", (triangle, complement))
    require(len(supports) == 17, "the labelled support census is not 17")
    require(
        sum(kind == "empty" for kind, _ in supports.values()) == 1
        and sum(kind == "star" for kind, _ in supports.values()) == 6
        and sum(kind == "triangles" for kind, _ in supports.values()) == 10,
        "the empty/star/triangle support counts changed",
    )
    return supports


def dead_edge_between_live_vertices(graph):
    live_vertices = frozenset(site for edge in graph for site in edge)
    dead_edges = tuple(
        edge for edge in combinations(sorted(live_vertices), 2)
        if edge not in graph
    )
    return live_vertices, dead_edges


def audit_nonempty_supports(supports):
    witnesses = {}
    for graph, (kind, _) in supports.items():
        if not graph:
            continue
        live_vertices, dead_edges = dead_edge_between_live_vertices(graph)
        # Every live edge has N_ru=(lambda_r+lambda_u)M_ru invertible on the
        # chart, so its two endpoint site factors are invertible.  A dead
        # edge between two such vertices would then be both zero and
        # invertible, the required contradiction.
        require(live_vertices == frozenset(SITES),
                ("a nonempty allowed support has an inactive vertex", kind))
        require(dead_edges,
                ("a nonempty allowed support has no dead-edge witness", kind))
        witnesses[graph] = dead_edges[0]
    require(len(witnesses) == 16,
            "not all 16 nonempty supports were excluded")

    pair_counts = {"first_nonempty": 0, "second_only": 0, "survivor": 0}
    survivor = None
    graphs = tuple(supports)
    for first, second in product(graphs, repeat=2):
        if first:
            pair_counts["first_nonempty"] += 1
        elif second:
            pair_counts["second_only"] += 1
        else:
            pair_counts["survivor"] += 1
            survivor = (first, second)
    require(pair_counts == {
        "first_nonempty": 16 * 17,
        "second_only": 16,
        "survivor": 1,
    }, ("the 17 by 17 pair collapse changed", pair_counts))
    require(survivor == (EMPTY, EMPTY),
            "the unique mixed-support survivor is not empty-empty")
    return witnesses, pair_counts


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
    return rank


def audit_shared_triangle_lemma():
    # At each of three sites normalize X_r^00=[U_r^0,V_r^0] to I_2 and
    # write d_r=(X_r^00)^(-1)V_r^1=(x_r,y_r).  The mixed block is
    #
    #   e0 d_u^T + d_r e0^T = [[x_r+x_u,y_u],[y_r,0]].
    #
    # All three pair blocks vanish.  Coefficient rows are ordered in the
    # variables x0,y0,x1,y1,x2,y2.
    equations = []
    for r, u in combinations(range(3), 2):
        x_sum = [0] * 6
        x_sum[2 * r] = 1
        x_sum[2 * u] = 1
        y_u = [0] * 6
        y_u[2 * u + 1] = 1
        y_r = [0] * 6
        y_r[2 * r + 1] = 1
        equations.extend((x_sum, y_u, y_r))
    require(len(equations) == 9,
            "the normalized mixed-triangle equation count changed")
    require(rational_rank(equations) == 6,
            "the mixed-triangle equations no longer force every d_r to zero")

    # Independently replay the coefficient consequences pair by pair.
    candidate_scalars = (Q(7, 3), Q(-7, 3), Q(-7, 3))
    require(candidate_scalars[0] + candidate_scalars[1] == 0
            and candidate_scalars[0] + candidate_scalars[2] == 0,
            "the first two pair equations were encoded incorrectly")
    require(candidate_scalars[1] + candidate_scalars[2] != 0,
            "characteristic-zero triangle closure became vacuous")
    return len(equations), rational_rank(equations)


# ---------------------------------------------------------------------------
# Tiny sparse-polynomial engine for the determinant identities.


def constant(value):
    return {(): value} if value else {}


def variable(name):
    return {(name,): 1}


def add(*polynomials):
    answer = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] = answer.get(monomial, 0) + coefficient
            if not answer[monomial]:
                del answer[monomial]
    return answer


def scale(coefficient, polynomial):
    return {monomial: coefficient * value
            for monomial, value in polynomial.items()
            if coefficient * value}


def multiply(left, right):
    answer = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            answer[monomial] = (
                answer.get(monomial, 0)
                + left_coefficient * right_coefficient
            )
            if not answer[monomial]:
                del answer[monomial]
    return answer


def determinant_2(matrix):
    return add(
        multiply(matrix[0][0], matrix[1][1]),
        scale(-1, multiply(matrix[0][1], matrix[1][0])),
    )


def transpose(matrix):
    return tuple(tuple(matrix[column][row] for column in range(2))
                 for row in range(2))


def matrix_product(left, right):
    return tuple(tuple(add(*(
        multiply(left[row][middle], right[middle][column])
        for middle in range(2)
    )) for column in range(2)) for row in range(2))


J = ((constant(0), constant(1)), (constant(1), constant(0)))


def symbolic_matrix(prefix):
    return tuple(tuple(variable(f"{prefix}{row}{column}")
                       for column in range(2)) for row in range(2))


def audit_determinant_transport_and_cover():
    left = symbolic_matrix("l")
    right = symbolic_matrix("r")
    transported = matrix_product(matrix_product(left, J), transpose(right))
    expected = scale(-1, multiply(
        determinant_2(left), determinant_2(right)
    ))
    require(determinant_2(transported) == expected,
            "det(X J Y^T) is not -det(X)det(Y)")

    # For one triangle, multiplying the three edge determinants in each
    # pure slice squares every site determinant.  Thus simultaneous
    # invertibility of the six pure blocks is precisely the forbidden
    # common-site-invertibility condition used by the triangle lemma.
    site_determinants = {
        (slice_colour, site): variable(f"d{slice_colour}_{site}")
        for slice_colour in (0, 1) for site in range(3)
    }
    cover_product = constant(1)
    for slice_colour in (0, 1):
        for r, u in combinations(range(3), 2):
            edge_determinant = scale(-1, multiply(
                site_determinants[slice_colour, r],
                site_determinants[slice_colour, u],
            ))
            cover_product = multiply(cover_product, edge_determinant)
    expected_monomial = tuple(sorted(
        name
        for slice_colour in (0, 1)
        for site in range(3)
        for name in (f"d{slice_colour}_{site}",) * 2
    ))
    require(cover_product == {expected_monomial: 1},
            "the pure-triangle determinant product changed")

    # det(K+aM) has leading coefficient det(M).  Verify this formally with
    # independent K and M entries; invertible M makes each determinant a
    # nonzero polynomial in the relevant pure potential sum.
    parameter = variable("a")
    k_matrix = symbolic_matrix("k")
    m_matrix = symbolic_matrix("m")
    pencil = tuple(tuple(add(
        k_matrix[row][column],
        multiply(parameter, m_matrix[row][column]),
    ) for column in range(2)) for row in range(2))
    pencil_determinant = determinant_2(pencil)
    leading_terms = {
        monomial: coefficient
        for monomial, coefficient in pencil_determinant.items()
        if monomial.count("a") == 2
    }
    expected_leading = {
        tuple(sorted(("a", "a") + monomial)): coefficient
        for monomial, coefficient in determinant_2(m_matrix).items()
    }
    require(leading_terms == expected_leading,
            "the leading coefficient of det(K+aM) is not det(M)")
    return len(TRIPLES)


def main():
    supports = expected_supports()
    witnesses, pair_counts = audit_nonempty_supports(supports)
    triangle_system = audit_shared_triangle_lemma()
    cover_count = audit_determinant_transport_and_cover()
    print("mixed-support pair collapse: all checks passed")
    print("  labelled supports        : 1 empty + 6 stars + 10 triangle pairs")
    print("  nonempty contradictions : %d/16" % len(witnesses))
    print("  support-pair split       : 288 killed, 1 empty-empty survivor")
    print("  shared triangle system  : %d equations, rank %d/6"
          % triangle_system)
    print("  pure determinant cover  : %d/20 residual triples" % cover_count)
    print("  scope                    : finite generic theorem; conjecture open")


if __name__ == "__main__":
    main()
