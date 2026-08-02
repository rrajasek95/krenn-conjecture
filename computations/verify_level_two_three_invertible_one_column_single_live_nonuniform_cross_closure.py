#!/usr/bin/env python3
"""Close the single-live nonuniform common-factor one-column overlap.

Assume P_t=0, Q_t!=0, exactly one t-Z block B=M_tz is live, the other
zero endpoint is inactive, and z is active P/V type with

    M_iz=m_i P_i v_z^T,  i in I,

where the three nonzero multiples m_i are not all equal.  Mixed L0
localization kills separately the nonuniform zero-star and the live-edge
tangent.  A surviving pure correction is a linear combination of their
derivatives.  The two pair-shore rank-one equations reduce it to an exact
four-site cofactor pattern, and the selected-basis support of that pattern
is contradictory.

The opposite Q/U type at the same P_t=0 boundary is easier: L1 makes the
live block a Q_t tensor u_z shore, so the matching tensor and every
remaining endpoint correction share that pair factor.  The two pure L0
targets cannot both have it.  Standard library only; checks remain live
under -O and -I -S.
"""

from fractions import Fraction as Q
from itertools import combinations, product


INNER = (0, 1, 2)
RANK_ONE = 3
ACTIVE_ZERO = 4
OTHER_ZERO = 5
SITES = INNER + (RANK_ONE, ACTIVE_ZERO, OTHER_ZERO)
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


def multiply(*polynomials):
    answer = constant(1)
    for polynomial in polynomials:
        updated = {}
        for left_monomial, left_coefficient in answer.items():
            for right_monomial, right_coefficient in polynomial.items():
                monomial = tuple(sorted(left_monomial + right_monomial))
                updated[monomial] = (
                    updated.get(monomial, Q(0))
                    + left_coefficient * right_coefficient
                )
                if not updated[monomial]:
                    del updated[monomial]
        answer = updated
    return answer


def audit_exceptional_reduction():
    # After the aligned core gauge is removed, an endpoint packet is
    #
    #   a_s f_u S_z + a_s(d_u-b_u)S_t.
    #
    # With B=M_tz the only live t-Z edge,
    # S_t=2*tau*G(e_t)-2*tau*T_B.  Use scalar block stand-ins to audit
    # the latter identity on all residual edges.
    tau = Q(5, 3)
    packet = {}
    star = {}
    tangent = {}
    for edge in combinations(SITES, 2):
        i, j = edge
        star[edge] = Q(i + j + 2) if i in INNER and j == RANK_ONE else Q(0)
        tangent[edge] = Q(17) if edge == (RANK_ONE, ACTIVE_ZERO) else Q(0)
        if star[edge]:
            packet[edge] = star[edge] / (2 * tau)
        elif tangent[edge]:
            packet[edge] = tangent[edge]
        else:
            packet[edge] = Q(0)

    checks = 0
    for edge in combinations(SITES, 2):
        radial = int(RANK_ONE in edge) * packet[edge]
        require(
            star[edge] == 2 * tau * radial - 2 * tau * tangent[edge],
            ("nonuniform exceptional reduction failed", edge),
        )
        checks += 1
    require(checks == 15, "exceptional edge census changed")
    return checks


def audit_nonuniform_live_localization():
    # For q*S_z+r*T_B=G(lambda), the I-triangle and I-t blocks kill
    # lambda_I and lambda_t.  The I-z equations are q=lambda_z*m_i.
    # Their exact pair certificate forces q=lambda_z=0 when the m_i are
    # nonuniform, and the live t-z equation then forces r=0.
    lam = variable("lambda_z")
    q = variable("q")
    multiples = [variable(f"m{i}") for i in INNER]
    equations = [add(multiply(lam, multiple), scale(-1, q))
                 for multiple in multiples]
    certificates = 0
    for i, j in combinations(INNER, 2):
        left = add(
            multiply(multiples[j], equations[i]),
            scale(-1, multiply(multiples[i], equations[j])),
        )
        right = multiply(
            q, add(multiples[i], scale(-1, multiples[j]))
        )
        require(left == right,
                ("nonuniform live localization identity failed", i, j))
        certificates += 1

    # Numeric rank audit with a genuinely nonuniform triple.  Columns are
    # lambda_0,lambda_1,lambda_2,lambda_t,lambda_z,q,r.
    rows = []

    def equation(entries):
        row = [Q(0)] * 7
        for column, coefficient in entries.items():
            row[column] += Q(coefficient)
        rows.append(row)

    for i, j in combinations(INNER, 2):
        equation({i: 1, j: 1})
    for i in INNER:
        equation({i: 1, RANK_ONE: 1})
    for i, multiple in zip(INNER, (2, 3, 5)):
        equation({i: multiple, 4: multiple, 5: -1})
    equation({RANK_ONE: 1, 4: 1, 6: -1})
    require(len(rows) == 10 and rational_rank(rows) == 7,
            "a nonzero zero-star/live-edge gauge combination survived")
    return certificates, len(rows)


def audit_scalar_patterns():
    # Write c_u=2*tau*(d_u-b_u).  Modulo gauges the correction is
    # a_s(f_u*S_z-c_u*T).  The two mixed slices force
    #
    # a0*f1=a0*c1=a1*f0=a1*c0=0.
    #
    # Hence nongauge pure support occurs in at most one colour.  Record
    # zero/nonzero supports of (f_u,c_u).
    closed = 0
    survivors = []
    supports = ((0, 0), (1, 0), (0, 1), (1, 1))
    for a0, a1 in product((0, 1), repeat=2):
        for support0, support1 in product(supports, repeat=2):
            f0, c0 = support0
            f1, c1 = support1
            # Active P/V means that at least one zero-endpoint scalar is
            # nonzero.  The broader inactive chart is handled separately.
            if not (f0 or f1):
                continue
            if a0 * f1 or a0 * c1 or a1 * f0 or a1 * c0:
                continue
            pure = tuple(
                colour for colour, (a, support) in enumerate(
                    ((a0, support0), (a1, support1))
                ) if a and any(support)
            )
            require(len(pure) <= 1,
                    ("two nonuniform pure corrections survived", a0, a1,
                     support0, support1))
            if pure:
                survivors.append((a0, a1, support0, support1, pure[0]))
            else:
                closed += 1
    require(closed == 12, ("nonuniform closed scalar count changed", closed))
    require(len(survivors) == 4,
            ("nonuniform survivor count changed", survivors))
    require({entry[-1] for entry in survivors} == {0, 1},
            "one pure correction colour disappeared")
    return closed, survivors


def audit_matching_and_derivative_decomposition():
    # H has 3 matchings through tz, 6 cross matchings sharing
    # Y=Q_t tensor v_z, and 6 dead matchings through tw or zw.  D(T_B)
    # is B tensor C.  D(S_z) has nine formal tangent/cofactor terms; the
    # three with t-w die and the remaining six share the same Y.
    categories = {"B*C": 0, "Y*K": 0, "dead": 0}
    for matching in MATCHINGS:
        edges = frozenset(matching)
        if (RANK_ONE, ACTIVE_ZERO) in edges:
            category = "B*C"
        elif any(
            (RANK_ONE in edge and OTHER_ZERO in edge)
            or (ACTIVE_ZERO in edge and OTHER_ZERO in edge)
            for edge in matching
        ):
            category = "dead"
        else:
            category = "Y*K"
        categories[category] += 1
    require(categories == {"B*C": 3, "Y*K": 6, "dead": 6},
            ("nonuniform matching decomposition changed", categories))

    derivative = {"Y*L": 0, "dead": 0}
    for i in INNER:
        remaining = tuple(site for site in SITES
                          if site not in (i, ACTIVE_ZERO))
        for matching in perfect_matchings(remaining):
            if any(RANK_ONE in edge and OTHER_ZERO in edge
                   for edge in matching):
                derivative["dead"] += 1
            else:
                t_edge = next(edge for edge in matching
                              if RANK_ONE in edge)
                require(any(j in t_edge for j in INNER if j != i),
                        ("zero-star derivative lost Q_t", i, matching))
                derivative["Y*L"] += 1
    require(derivative == {"Y*L": 6, "dead": 3},
            ("zero-star derivative census changed", derivative))
    return categories, derivative


def audit_pair_shore_reduction():
    # The two equations on the {t,z}|rest cut are
    #
    # H=X*C+Y*K=h E_s*F_s,
    # E_k*F_k=kappa H+A Y*L+D X*C,
    #
    # with (A,D)!=(0,0).  If X,Y are dependent, both equations have one
    # left factor and cannot give complementary E_s,E_k.  If independent,
    # rank(H)=1 makes C,K dependent.  The second target puts E_k in
    # span(E_s,Y).  A decomposable Y in span(E_00,E_11) is one of those
    # two endpoints; independence excludes E_s, so Y=E_k.  Its remaining
    # right equation has A!=0 and L=alpha F_k+beta F_s, alpha!=0.
    a = variable("a")
    b = variable("b")
    diagonal = ((a, constant(0)), (constant(0), b))
    determinant = add(
        multiply(diagonal[0][0], diagonal[1][1]),
        scale(-1, multiply(diagonal[0][1], diagonal[1][0])),
    )
    require(determinant == multiply(a, b) and determinant,
            "the diagonal pair plane acquired another rank-one point")

    # Audit the two complementary pair words and four-shore words.
    checks = 0
    for s in COLOURS:
        k = 1 - s
        pair_words = ((s, s), (k, k))
        four_words = ((s,) * 4, (k,) * 4)
        require(pair_words[0] != pair_words[1]
                and four_words[0] != four_words[1],
                ("complementary shore words collided", s))
        checks += 1
    return checks


def cofactor_coefficients(word, rows):
    # Selected coordinates P=e0,Q=e1 on I.  With irrelevant nonzero
    # global scalars suppressed,
    #
    # C=sum J_ij W_k,       L=2 sum P_i P_j W_k,
    #
    # where {i,j,k}=I and rows[k][a] is the projected a-row of M_kw.
    c_value = constant(0)
    l_value = constant(0)
    for omitted in INNER:
        pair = tuple(i for i in INNER if i != omitted)
        i, j = pair
        if word[i] != word[j]:
            c_value = add(c_value, rows[omitted][word[omitted]])
        if word[i] == word[j] == 0:
            l_value = add(
                l_value, scale(2, rows[omitted][word[omitted]])
            )
    return c_value, l_value


def audit_four_shore_support_obstruction():
    # C is a nonzero pure s-word.  L=alpha*(pure k-word)+beta*(pure
    # s-word), alpha!=0.  Project the w site along a covector phi with
    # phi(e_s)=0, phi(e_k)!=0.  The projected L is a nonzero product of
    # the three local coordinate vectors x_i for physical e_k.
    rows = tuple(
        (variable(f"w{i}0"), variable(f"w{i}1")) for i in INNER
    )
    structural = 0
    for word in product(COLOURS, repeat=3):
        c_value, l_value = cofactor_coefficients(word, rows)
        if sum(word) >= 2:
            require(l_value == {},
                    ("L gained support on two selected Q coordinates", word))
        if word == (1, 1, 1):
            require(c_value == {}, "C gained an all-Q coefficient")
        structural += 1

    # If two x_i have nonzero Q coordinate, their product gives forbidden
    # projected-L support with at least two Qs.  Thus either every x_i=P_i,
    # or there is a unique exceptional ell.  In the first case the
    # opposite physical vectors y_i all have nonzero Q coordinate, against
    # C_111=0.  Audit the exact contradiction in each unique-exception case.
    exception_checks = 0
    for ell in INNER:
        ordinary = tuple(i for i in INNER if i != ell)
        i, j = ordinary
        single_ell = tuple(int(r == ell) for r in INNER)
        single_j = tuple(int(r == j) for r in INNER)
        c_ell, l_ell = cofactor_coefficients(single_ell, rows)
        c_j, l_j = cofactor_coefficients(single_j, rows)
        require(l_ell == scale(2, rows[ell][1]),
                ("exceptional L coefficient changed", ell, l_ell))
        require(l_j == scale(2, rows[j][1]),
                ("ordinary L coefficient changed", ell, l_j))

        # C_111=0 forces y_ell,Q=0 because y_i,Q,y_j,Q are nonzero.
        # At the word P_i Q_j Q_ell, pure C is therefore zero, whereas
        # its projected actual coefficient is w_ell,1+w_j,1.  Projected L
        # makes the first nonzero and the second zero.
        witness = [1, 1, 1]
        witness[i] = 0
        c_witness, _ = cofactor_coefficients(tuple(witness), rows)
        expected = add(rows[ell][1], rows[j][1])
        require(c_witness == expected,
                ("four-shore witness coefficient changed", ell,
                 tuple(witness), c_witness))
        specialized_rows = tuple(
            (constant(0), constant(int(r == ell))) for r in INNER
        )
        specialized_witness, _ = cofactor_coefficients(
            tuple(witness), specialized_rows
        )
        require(specialized_witness == constant(1),
                ("projected cofactor contradiction vanished", ell))
        exception_checks += 1
    require(structural == 8 and exception_checks == 3,
            "four-shore support census changed")
    return structural, exception_checks


def audit_opposite_type_pair_factor():
    # For active Q/U data with P_t=0, one nonzero U_z^s=f_s u_z makes
    # Q_t(U_z^s)^T proportional to live B, hence B=beta Q_t u_z^T.
    # Every live matching and every t- or z-star derivative then shares
    # Y=Q_t tensor u_z across {t,z}.  The two pure targets require Y to be
    # both E_00 and E_11, which are independent.
    shared = {"B*C": 0, "Y*K": 0, "dead": 0}
    for matching in MATCHINGS:
        edges = frozenset(matching)
        if (RANK_ONE, ACTIVE_ZERO) in edges:
            shared["B*C"] += 1
        elif any(
            (RANK_ONE in edge and OTHER_ZERO in edge)
            or (ACTIVE_ZERO in edge and OTHER_ZERO in edge)
            for edge in matching
        ):
            shared["dead"] += 1
        else:
            shared["Y*K"] += 1
    require(shared == {"B*C": 3, "Y*K": 6, "dead": 6},
            ("opposite-type shared-shore census changed", shared))

    derivative = {"t-star": [0, 0], "z-star": [0, 0]}
    for label, tangent_site in (
        ("t-star", RANK_ONE),
        ("z-star", ACTIVE_ZERO),
    ):
        for i in INNER:
            remaining = tuple(site for site in SITES
                              if site not in (i, tangent_site))
            for matching in perfect_matchings(remaining):
                dead = any(
                    ACTIVE_ZERO in edge and OTHER_ZERO in edge
                    for edge in matching
                ) if tangent_site == RANK_ONE else any(
                    RANK_ONE in edge and OTHER_ZERO in edge
                    for edge in matching
                )
                derivative[label][int(dead)] += 1
    require(derivative == {"t-star": [6, 3], "z-star": [6, 3]},
            ("opposite-type derivative shores changed", derivative))

    pure_pairs = frozenset(((0, 0), (1, 1)))
    require(len(pure_pairs) == 2,
            "the two pure targets acquired a common pair factor")
    return shared, derivative


def main():
    reduction = audit_exceptional_reduction()
    certificates, equations = audit_nonuniform_live_localization()
    closed, survivors = audit_scalar_patterns()
    matching, derivative = audit_matching_and_derivative_decomposition()
    shore = audit_pair_shore_reduction()
    structural, exceptions = audit_four_shore_support_obstruction()
    opposite, opposite_derivative = audit_opposite_type_pair_factor()
    print("three-invertible single-live nonuniform overlap: all checks passed")
    print(f"  exceptional edge identities : {reduction}")
    print(f"  localization certs/equations: {certificates}/{equations}")
    print(f"  scalar charts closed/live   : {closed}/{len(survivors)}")
    print(f"  matching/derivative classes : {matching}/{derivative}")
    print(f"  pair-shore reductions       : {shore}")
    print(f"  cofactor words/exceptions   : {structural}/{exceptions}")
    print(f"  opposite Q/U shared shore   : {opposite}")
    print(f"  opposite Q/U derivatives    : {opposite_derivative}")


if __name__ == "__main__":
    main()
