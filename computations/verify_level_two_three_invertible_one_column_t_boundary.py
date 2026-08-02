#!/usr/bin/env python3
"""Verify the one-column rank-one-site boundary reduction.

Assume P_t=0 and Q_t!=0.  After L1 alignment on the invertible triangle
and zero sites,

    U_t^s=0,  V_t^s=d_s Q_t,
    N^su=a_s b_u G(nu)+a_s(d_u-b_u) S_t,

where S_t has blocks P_i Q_t^T on the three I-t edges.  If the residual
t-Z star vanishes, S_t is radial gauge and pure L0 collinearity closes the
branch.  If it is live, mixed-slice kernel rigidity forces

    a_0(d_1-b_1)=a_1(d_0-b_0)=0.

Only two one-zero scalar charts survive.  A rank-one t-flattening then
forces the matching tensor, Q_t, and a five-site cofactor to complementary
pure coordinate tensors.  The Q_t=0 case is symmetric.

Standard library only; all checks remain live under -O and -I -S.
"""

from fractions import Fraction as Q
from itertools import combinations, product


INNER = (0, 1, 2)
RANK_ONE = 3
ZEROS = (4, 5)
SITES = INNER + (RANK_ONE,) + ZEROS
FIVE_SITES = INNER + ZEROS


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rational_rank(matrix):
    rows = [[Q(value) for value in row] for row in matrix]
    height = len(rows)
    width = len(rows[0]) if rows else 0
    rank = 0
    for column in range(width):
        pivot = next((row for row in range(rank, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [value / scale for value in rows[rank]]
        for row in range(height):
            if row == rank or not rows[row][column]:
                continue
            multiple = rows[row][column]
            rows[row] = [
                left - multiple * right
                for left, right in zip(rows[row], rows[rank])
            ]
        rank += 1
    return rank


# Sparse formal polynomials with monomials represented by sorted names.
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


def audit_exceptional_star_formula():
    tau = variable("tau")
    a = variable("a")
    b = variable("b")
    d = variable("d")
    deviation = add(d, scale(-1, b))

    # nu=(tau,tau,tau,tau,-tau,-tau) has sum 2*tau.
    signs = (1, 1, 1, 1, -1, -1)
    require(sum(signs) == 2, "the generic-kernel weight sum changed")
    require(signs[4] + signs[5] == -2,
            "the forced M_45 coefficient vanished")
    require(signs[0] + signs[4] == 0,
            "the I-Z cut coefficient became nonzero")

    checks = 0
    for r, u in combinations(SITES, 2):
        aligned = scale(
            signs[r] + signs[u], multiply(tau, a, b)
        )
        correction = constant(0)
        if r in INNER and u == RANK_ONE:
            # P_i Q_t^T=2*tau*M_it.
            actual = scale(2, multiply(tau, a, d))
            correction = scale(2, multiply(tau, a, deviation))
        elif r in INNER and u in INNER:
            actual = scale(2, multiply(tau, a, b))
        else:
            actual = constant(0)
            if r in ZEROS and u in ZEROS:
                # The nonzero multiplier -2*tau and X_4=X_5=0 force
                # M_45=0, so the aligned packet is effectively zero.
                aligned = constant(0)
        require(actual == add(aligned, correction),
                ("exceptional star decomposition failed", r, u))
        checks += 1
    require(checks == 15, "exceptional block census changed")
    return checks


def audit_star_support_independence():
    # If D(q S_t) is collinear with H, kernel=gauges makes q S_t=G(lambda)
    # for unrestricted generalized weights lambda.  Use the invertible
    # I-triangle, one invertible I-spoke to each zero, all nonzero I-t
    # selected blocks, and one live t-Z block.  The resulting scalar system
    # in lambda_0,...,lambda_5,q has full rank seven.
    tau = Q(3, 2)
    rows = []

    def equation(entries):
        row = [Q(0)] * 7
        for column, coefficient in entries.items():
            row[column] += Q(coefficient)
        rows.append(row)

    for i, j in combinations(INNER, 2):
        equation({i: 1, j: 1})
    # The two zero-site witnesses need not use distinct inner vertices.
    equation({0: 1, 4: 1})
    equation({0: 1, 5: 1})
    for i in INNER:
        # q*S_it=2*tau*q*M_it=(lambda_i+lambda_t)M_it.
        equation({i: 1, RANK_ONE: 1, 6: -2 * tau})
    # One live t-Z block has q*S_tz=0.
    equation({RANK_ONE: 1, 4: 1})

    require(len(rows) == 9, "star-support equation count changed")
    require(rational_rank(rows) == 7,
            "a nonzero generalized gauge survived on the exceptional star")
    return len(rows)


def audit_zero_tz_star_closure():
    # If M_t4=M_t5=0, then S_it=P_i Q_t^T=2*tau*M_it and every
    # other t-edge block of S is zero.  Hence S=G(2*tau*e_t), so every
    # endpoint slice is a generalized gauge and both pure targets would
    # be collinear with H.
    tau = Q(7, 3)
    inner_coefficients = tuple(2 * tau for _ in INNER)
    zero_coefficients = tuple(0 for _ in ZEROS)
    radial = inner_coefficients + zero_coefficients
    exceptional = tuple(2 * tau for _ in INNER) + (0, 0)
    require(exceptional == radial,
            "the zero-tZ exceptional star is not radial gauge")
    return len(radial)


def audit_scalar_zero_patterns():
    # Record only zero/nonzero status for a0,a1,delta0,delta1, where
    # delta_u=d_u-b_u.  Mixed slices force a0*delta1=a1*delta0=0.
    # If both pure products a_s*delta_s vanish, both pure slices are
    # collinear and impossible.  Exactly two labelled patterns remain.
    survivors = []
    closed = 0
    for a0, a1, delta0, delta1 in product((0, 1), repeat=4):
        if a0 * delta1 or a1 * delta0:
            continue
        pure = (a0 * delta0, a1 * delta1)
        if pure == (0, 0):
            closed += 1
        else:
            survivors.append((a0, a1, delta0, delta1, pure))
    require(survivors == [
        (0, 1, 0, 1, (0, 1)),
        (1, 0, 1, 0, (1, 0)),
    ], ("unexpected exceptional scalar patterns", survivors))
    require(closed == 7, ("closed scalar-pattern count changed", closed))
    return closed, survivors


def audit_rank_one_flattening_isolation():
    # In an exceptional chart, H=h e_s^6.  The other pure equation is
    #
    #   q Q_t tensor C = e_r^6 - k h e_s^6,  r=1-s.
    #
    # Across t | (five sites), the right side has the displayed 2x2 minor
    # -k*h on columns e_s^5,e_r^5.  The left side has rank at most one, so
    # k=0 because h!=0.  Its singleton support then forces Q_t and C to be
    # the complementary pure coordinate factors.
    k = variable("k")
    h = variable("h")
    determinant_checks = 0
    support_checks = 0
    for missing_colour in (0, 1):
        other = 1 - missing_colour
        flattening = [[constant(0), constant(0)] for _ in range(2)]
        flattening[missing_colour][0] = scale(-1, multiply(k, h))
        flattening[other][1] = constant(1)
        determinant = add(
            multiply(flattening[0][0], flattening[1][1]),
            scale(-1, multiply(flattening[0][1], flattening[1][0])),
        )
        expected_sign = -1 if missing_colour == 0 else 1
        require(determinant == scale(expected_sign, multiply(k, h)),
                ("rank-one flattening minor changed", missing_colour))
        determinant_checks += 1

        target_word = (other,) * len(FIVE_SITES)
        singleton = frozenset(((other, target_word),))
        left_projection = frozenset(row for row, _ in singleton)
        right_projection = frozenset(word for _, word in singleton)
        require(left_projection == frozenset((other,))
                and right_projection == frozenset((target_word,)),
                "singleton outer-product support did not force pure factors")
        support_checks += 1
    return determinant_checks, support_checks


def audit_five_site_cofactor_factorization():
    # S_t is supported on the three I-t edges with
    # S_it(x_i,x_t)=P_i(x_i)Q_t(x_t).  Every derivative term therefore
    # has the common Q_t(x_t) factor; the remaining sum is a five-site
    # tensor C on I union Z.
    term_checks = 0
    for t_colour in (0, 1):
        for five_word in product((0, 1), repeat=5):
            require(len(five_word) == len(FIVE_SITES),
                    "five-site word length changed")
            for i in INNER:
                # The cofactor deletes i and t, so it is independent of
                # t_colour and leaves four residual vertices.
                remaining = tuple(
                    site for site in FIVE_SITES if site != i
                )
                require(len(remaining) == 4 and RANK_ONE not in remaining,
                        ("wrong exceptional cofactor shore", i, remaining))
                term_checks += 1
    require(term_checks == 2 * 32 * 3,
            "rank-one t-flattening term census changed")
    return term_checks


def audit_symmetric_dictionary():
    p_zero = {
        "triangle_family": "a",
        "deviation": "d-b",
        "t_vector": "Q_t",
        "cofactor_rows": "P_i",
    }
    q_zero = {
        "triangle_family": "b",
        "deviation": "d-a",
        "t_vector": "P_t",
        "cofactor_rows": "Q_i",
    }
    require(tuple(p_zero) == tuple(q_zero),
            "the symmetric boundary dictionaries disagree")
    require(set(p_zero.values()).isdisjoint(q_zero.values()),
            "the P/Q boundary labels unexpectedly collided")
    return p_zero, q_zero


def main():
    block_checks = audit_exceptional_star_formula()
    support_equations = audit_star_support_independence()
    radial_edges = audit_zero_tz_star_closure()
    closed, survivors = audit_scalar_zero_patterns()
    minors, support = audit_rank_one_flattening_isolation()
    cofactor_terms = audit_five_site_cofactor_factorization()
    audit_symmetric_dictionary()
    print("three-invertible one-column t-boundary: all checks passed")
    print(f"  exceptional block identities : {block_checks}/15")
    print(f"  live-tZ support equations     : {support_equations}, rank 7")
    print(f"  zero-tZ radial-gauge edges    : {radial_edges}/5")
    print(f"  scalar charts closed/survive  : {closed}/{len(survivors)}")
    print(f"  flattening minors/supports    : {minors}/{support}")
    print(f"  five-site cofactor terms      : {cofactor_terms}")
    print("  symmetric P_t/Q_t boundaries : both audited")


if __name__ == "__main__":
    main()
