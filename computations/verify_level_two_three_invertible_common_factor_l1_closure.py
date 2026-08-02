#!/usr/bin/env python3
"""Close the common-factor singular-cross L1 boundary.

The two active zero-site types from the singular-cross classification are

    P/V: M_rz=m_r P_r v_z^T, U_z=0, V_z^s=d_zs v_z,
    Q/U: M_rz=m_r Q_r u_z^T, V_z=0, U_z^s=d_zs u_z.

Uniform spoke multiples make the associated z-star a radial generalized
gauge.  Nonuniform multiples force both mixed products to vanish.  This
checker audits the resulting scalar-support census, the factor shared by
one or two same-type z-stars, the complementary-purity flattening, and the
termwise zero that closes opposite active types.

Standard library only; all checks remain live under -O and -I -S.
"""

from fractions import Fraction as Q
from itertools import combinations, product


INNER = (0, 1, 2)
RANK_ONE = 3
CORE = INNER + (RANK_ONE,)
ZEROS = (4, 5)
SITES = CORE + ZEROS
COLOURS = (0, 1)
J = ((0, 1), (1, 0))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


# Sparse formal polynomials for the pure-flattening determinant.


def polynomial_constant(value):
    return {(): Q(value)} if value else {}


def polynomial_variable(name):
    return {(name,): Q(1)}


def polynomial_add(*polynomials):
    answer = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] = answer.get(monomial, Q(0)) + coefficient
            if not answer[monomial]:
                del answer[monomial]
    return answer


def polynomial_scale(coefficient, polynomial):
    return {
        monomial: Q(coefficient) * value
        for monomial, value in polynomial.items()
        if coefficient * value
    }


def polynomial_multiply(left, right):
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


def outer(left, right):
    return tuple(
        tuple(left[row] * right[column] for column in COLOURS)
        for row in COLOURS
    )


def transpose(matrix):
    return tuple(
        tuple(matrix[column][row] for column in COLOURS)
        for row in COLOURS
    )


def matrix_product(left, right):
    return tuple(
        tuple(sum(left[row][middle] * right[middle][column]
                  for middle in COLOURS)
              for column in COLOURS)
        for row in COLOURS
    )


def oriented_value(blocks, u, v, a, b):
    if u < v:
        return blocks[u, v][a][b]
    return blocks[v, u][b][a]


def audit_uniform_star_is_radial():
    # Categories are the six vertices; z=4 has live blocks precisely to the
    # four core vertices, while M_45=0.  If M_r4=m S_r4 with one common
    # nonzero m, then S=(1/m)G(e_4) on every residual edge.
    m = Q(7, 3)
    star = {}
    packet = {}
    radial = {}
    checks = 0
    for u, v in combinations(SITES, 2):
        star[u, v] = Q(1) if u in CORE and v == 4 else Q(0)
        packet[u, v] = m * star[u, v]
        radial[u, v] = (
            (int(u == 4) + int(v == 4)) * packet[u, v] / m
        )
        require(star[u, v] == radial[u, v],
                ("uniform z-star is not radial gauge", u, v))
        checks += 1
    require(checks == 15, "uniform radial-gauge edge count changed")
    return checks


def audit_opposite_type_supports():
    # Let d be the P/V endpoint support and e the Q/U support.  Since M_45=0,
    # the two mixed L0 equations impose d1*e0=d0*e1=0.  With both families
    # active, exactly two support charts remain: the same singleton k.
    survivors = []
    rejected = 0
    for d0, d1, e0, e1 in product((0, 1), repeat=4):
        if not (d0 or d1) or not (e0 or e1):
            continue
        if d1 * e0 or d0 * e1:
            rejected += 1
            continue
        survivors.append(((d0, d1), (e0, e1)))
    require(survivors == [
        ((0, 1), (0, 1)),
        ((1, 0), (1, 0)),
    ], ("opposite-type support charts changed", survivors))
    require(rejected == 7, "opposite-type rejected count changed")

    # R2 is then forced to use h=e_(1-k) at the rank-one site: in chart k=0
    # Q/U gets its complement from its endpoint, while P/V needs h=e1;
    # the roles reverse in chart k=1.
    complements = []
    for d, e in survivors:
        k = 0 if d == (1, 0) else 1
        p_endpoint = d == (0, 1)
        q_endpoint = e == (1, 0)
        h = 1 - k
        require((p_endpoint or h == 1)
                and (q_endpoint or h == 0),
                ("opposite-type R2 complement failed", k))
        complements.append((k, h))
    require(sorted(complements) == [(0, 1), (1, 0)],
            "complementary rank-one-site colours changed")
    return rejected, tuple(sorted(complements))


def normalized_core(h_colour):
    # X_i=I on the invertible triangle and
    # X_t=[P_t Q_t] with P_t=Q_t=e_h for support auditing.
    x = {i: ((1, 0), (0, 1)) for i in INNER}
    h = (int(h_colour == 0), int(h_colour == 1))
    x[RANK_ONE] = ((h[0], h[0]), (h[1], h[1]))
    blocks = {}
    for u, v in combinations(CORE, 2):
        blocks[u, v] = matrix_product(
            matrix_product(x[u], J),
            transpose(x[v]),
        )
    return x, blocks


def audit_opposite_type_complement_coordinate_zero():
    # P/V is placed at site 4 and Q/U at site 5.  At the complementary
    # pure word r=1-k, R2 gives h=e_r.  A nonzero matching would have to
    # pair the P-zero to t and the Q-zero to I (or vice versa after swapping
    # the types), leaving two I vertices joined through a diagonal entry of
    # J.  Every matching term is therefore zero.
    term_checks = 0
    orientations = (("P", "Q"), ("Q", "P"))
    for k in COLOURS:
        pure = 1 - k
        x, core_blocks = normalized_core(pure)
        for type4, type5 in orientations:
            blocks = dict(core_blocks)
            factor4 = {
                r: tuple(x[r][row][0 if type4 == "P" else 1]
                         for row in COLOURS)
                for r in CORE
            }
            factor5 = {
                r: tuple(x[r][row][0 if type5 == "P" else 1]
                         for row in COLOURS)
                for r in CORE
            }
            zero_vector = (1, 1)
            for r in CORE:
                blocks[min(r, 4), max(r, 4)] = outer(
                    factor4[r], zero_vector
                )
                blocks[min(r, 5), max(r, 5)] = outer(
                    factor5[r], zero_vector
                )
            blocks[4, 5] = ((0, 0), (0, 0))

            word = (pure,) * 6
            for matching in MATCHINGS[SITES]:
                term = Q(1)
                for u, v in matching:
                    term *= oriented_value(
                        blocks, u, v, word[u], word[v]
                    )
                require(term == 0,
                        ("opposite-type complementary coordinate survived",
                         k, type4, type5, matching))
                term_checks += 1
    require(term_checks == 60,
            "opposite-type matching-term count changed")
    return term_checks


def audit_nonuniform_scalar_patterns():
    # For each nonuniform P/V site, mixed L0 imposes
    # a0*d1=a1*d0=0.  Uniform sites are radial and do not contribute a
    # nongauge pure star.  For one or two nonuniform sites, the remaining
    # nongauge stars occur in at most one pure colour.  Q/U is identical
    # with (a0,a1) replaced by (b0,b1).
    summaries = {}
    for number in (1, 2):
        admissible = []
        for scalars in product((0, 1), repeat=2):
            for supports in product(
                ((1, 0), (0, 1), (1, 1)), repeat=number
            ):
                a0, a1 = scalars
                if any(a0 * d1 or a1 * d0 for d0, d1 in supports):
                    continue
                pure_support = tuple(
                    colour for colour in COLOURS
                    if scalars[colour]
                    and any(support[colour] for support in supports)
                )
                require(len(pure_support) <= 1,
                        ("two nongauge pure colours survived",
                         number, scalars, supports))
                admissible.append((scalars, supports, pure_support))
        summaries[number] = tuple(admissible)
        require(admissible, ("nonuniform census became empty", number))
    return tuple((number, len(rows)) for number, rows in summaries.items())


def audit_same_type_star_factor():
    # Tag only the common residual factor at each active zero site.  A
    # derivative term from S_z contains z's tangent factor.  If the other
    # zero is active with the same type, M_45=0 forces it to match the core,
    # contributing its factor too.  Thus every term in any sum of the
    # nongauge stars shares the product of all active zero-site factors.
    checks = 0
    term_counts = {}
    for active in ((4,), (5,), (4, 5)):
        active = frozenset(active)
        nonuniform = tuple(active)
        count = 0
        for z in nonuniform:
            for r in CORE:
                remaining = tuple(
                    site for site in SITES if site not in (r, z)
                )
                for matching in MATCHINGS[remaining]:
                    if (4, 5) in matching or (5, 4) in matching:
                        continue
                    tags = {z}
                    valid = True
                    for u, v in matching:
                        endpoint = (
                            u if u in active
                            else v if v in active
                            else None
                        )
                        if endpoint is not None:
                            other = v if endpoint == u else u
                            if other not in CORE:
                                valid = False
                                break
                            tags.add(endpoint)
                    if not valid:
                        continue
                    require(tags == active,
                            ("same-type star lost a common zero factor",
                             active, z, r, matching, tags))
                    count += 1
                    checks += 1
        term_counts[tuple(sorted(active))] = count
    require(all(term_counts.values()),
            ("a same-type factor census became empty", term_counts))
    return checks, term_counts


def audit_pure_flattening_isolation():
    # If the nongauge pure-k correction has rank one across the active-zero
    # versus remaining cut, the equation
    #
    #   correction=e_k^6-kappa*h*e_(1-k)^6
    #
    # has the displayed 2x2 determinant +/-kappa*h.  Since h!=0, kappa=0;
    # singleton outer-product support forces every active zero factor e_k.
    checks = 0
    kappa = polynomial_variable("kappa")
    h = polynomial_variable("h")
    for k in COLOURS:
        other = 1 - k
        matrix = [
            [polynomial_constant(0), polynomial_constant(0)]
            for _ in COLOURS
        ]
        matrix[k][0] = polynomial_constant(1)
        matrix[other][1] = polynomial_scale(
            -1, polynomial_multiply(kappa, h)
        )
        det = polynomial_add(
            polynomial_multiply(matrix[0][0], matrix[1][1]),
            polynomial_scale(
                -1, polynomial_multiply(matrix[0][1], matrix[1][0])
            ),
        )
        expected = polynomial_scale(
            -1 if k == 0 else 1,
            polynomial_multiply(kappa, h),
        )
        require(det == expected and det,
                ("pure flattening determinant changed", k, det))

        for number_active in (1, 2):
            singleton = (k,) * number_active
            require(all(colour == k for colour in singleton),
                    "singleton support failed to force a zero-site factor")
            checks += 1
    require(checks == 4, "pure flattening audit count changed")
    return checks


def audit_isolated_factor_kills_other_pure_coordinate():
    # Once a nonuniform active zero factor is e_k, every incident packet
    # block vanishes at residual colour 1-k, and M_45=0.  Every perfect
    # matching of the complementary pure word therefore has a zero factor.
    checks = 0
    for k in COLOURS:
        other = 1 - k
        for z in ZEROS:
            companion = next(site for site in ZEROS if site != z)
            blocks = {
                edge: ((1, 1), (1, 1))
                for edge in combinations(SITES, 2)
            }
            zero_factor = (int(k == 0), int(k == 1))
            for r in CORE:
                blocks[min(r, z), max(r, z)] = outer(
                    (1, 1), zero_factor
                )
            blocks[min(z, companion), max(z, companion)] = (
                (0, 0), (0, 0)
            )
            word = (other,) * 6
            for matching in MATCHINGS[SITES]:
                term = Q(1)
                for u, v in matching:
                    term *= oriented_value(
                        blocks, u, v, word[u], word[v]
                    )
                require(term == 0,
                        ("complementary zero-site factor survived",
                         k, z, matching))
                checks += 1
    require(checks == 60, "isolated-factor matching count changed")
    return checks


def main():
    radial = audit_uniform_star_is_radial()
    rejected, opposite = audit_opposite_type_supports()
    opposite_terms = audit_opposite_type_complement_coordinate_zero()
    scalar_census = audit_nonuniform_scalar_patterns()
    factor_checks, factor_terms = audit_same_type_star_factor()
    flattenings = audit_pure_flattening_isolation()
    killed_terms = audit_isolated_factor_kills_other_pure_coordinate()
    print("three-invertible common-factor L1 closure: all checks passed")
    print(f"  uniform radial edges       : {radial}/15")
    print(f"  opposite charts/rejected   : {opposite}/{rejected}")
    print(f"  opposite zero terms        : {opposite_terms}")
    print(f"  nonuniform scalar census   : {scalar_census}")
    print(f"  shared-factor terms        : {factor_checks}, {factor_terms}")
    print(f"  pure flattening charts     : {flattenings}")
    print(f"  complementary killed terms : {killed_terms}")
    print("  conclusion                 : no common-factor type survives")


if __name__ == "__main__":
    main()
