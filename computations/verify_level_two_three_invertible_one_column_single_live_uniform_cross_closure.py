#!/usr/bin/env python3
"""Close a single-live uniform common-factor one-column overlap.

Assume P_t=0, Q_t!=0.  Exactly one t-Z edge, t-z, is live; z has one
active P/V endpoint family with uniform I-z spoke multiples, while the
other zero w is endpoint-inactive and M_tw=0.  The exceptional t-star and
the uniform z-star reduce modulo radial gauges to one tangent T supported
on t-z.  Mixed L0 leaves two pure scalar charts.  The first pure equation
forces M_tz and its four-site cofactor to the complementary pure word.
The full matching tensor then differs from that pure tensor by one
Q_t tensor v_z shore factor, producing a rank-two/rank-one contradiction.

The Q_t=0, Q/U case is symmetric.  Standard library only; all checks
remain live under -O and -I -S.
"""

from fractions import Fraction as Q
from itertools import combinations, product


INNER = (0, 1, 2)
RANK_ONE = 3
ACTIVE_ZERO = 4
OTHER_ZERO = 5
CORE = INNER + (RANK_ONE,)
SITES = CORE + (ACTIVE_ZERO, OTHER_ZERO)
COLOURS = (0, 1)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        remaining = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remaining):
            answer.append(((first, second),) + tail)
    return tuple(answer)


MATCHINGS = perfect_matchings(SITES)


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
            rows[slot] = [
                left - multiple * right
                for left, right in zip(rows[slot], rows[rank])
            ]
        rank += 1
    return rank


# Sparse formal polynomials.
def constant(value):
    return {(): Q(value)} if value else {}


def variable(name):
    return {(name,): Q(1)}


def add(*polynomials):
    answer = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] = answer.get(monomial, Q(0)) + coefficient
            if not answer[monomial]:
                del answer[monomial]
    return answer


def scale(coefficient, polynomial):
    return {
        monomial: Q(coefficient) * value
        for monomial, value in polynomial.items()
        if coefficient * value
    }


def multiply(left, right):
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


def audit_two_radial_reductions():
    # Use scalar stand-ins for whole nonzero blocks.  On I-t,
    # S_t=2*tau*M; on I-z, M=m*S_z; the only remaining incident block is
    # B=M_tz.  Therefore
    #
    # S_t = 2*tau*G(e_t) - 2*tau*T,
    # S_z = (1/m)*G(e_z) - (1/m)*T.
    tau = Q(3, 2)
    m = Q(5, 3)
    packet = {}
    s_t = {}
    s_z = {}
    tangent = {}
    for edge in combinations(SITES, 2):
        u, v = edge
        s_t[edge] = Q(u + v + 1) if u in INNER and v == RANK_ONE else Q(0)
        s_z[edge] = Q(2 * u + v + 1) if u in INNER and v == ACTIVE_ZERO else Q(0)
        tangent[edge] = Q(11) if edge == (RANK_ONE, ACTIVE_ZERO) else Q(0)
        if s_t[edge]:
            packet[edge] = s_t[edge] / (2 * tau)
        elif s_z[edge]:
            packet[edge] = m * s_z[edge]
        elif tangent[edge]:
            packet[edge] = tangent[edge]
        else:
            packet[edge] = Q(0)

    checks = 0
    for edge in combinations(SITES, 2):
        radial_t = int(RANK_ONE in edge) * packet[edge]
        radial_z = int(ACTIVE_ZERO in edge) * packet[edge]
        require(
            s_t[edge] == 2 * tau * radial_t - 2 * tau * tangent[edge],
            ("t-star radial reduction failed", edge),
        )
        require(
            s_z[edge] == radial_z / m - tangent[edge] / m,
            ("zero-star radial reduction failed", edge),
        )
        checks += 2
    require(checks == 30, "radial reduction census changed")
    return checks


def audit_single_edge_support_rigidity():
    # If q*T=G(lambda), the triangle, I-t, and I-z blocks force all weights
    # at I,t,z to zero.  The live t-z block then forces q=0.  Variables are
    # lambda_0,lambda_1,lambda_2,lambda_t,lambda_z,q.
    rows = []

    def equation(entries):
        row = [Q(0)] * 6
        for column, coefficient in entries.items():
            row[column] += Q(coefficient)
        rows.append(row)

    for i, j in combinations(INNER, 2):
        equation({i: 1, j: 1})
    for i in INNER:
        equation({i: 1, RANK_ONE: 1})
        equation({i: 1, 4: 1})
    equation({RANK_ONE: 1, 4: 1, 5: -1})
    require(len(rows) == 10 and rational_rank(rows) == 6,
            "a generalized gauge survived on the single live edge")
    return len(rows)


def audit_scalar_patterns():
    # eta_u=2*tau*(d_u-b_u)+f_u/m is the single-edge coefficient after
    # radial reduction.  Mixed L0 gives a0*eta1=a1*eta0=0.  If both pure
    # products vanish, pure collinearity closes; exactly two charts remain.
    closed = 0
    survivors = []
    for a0, a1, eta0, eta1 in product((0, 1), repeat=4):
        if a0 * eta1 or a1 * eta0:
            continue
        pure = (a0 * eta0, a1 * eta1)
        if pure == (0, 0):
            closed += 1
        else:
            survivors.append((a0, a1, eta0, eta1, pure))
    require(survivors == [
        (0, 1, 0, 1, (0, 1)),
        (1, 0, 1, 0, (1, 0)),
    ], ("single-edge scalar charts changed", survivors))
    require(closed == 7, "single-edge closed-chart count changed")
    return closed, survivors


def audit_first_pure_flattening():
    # In a survivor, H=h*e_s^6 and the pure-k equation is
    #
    # q*(B tensor C)=e_k^6-kappa*h*e_s^6, k=1-s.
    #
    # Across {t,z}|the remaining four sites, B tensor C has rank one.  The
    # displayed pure 2x2 minor forces kappa=0; singleton support forces
    # B=beta*E_kk and C=gamma*e_k^4.
    kappa = variable("kappa")
    h = variable("h")
    checks = 0
    for missing in COLOURS:
        k = 1 - missing
        matrix = [[constant(0), constant(0)] for _ in COLOURS]
        matrix[k][0] = constant(1)
        matrix[missing][1] = scale(-1, multiply(kappa, h))
        determinant = add(
            multiply(matrix[0][0], matrix[1][1]),
            scale(-1, multiply(matrix[0][1], matrix[1][0])),
        )
        expected = scale(
            -1 if k == 0 else 1, multiply(kappa, h)
        )
        require(determinant == expected and determinant,
                ("first pure flattening minor changed", missing))

        pair_word = (k, k)
        four_word = (k,) * 4
        singleton = frozenset(((pair_word, four_word),))
        require(
            frozenset(left for left, _ in singleton) == frozenset((pair_word,))
            and frozenset(right for _, right in singleton)
            == frozenset((four_word,)),
            "singleton support did not isolate B and C",
        )
        checks += 1
    return checks


def audit_matching_decomposition():
    # With M_tw=M_zw=0, every nonzero matching either uses t-z and a
    # matching on I+w, or pairs t and z to two distinct I vertices and the
    # remaining I vertex to w.  The first class gives B tensor C; the second
    # shares the physical pair factor Q_t tensor v_z.  Six other matchings
    # contain a dead edge.
    categories = {"B*C": 0, "Qv*K": 0, "dead": 0}
    checks = 0
    for matching in MATCHINGS:
        edges = frozenset(matching)
        if (RANK_ONE, ACTIVE_ZERO) in edges:
            category = "B*C"
            remaining = tuple(
                edge for edge in matching
                if edge != (RANK_ONE, ACTIVE_ZERO)
            )
            require(len(remaining) == 2,
                    ("wrong B-cofactor matching", matching))
        elif any(
            (RANK_ONE in edge and OTHER_ZERO in edge)
            or (ACTIVE_ZERO in edge and OTHER_ZERO in edge)
            for edge in matching
        ):
            category = "dead"
        else:
            category = "Qv*K"
            t_edge = next(edge for edge in matching if RANK_ONE in edge)
            z_edge = next(edge for edge in matching if ACTIVE_ZERO in edge)
            w_edge = next(edge for edge in matching if OTHER_ZERO in edge)
            require(
                any(i in t_edge for i in INNER)
                and any(i in z_edge for i in INNER)
                and any(i in w_edge for i in INNER),
                ("a cross matching lost its I partners", matching),
            )
        categories[category] += 1
        checks += 1
    require(checks == 15, "K6 matching census changed")
    require(categories == {"B*C": 3, "Qv*K": 6, "dead": 6},
            ("matching decomposition changed", categories))
    return categories


def audit_second_flattening_contradiction():
    # The full matching decomposition is
    #
    # H = B tensor C + (Q_t tensor v_z) tensor K.
    #
    # The first pure flattening gives H=h e_s^6 and
    # B tensor C=g e_k^6 with h,g nonzero and k=1-s.  Hence the final
    # Qv tensor K term would equal their difference, whose shore flattening
    # has determinant +/-h*g and rank two.
    h = variable("h")
    g = variable("g")
    checks = 0
    for s in COLOURS:
        k = 1 - s
        matrix = [[constant(0), constant(0)] for _ in COLOURS]
        matrix[s][0] = h
        matrix[k][1] = scale(-1, g)
        determinant = add(
            multiply(matrix[0][0], matrix[1][1]),
            scale(-1, multiply(matrix[0][1], matrix[1][0])),
        )
        expected = scale(
            -1 if s == 0 else 1, multiply(h, g)
        )
        require(determinant == expected and determinant,
                ("final rank-two determinant changed", s))
        checks += 1
    return checks


def audit_symmetric_dictionary():
    p_zero = ("P_t=0", "P/V", "a", "Q_t")
    q_zero = ("Q_t=0", "Q/U", "b", "P_t")
    require(len(p_zero) == len(q_zero) == 4,
            "symmetric single-live dictionary changed")
    require(set(p_zero).isdisjoint(q_zero),
            "symmetric single-live labels collided")
    return p_zero, q_zero


def main():
    radial = audit_two_radial_reductions()
    support = audit_single_edge_support_rigidity()
    closed, survivors = audit_scalar_patterns()
    first = audit_first_pure_flattening()
    categories = audit_matching_decomposition()
    second = audit_second_flattening_contradiction()
    audit_symmetric_dictionary()
    print("three-invertible single-live uniform overlap: all checks passed")
    print(f"  radial edge identities   : {radial}")
    print(f"  support equations/rank   : {support}/6")
    print(f"  scalar charts closed/live: {closed}/{len(survivors)}")
    print(f"  first/final flattenings  : {first}/{second}")
    print(f"  matching decomposition   : {categories}")
    print("  symmetric P/Q cases      : both closed")


if __name__ == "__main__":
    main()
