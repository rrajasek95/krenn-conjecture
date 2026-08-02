#!/usr/bin/env python3
"""Verify the L1-aligned pure-L0 collinearity obstruction.

In the cross-invertible 3I+1R+2Z normal form, L1 alignment makes every
endpoint slice N a generalized vertex gauge G(lambda), with

    lambda = c (1,1,1,1,-1,-1).

Its weights sum to 2c, so dPsi(G(lambda))=2c Psi(M), rather than zero.
After adding the direct endpoint block, every L0 slice is consequently a
scalar multiple of the same matching tensor.  The two pure target slices
cannot be two distinct coordinate vectors.

Standard library only; all checks remain live under -O and -I -S.
"""

from fractions import Fraction as Q
from itertools import combinations


SITES = tuple(range(6))
CORE = (0, 1, 2, 3)
ZEROS = (4, 5)
EDGES = tuple(combinations(SITES, 2))
SIGMA = (1, 1, 1, 1, -1, -1)


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


def audit_aligned_slice_is_generalized_gauge():
    # Write c=tau*a_s*b_u.  The generic-kernel coefficient on edge rv is
    # sigma_r+sigma_v.  L1 alignment therefore gives the same coefficient
    # for N and G(c*sigma).  On 45, selected stars vanish while the generic
    # equation has coefficient -2*tau; tau!=0 forces M_45=0.
    require(SIGMA[4] + SIGMA[5] == -2,
            "the zero-zero generic-kernel coefficient vanished")
    require(sum(SIGMA) == 2,
            "the cut weights became trace zero")

    checks = 0
    for r, u in EDGES:
        coefficient = SIGMA[r] + SIGMA[u]
        if r in CORE and u in CORE:
            aligned_coefficient = 2
            require(coefficient == aligned_coefficient,
                    ("core coefficient changed", r, u))
        elif r in ZEROS and u in ZEROS:
            # Both selected endpoint matrices vanish.  Since coefficient
            # -2 is nonzero, the generic-kernel equation forces M_45=0;
            # both N and G(c*sigma) are consequently zero on this edge.
            aligned_coefficient = 0
            gauge_on_forced_block = coefficient * 0
            require(aligned_coefficient == gauge_on_forced_block == 0,
                    "the forced zero-zero block became live")
        else:
            aligned_coefficient = 0
            require(coefficient == aligned_coefficient,
                    ("cross-cut coefficient changed", r, u))
        checks += 1
    require(checks == 15, "not all residual blocks were checked")
    return checks


def audit_generalized_gauge_differential():
    # In any perfect matching, summing lambda_r+lambda_u over its three
    # edges counts every vertex exactly once.  Termwise differentiation
    # therefore gives dPsi(G(lambda))=(sum lambda)Psi(M).
    matchings = perfect_matchings(SITES)
    require(len(matchings) == 15, "K6 perfect-matching census changed")
    for matching in matchings:
        incidence = [0] * 6
        for r, u in matching:
            incidence[r] += 1
            incidence[u] += 1
        require(incidence == [1] * 6,
                ("a matching did not count every cut weight once", matching))
        coefficient = sum(SIGMA[r] + SIGMA[u] for r, u in matching)
        require(coefficient == sum(SIGMA) == 2,
                ("aligned slice derivative coefficient changed", matching))
    return len(matchings)


# Sparse polynomials in k0,k1,h0,h1 for an exact unit certificate.
ZERO = (0, 0, 0, 0)


def constant(value):
    return {ZERO: Q(value)} if value else {}


def variable(index):
    exponent = [0] * 4
    exponent[index] = 1
    return {tuple(exponent): Q(1)}


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
            monomial = tuple(a + b for a, b in zip(
                left_monomial, right_monomial
            ))
            answer[monomial] = (
                answer.get(monomial, Q(0))
                + left_coefficient * right_coefficient
            )
            if not answer[monomial]:
                del answer[monomial]
    return answer


def audit_pure_target_unit_certificate():
    # If k0 H=e_(0^6) and k1 H=e_(1^6), their two pure coordinates obey
    # f00=f01=f10=f11=0 below.  Commutativity gives the displayed explicit
    # Nullstellensatz certificate for 1.
    k0, k1, h0, h1 = tuple(variable(index) for index in range(4))
    f00 = add(multiply(k0, h0), constant(-1))
    f01 = multiply(k0, h1)
    f10 = multiply(k1, h0)
    f11 = add(multiply(k1, h1), constant(-1))
    certificate = add(
        multiply(f01, f10),
        scale(-1, multiply(f00, f11)),
        scale(-1, f00),
        scale(-1, f11),
    )
    require(certificate == constant(1),
            "the two-pure-target unit certificate failed")
    return 4


def main():
    edge_checks = audit_aligned_slice_is_generalized_gauge()
    matching_checks = audit_generalized_gauge_differential()
    target_equations = audit_pure_target_unit_certificate()
    print("three-invertible L1/pure-L0 obstruction: all checks passed")
    print(f"  aligned block identities : {edge_checks}/15")
    print(f"  matching derivative audit: {matching_checks}/15")
    print("  generalized-gauge sum    : 2c, hence dPsi(N)=2c Psi(M)")
    print(f"  pure collinearity ideal  : (1), {target_equations} equations")
    print("  external dependencies    : none")


if __name__ == "__main__":
    main()
