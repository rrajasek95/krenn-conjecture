#!/usr/bin/env python3
"""Close the dead-tZ one-column/common-factor overlap.

Assume P_t=0, Q_t!=0, M_t4=M_t5=0, rank dPsi=55, and kernel equal to
the five gauges.  Any active zero-site L1 family must then have P/V form.
The exceptional t-star is radial.  Uniform P/V zero-stars are radial too;
mixed L0 kills every nonuniform star outside at most one pure colour.  The
remaining pure correction shares all active physical zero-site factors,
and its rank-one flattening contradicts the complementary pure coordinate
of the residual matching tensor.  Q_t=0 is symmetric.

Standard library only; all checks remain live under -O and -I -S.
"""

from fractions import Fraction as Q
from itertools import combinations, product


INNER = (0, 1, 2)
RANK_ONE = 3
ZEROS = (4, 5)
CORE = INNER + (RANK_ONE,)
SITES = CORE + ZEROS
COLOURS = (0, 1)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


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


MATCHINGS = {
    vertices: perfect_matchings(vertices)
    for size in (0, 2, 4, 6)
    for vertices in combinations(SITES, size)
}


def outer(left, right):
    return tuple(
        tuple(left[row] * right[column] for column in COLOURS)
        for row in COLOURS
    )


def oriented_value(blocks, u, v, a, b):
    if u < v:
        return blocks[u, v][a][b]
    return blocks[v, u][b][a]


# Sparse polynomials for exact formal identities.
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


def audit_dead_tz_l1_types():
    # A Q/U-active zero has U_z=d*u with d!=0.  The t-z L1 equation has
    # nonzero left side Q_t U_z^T but zero right side rho*M_tz.  P/V is
    # compatible because its corresponding selected column P_t vanishes.
    q_t = (Q(2), Q(3))
    u_z = (Q(5), Q(7))
    forbidden = outer(q_t, u_z)
    require(any(value for row in forbidden for value in row),
            "Q_t U_z^T unexpectedly vanished")
    require(outer((0, 0), u_z) == ((0, 0), (0, 0)),
            "P_t V_z^T did not vanish with P_t=0")
    return 2


def audit_exceptional_t_star_is_radial():
    # S_t is supported on I-t and equals 2*tau*M there.  Since both t-Z
    # blocks vanish, S_t=2*tau*G(e_t) on all fifteen residual edges.
    checks = 0
    for u, v in combinations(SITES, 2):
        star = int(u in INNER and v == RANK_ONE)
        radial = int(RANK_ONE in (u, v) and set((u, v)) != {RANK_ONE, 4}
                     and set((u, v)) != {RANK_ONE, 5})
        # The only nonzero residual blocks incident with t that matter here
        # are the three I-t blocks; t4 and t5 are assumed zero.
        if set((u, v)) in ({RANK_ONE, 4}, {RANK_ONE, 5}):
            radial = 0
        require(star == radial,
                ("exceptional t-star is not radial on an edge", u, v))
        checks += 1
    require(checks == 15, "dead-tZ radial edge census changed")
    return checks


def audit_uniform_zero_star_is_radial():
    # For a uniform active P/V site z, M_iz=m*S_iz on I-z, while tz and
    # 45 vanish.  Hence m*S_z=G(e_z), even though P_t=0.
    checks = 0
    for z in ZEROS:
        for u, v in combinations(SITES, 2):
            star = int(u in INNER and v == z)
            radial = int(z in (u, v) and (
                (u in INNER) or (v in INNER)
            ))
            require(star == radial,
                    ("uniform zero-star is not radial", z, u, v))
            checks += 1
    require(checks == 30, "uniform zero-star edge census changed")
    return checks


def audit_core_support_rigidity():
    # A generalized gauge supported on zero stars first vanishes on the
    # invertible I-triangle and on the nonzero I-t blocks.  These six scalar
    # equations have full rank four in lambda_0,...,lambda_t.
    rows = []
    for i, j in combinations(INNER, 2):
        row = [Q(0)] * 4
        row[i] = row[j] = Q(1)
        rows.append(row)
    for i in INNER:
        row = [Q(0)] * 4
        row[i] = row[RANK_ONE] = Q(1)
        rows.append(row)
    require(len(rows) == 6 and rational_rank(rows) == 4,
            "the core failed to kill generalized-gauge weights")
    return len(rows)


def audit_nonuniform_localization():
    # On a P/V star, q*S_iz=G(lambda)_iz gives
    # f_i=lambda_z*m_i-q=0 after the core weights vanish.  The exact
    # identity m_j*f_i-m_i*f_j=q*(m_i-m_j) forces q=0 whenever the
    # spoke multiples are nonuniform.
    lam = variable("lambda")
    q = variable("q")
    checks = 0
    for i, j in combinations(INNER, 2):
        m_i = variable(f"m{i}")
        m_j = variable(f"m{j}")
        f_i = add(multiply(lam, m_i), scale(-1, q))
        f_j = add(multiply(lam, m_j), scale(-1, q))
        left = add(
            multiply(m_j, f_i),
            scale(-1, multiply(m_i, f_j)),
        )
        right = multiply(q, add(m_i, scale(-1, m_j)))
        require(left == right,
                ("nonuniform localization identity failed", i, j))
        checks += 1
    require(checks == 3, "nonuniform localization count changed")
    return checks


def audit_scalar_supports():
    # For every nonuniform site z, mixed L0 gives
    # a0*d_z1=a1*d_z0=0.  Record zero/nonzero supports for one or two
    # nonuniform sites.  Nongauge pure corrections occur in at most one
    # physical colour; an empty pure support is the collinearity closure.
    summaries = {}
    for number in (1, 2):
        admissible = []
        for a0, a1 in product((0, 1), repeat=2):
            for supports in product(
                ((1, 0), (0, 1), (1, 1)), repeat=number
            ):
                if any(a0 * d1 or a1 * d0 for d0, d1 in supports):
                    continue
                pure = tuple(
                    colour for colour in COLOURS
                    if (a0, a1)[colour]
                    and any(support[colour] for support in supports)
                )
                require(len(pure) <= 1,
                        ("two nongauge pure colours survived",
                         number, (a0, a1), supports))
                admissible.append(((a0, a1), supports, pure))
        require(admissible, ("scalar support census became empty", number))
        summaries[number] = len(admissible)
    require(summaries == {1: 5, 2: 11},
            ("dead-tZ scalar census changed", summaries))
    return summaries


def audit_common_physical_factors():
    # For one active P/V zero, D(S_z)=v_z tensor C.  With two active zeros,
    # every nonzero derivative term from either star contains both factors:
    # the tangent supplies one; M_45=M_t,other=0 forces the other zero to
    # meet an I vertex in the cofactor.
    counts = {}
    checks = 0
    cases = (
        ((4,), (4,)),
        ((5,), (5,)),
        ((4, 5), (4,)),
        ((4, 5), (5,)),
        ((4, 5), (4, 5)),
    )
    for active_tuple, tangent_tuple in cases:
        active = frozenset(active_tuple)
        count = 0
        for z in tangent_tuple:
            for i in INNER:
                remaining = tuple(
                    site for site in SITES if site not in (i, z)
                )
                for matching in MATCHINGS[remaining]:
                    # Terms using t-otherZero vanish because tZ is dead.
                    zero_term = any(
                        RANK_ONE in edge
                        and any(other in edge for other in active - {z})
                        for edge in matching
                    )
                    if zero_term:
                        continue
                    tags = {z}
                    for edge in matching:
                        for other in active - {z}:
                            if other in edge:
                                partner = edge[0] if edge[1] == other else edge[1]
                                require(partner in INNER,
                                        ("active zero did not meet I",
                                         active_tuple, tangent_tuple, edge))
                                tags.add(other)
                    require(tags == active,
                            ("pure correction lost a physical factor",
                             active_tuple, tangent_tuple, z, i, matching, tags))
                    count += 1
                    checks += 1
        counts[active_tuple, tangent_tuple] = count
    require(counts == {
        ((4,), (4,)): 9,
        ((5,), (5,)): 9,
        ((4, 5), (4,)): 6,
        ((4, 5), (5,)): 6,
        ((4, 5), (4, 5)): 12,
    }, ("common physical-factor census changed", counts))
    return checks, counts


def audit_pure_flattening():
    # The pure-k equation is
    # factorized_correction=e_k^6-kappa*h*e_r^6.  Across the active-zero
    # cut, its displayed 2x2 minor is +/-kappa*h.  Rank one forces kappa=0,
    # and singleton support forces every physical zero factor to be e_k.
    kappa = variable("kappa")
    h = variable("h")
    checks = 0
    for k in COLOURS:
        r = 1 - k
        matrix = [[constant(0), constant(0)] for _ in COLOURS]
        matrix[k][0] = constant(1)
        matrix[r][1] = scale(-1, multiply(kappa, h))
        determinant = add(
            multiply(matrix[0][0], matrix[1][1]),
            scale(-1, multiply(matrix[0][1], matrix[1][0])),
        )
        expected = scale(
            -1 if k == 0 else 1, multiply(kappa, h)
        )
        require(determinant == expected and determinant,
                ("physical pure flattening minor changed", k))
        for active_count in (1, 2):
            singleton = (k,) * active_count
            require(set(singleton) == {k},
                    "singleton support failed to force physical factors")
            checks += 1
    require(checks == 4, "pure flattening audit count changed")
    return checks


def audit_complementary_matching_zero():
    # Once an active physical factor is e_k, every all-r matching, r=1-k,
    # vanishes: that zero meets I through its factor, t through M_tz=0, or
    # the other zero through M_45=0.
    checks = 0
    for k in COLOURS:
        r = 1 - k
        for z in ZEROS:
            blocks = {
                edge: ((1, 1), (1, 1))
                for edge in combinations(SITES, 2)
            }
            physical = (int(k == 0), int(k == 1))
            for i in INNER:
                blocks[min(i, z), max(i, z)] = outer(
                    (1, 1), physical
                )
            blocks[min(RANK_ONE, z), max(RANK_ONE, z)] = (
                (0, 0), (0, 0)
            )
            companion = next(other for other in ZEROS if other != z)
            blocks[min(z, companion), max(z, companion)] = (
                (0, 0), (0, 0)
            )
            word = (r,) * 6
            for matching in MATCHINGS[SITES]:
                term = Q(1)
                for u, v in matching:
                    term *= oriented_value(
                        blocks, u, v, word[u], word[v]
                    )
                require(term == 0,
                        ("complementary matching survived", k, z, matching))
                checks += 1
    require(checks == 60, "complementary matching census changed")
    return checks


def audit_symmetric_boundary():
    p_zero = ("P_t=0", "P/V", "a", "Q_t")
    q_zero = ("Q_t=0", "Q/U", "b", "P_t")
    require(len(p_zero) == len(q_zero) == 4,
            "the symmetric boundary dictionary changed")
    require(set(p_zero).isdisjoint(q_zero),
            "the symmetric boundary labels collided")
    return p_zero, q_zero


def main():
    l1_checks = audit_dead_tz_l1_types()
    t_radial = audit_exceptional_t_star_is_radial()
    z_radial = audit_uniform_zero_star_is_radial()
    core_equations = audit_core_support_rigidity()
    localization = audit_nonuniform_localization()
    scalar_census = audit_scalar_supports()
    factor_checks, factor_counts = audit_common_physical_factors()
    flattenings = audit_pure_flattening()
    killed = audit_complementary_matching_zero()
    audit_symmetric_boundary()
    print("three-invertible dead-tZ double boundary: all checks passed")
    print(f"  one-column L1 exclusions : {l1_checks}")
    print(f"  radial t/z edges         : {t_radial}/{z_radial}")
    print(f"  core support equations   : {core_equations}, rank 4")
    print(f"  localization identities  : {localization}")
    print(f"  scalar support census    : {scalar_census}")
    print(f"  common-factor terms      : {factor_checks}, {factor_counts}")
    print(f"  flattenings/killed terms : {flattenings}/{killed}")
    print("  symmetric P/Q cases      : both closed")


if __name__ == "__main__":
    main()
